"""
Team recent-form scraper for Soccerway.

What this scraper stores for top 5 teams in each top-5 league:
- Overall standings snapshot
- Last-5 overall form and goals for/against
- Last-5 home form and goals for/against
- Last-5 away form and goals for/against
- Clean sheets in recent overall matches (computed from match pages)

Data is saved into a dedicated SQLite database: team_recent_form.db
This keeps team-level features separate from the players database.
"""

import logging
import os
import re
import sqlite3
import time
from datetime import datetime
from urllib.parse import urljoin

import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

try:
    from .team_recent_form_config import (
        BASE_URL,
        COUNTRY_TO_LEAGUE_KEY,
        LEAGUE_STANDINGS,
        PLAYERS_DB_PATH,
        RECENT_FORM_SAMPLE_SIZE,
        REQUEST_TIMEOUT,
        Selectors,
        TEAM_FORM_DB_PATH,
        TEAM_NAME_ALIASES,
        TARGET_TEAMS,
        TOP_TEAMS_PER_LEAGUE,
        Timeouts,
    )
except ImportError:
    from team_recent_form_config import (
        BASE_URL,
        COUNTRY_TO_LEAGUE_KEY,
        LEAGUE_STANDINGS,
        PLAYERS_DB_PATH,
        RECENT_FORM_SAMPLE_SIZE,
        REQUEST_TIMEOUT,
        Selectors,
        TEAM_FORM_DB_PATH,
        TEAM_NAME_ALIASES,
        TARGET_TEAMS,
        TOP_TEAMS_PER_LEAGUE,
        Timeouts,
    )

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


def init_db(db_path: str = TEAM_FORM_DB_PATH) -> sqlite3.Connection:
    """Create or open team-form DB and ensure schema exists."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")

    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leagues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                league_key TEXT NOT NULL UNIQUE,
                league_name TEXT NOT NULL,
                standings_overall_url TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                league_id INTEGER NOT NULL,
                team_name TEXT NOT NULL,
                team_url TEXT NOT NULL,
                team_slug_key TEXT NOT NULL,
                rank_overall INTEGER,
                matches_overall INTEGER,
                wins_overall INTEGER,
                draws_overall INTEGER,
                losses_overall INTEGER,
                goals_for_overall INTEGER,
                goals_against_overall INTEGER,
                goal_diff_overall INTEGER,
                points_overall INTEGER,
                scraped_at TEXT NOT NULL,
                UNIQUE (league_id, team_slug_key, scraped_at),
                FOREIGN KEY (league_id) REFERENCES leagues(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS team_recent_forms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                scope TEXT NOT NULL,
                sample_size INTEGER NOT NULL,
                matches_played INTEGER,
                wins INTEGER,
                draws INTEGER,
                losses INTEGER,
                goals_for INTEGER,
                goals_against INTEGER,
                goal_diff INTEGER,
                points INTEGER,
                form_sequence TEXT,
                scraped_at TEXT NOT NULL,
                UNIQUE (team_id, scope, scraped_at),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS team_recent_matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                scope TEXT NOT NULL,
                match_url TEXT NOT NULL,
                result_token TEXT,
                goals_for INTEGER,
                goals_against INTEGER,
                clean_sheet INTEGER,
                sequence_index INTEGER,
                scraped_at TEXT NOT NULL,
                UNIQUE (team_id, scope, match_url, scraped_at),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS team_model_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                league_key TEXT NOT NULL,
                team_name TEXT NOT NULL,
                scraped_at TEXT NOT NULL,
                rank_overall INTEGER,
                points_overall INTEGER,
                matches_overall INTEGER,
                goals_for_overall INTEGER,
                goals_against_overall INTEGER,
                goal_diff_overall INTEGER,
                form_overall_last5 TEXT,
                wins_overall_last5 INTEGER,
                draws_overall_last5 INTEGER,
                losses_overall_last5 INTEGER,
                goals_for_overall_last5 INTEGER,
                goals_against_overall_last5 INTEGER,
                points_overall_last5 INTEGER,
                clean_sheets_overall_last5 INTEGER,
                form_home_last5 TEXT,
                wins_home_last5 INTEGER,
                draws_home_last5 INTEGER,
                losses_home_last5 INTEGER,
                goals_for_home_last5 INTEGER,
                goals_against_home_last5 INTEGER,
                points_home_last5 INTEGER,
                form_away_last5 TEXT,
                wins_away_last5 INTEGER,
                draws_away_last5 INTEGER,
                losses_away_last5 INTEGER,
                goals_for_away_last5 INTEGER,
                goals_against_away_last5 INTEGER,
                points_away_last5 INTEGER,
                UNIQUE (team_id, scraped_at),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS team_player_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER NOT NULL,
                player_team_name TEXT NOT NULL,
                player_team_url TEXT,
                players_db_path TEXT NOT NULL,
                matched_by TEXT NOT NULL,
                scraped_at TEXT NOT NULL,
                UNIQUE (team_id, player_team_name, scraped_at),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
            """
        )

    return conn


def _make_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1920, 1080)
    driver.set_page_load_timeout(90)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


def _safe_get(driver: webdriver.Chrome, url: str, attempts: int = 3, wait_after: float = 1.0) -> None:
    """Open URL with retry to survive transient page-load hangs/timeouts."""
    last_exc = None
    for attempt in range(1, attempts + 1):
        try:
            driver.get(url)
            if wait_after:
                time.sleep(wait_after)
            return
        except (TimeoutException, WebDriverException) as exc:
            last_exc = exc
            log.warning("Navigation attempt %d/%d failed for %s: %s", attempt, attempts, url, exc)
            try:
                driver.execute_script("window.stop();")
            except Exception:
                pass
            time.sleep(1.0)
    raise RuntimeError(f"Failed to open URL after {attempts} attempts: {url}") from last_exc


def _dismiss_consent(driver: webdriver.Chrome) -> None:
    for xpath in Selectors.CONSENT_BUTTONS_XPATH:
        try:
            btn = WebDriverWait(driver, 4).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            time.sleep(1)
            log.info("Consent banner dismissed.")
            return
        except Exception:
            continue


def _wait_rows(driver: webdriver.Chrome) -> None:
    WebDriverWait(driver, Timeouts.ROWS_WAIT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.ROWS))
    )


def _to_int(value: str):
    if value is None:
        return None
    cleaned = str(value).strip().replace(",", "")
    if cleaned == "" or cleaned == "?":
        return None
    try:
        return int(cleaned)
    except ValueError:
        return None


def _extract_team_key(team_href: str) -> str:
    if not team_href:
        return ""
    parts = [p for p in team_href.strip("/").split("/") if p]
    return parts[-1] if parts else ""


def _parse_gf_ga(score_text: str):
    if not score_text or ":" not in score_text:
        return None, None
    left, right = score_text.split(":", 1)
    return _to_int(left), _to_int(right)


def _normalize_team_name(name: str) -> str:
    if not name:
        return ""

    n = name.lower().strip()
    n = n.replace(".", " ")
    n = n.replace("-", " ")
    n = n.replace("'", "")
    n = re.sub(r"\s+", " ", n)

    alias = TEAM_NAME_ALIASES.get(n)
    if alias is not None:
        return alias

    n = re.sub(r"\b(fc|cf|ac|sc|afc|cfc|u\.?s\.?|s\.s\.c\.)\b", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n


def _is_target_team(team_name: str) -> bool:
    target_names = {_normalize_team_name(name) for name in TARGET_TEAMS}
    return _normalize_team_name(team_name) in target_names


def _build_form_urls(standings_overall_url: str, sample_size: int):
    base = standings_overall_url
    if "/standings/overall/" not in base:
        raise ValueError(f"Unexpected standings URL format: {standings_overall_url}")

    return {
        "overall": base.replace("/standings/overall/", f"/form/overall/{sample_size}/"),
        "home": base.replace("/standings/overall/", f"/form/home/{sample_size}/"),
        "away": base.replace("/standings/overall/", f"/form/away/{sample_size}/"),
    }


def _parse_table_rows(
    driver: webdriver.Chrome,
    top_n: int = None,
    allowed_team_keys=None,
):
    rows = driver.find_elements(By.CSS_SELECTOR, Selectors.ROWS)
    parsed = []

    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "div.table__cell")
        if len(cells) < 2:
            continue

        try:
            team_el = row.find_element(By.CSS_SELECTOR, Selectors.TEAM_LINK)
        except NoSuchElementException:
            continue

        team_name = team_el.text.strip()
        team_href = team_el.get_attribute("href")
        rel_href = team_el.get_attribute("href") or ""
        team_key = _extract_team_key(rel_href)

        if allowed_team_keys and team_key not in allowed_team_keys:
            continue

        rank_text = None
        gp = None
        wins = None
        draws = None
        losses = None
        gf = None
        ga = None
        gd = None
        pts = None
        form_text = ""

        if len(cells) >= 10:
            rank_text = cells[0].text.strip().replace(".", "")
            gp = _to_int(cells[2].text)
            wins = _to_int(cells[3].text)
            draws = _to_int(cells[4].text)
            losses = _to_int(cells[5].text)
            gf, ga = _parse_gf_ga(cells[6].text.strip())
            gd = _to_int(cells[7].text)
            pts = _to_int(cells[8].text)
            form_text = re.sub(r"[^WDL?]", "", cells[9].text.strip().upper())
        else:
            # Fallback for compact DOM layouts where only a few "cell" nodes exist.
            # Example row text lines:
            # 1. / Barcelona / 37 / 31 / 1 / 5 / 94:33 / 61 / 94 / ? / W / L / W / W / W
            lines = [ln.strip() for ln in row.text.splitlines() if ln.strip()]
            if len(lines) >= 9:
                rank_text = lines[0].replace(".", "")
                numeric_block = lines[2:9]
                if len(numeric_block) == 7:
                    gp = _to_int(numeric_block[0])
                    wins = _to_int(numeric_block[1])
                    draws = _to_int(numeric_block[2])
                    losses = _to_int(numeric_block[3])
                    gf, ga = _parse_gf_ga(numeric_block[4])
                    gd = _to_int(numeric_block[5])
                    pts = _to_int(numeric_block[6])
                form_tail = "".join(lines[9:]) if len(lines) > 9 else ""
                form_text = re.sub(r"[^WDL?]", "", form_tail.upper())

        form_links = []
        for a in row.find_elements(By.CSS_SELECTOR, Selectors.FORM_LINKS):
            href = a.get_attribute("href")
            token = (a.text or "").strip().upper()
            if href:
                form_links.append(
                    {
                        "token": token if token in {"W", "D", "L", "?"} else "",
                        "url": href if href.startswith("http") else urljoin(BASE_URL, href),
                    }
                )

        parsed.append(
            {
                "rank": _to_int(rank_text),
                "team_name": team_name,
                "team_href": team_href,
                "team_key": team_key,
                "matches": gp,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "goals_for": gf,
                "goals_against": ga,
                "goal_diff": gd,
                "points": pts,
                "form_sequence": form_text,
                "form_links": form_links,
            }
        )

    parsed.sort(key=lambda x: (x["rank"] if x["rank"] is not None else 999))
    if top_n is not None:
        parsed = parsed[:top_n]
    return parsed


def _team_keys_from_match_url(match_url: str):
    """Extract (home_key, away_key) from a Soccerway match URL.

    URL pattern: /match/{home-name}-{home_key}/{away-name}-{away_key}/
    Example: /match/barcelona-SKbpVP5K/betis-vJbTeCGP/?mid=...
    """
    m = re.search(r'/match/[^/]+-([A-Za-z0-9]+)/[^/]+-([A-Za-z0-9]+)/', match_url)
    if m:
        return m.group(1), m.group(2)
    return None, None


def _fetch_match_result_selenium(
    driver: webdriver.Chrome, match_url: str, team_key: str, result_token: str = None
):
    """Fetch match scoreline via Selenium (scores are JS-rendered on Soccerway).

    Optimisations:
    - Losses are never clean sheets: return early without loading the page.
    - Unknown/pending ('?') results are skipped.
    - Home/away team identification is done from the URL, not from HTML.
    """
    if result_token == "L":
        # We know opponent scored >= 1: no clean sheet, but goals are unknown.
        return {"goals_for": None, "goals_against": None, "clean_sheet": 0}
    if result_token in (None, "?"):
        return None

    home_key, away_key = _team_keys_from_match_url(match_url)
    if not home_key or not away_key:
        log.warning("Could not parse team keys from match URL: %s", match_url)
        return None
    if team_key not in (home_key, away_key):
        log.warning("team_key %s not in match URL %s", team_key, match_url)
        return None

    try:
        _safe_get(driver, match_url, wait_after=0)
        # Wait for the score element to appear and contain digits.
        WebDriverWait(driver, 15).until(
            lambda d: bool(
                re.search(
                    r'\d+\s*-\s*\d+',
                    d.find_element(By.CSS_SELECTOR, ".detailScore__wrapper").text,
                )
            )
        )
        score_text = driver.find_element(By.CSS_SELECTOR, ".detailScore__wrapper").text.strip()
    except (TimeoutException, NoSuchElementException):
        log.warning("Score element not found or timed out for %s", match_url)
        return None
    except Exception as exc:
        log.warning("Unexpected error fetching %s: %s", match_url, exc)
        return None

    score_match = re.search(r'(\d+)\s*-\s*(\d+)', score_text)
    if not score_match:
        log.warning("Could not parse score from text %r at %s", score_text, match_url)
        return None

    home_goals, away_goals = int(score_match.group(1)), int(score_match.group(2))
    if team_key == home_key:
        gf, ga = home_goals, away_goals
    else:
        gf, ga = away_goals, home_goals

    return {"goals_for": gf, "goals_against": ga, "clean_sheet": 1 if ga == 0 else 0}


def _upsert_league(conn: sqlite3.Connection, league_key: str, league_name: str, standings_url: str) -> int:
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO leagues (league_key, league_name, standings_overall_url)
            VALUES (?, ?, ?)
            """,
            (league_key, league_name, standings_url),
        )

    cur = conn.execute("SELECT id FROM leagues WHERE league_key = ?", (league_key,))
    row = cur.fetchone()
    if not row:
        raise RuntimeError(f"Failed to upsert league: {league_key}")
    return row[0]


def _insert_team(conn: sqlite3.Connection, league_id: int, team_row: dict, scraped_at: str) -> int:
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO teams (
                league_id, team_name, team_url, team_slug_key,
                rank_overall, matches_overall, wins_overall, draws_overall, losses_overall,
                goals_for_overall, goals_against_overall, goal_diff_overall, points_overall,
                scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                league_id,
                team_row["team_name"],
                team_row["team_href"],
                team_row["team_key"],
                team_row["rank"],
                team_row["matches"],
                team_row["wins"],
                team_row["draws"],
                team_row["losses"],
                team_row["goals_for"],
                team_row["goals_against"],
                team_row["goal_diff"],
                team_row["points"],
                scraped_at,
            ),
        )

    cur = conn.execute(
        """
        SELECT id
        FROM teams
        WHERE league_id = ? AND team_slug_key = ? AND scraped_at = ?
        """,
        (league_id, team_row["team_key"], scraped_at),
    )
    row = cur.fetchone()
    if not row:
        raise RuntimeError(f"Failed to insert team: {team_row['team_name']}")
    return row[0]


def _insert_form(conn: sqlite3.Connection, team_id: int, scope: str, row: dict, scraped_at: str) -> None:
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO team_recent_forms (
                team_id, scope, sample_size, matches_played, wins, draws, losses,
                goals_for, goals_against, goal_diff, points, form_sequence, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                team_id,
                scope,
                RECENT_FORM_SAMPLE_SIZE,
                row.get("matches"),
                row.get("wins"),
                row.get("draws"),
                row.get("losses"),
                row.get("goals_for"),
                row.get("goals_against"),
                row.get("goal_diff"),
                row.get("points"),
                row.get("form_sequence"),
                scraped_at,
            ),
        )


def _insert_recent_match(
    conn: sqlite3.Connection,
    team_id: int,
    scope: str,
    match_url: str,
    result_token: str,
    goals_for,
    goals_against,
    clean_sheet,
    sequence_index: int,
    scraped_at: str,
) -> None:
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO team_recent_matches (
                team_id, scope, match_url, result_token, goals_for, goals_against,
                clean_sheet, sequence_index, scraped_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                team_id,
                scope,
                match_url,
                result_token,
                goals_for,
                goals_against,
                clean_sheet,
                sequence_index,
                scraped_at,
            ),
        )


def _insert_model_features(
    conn: sqlite3.Connection,
    team_id: int,
    league_key: str,
    team_name: str,
    overall_standing: dict,
    overall_form: dict,
    home_form: dict,
    away_form: dict,
    clean_sheets_overall_last5: int,
    scraped_at: str,
) -> None:
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO team_model_features (
                team_id, league_key, team_name, scraped_at,
                rank_overall, points_overall, matches_overall, goals_for_overall,
                goals_against_overall, goal_diff_overall,
                form_overall_last5, wins_overall_last5, draws_overall_last5,
                losses_overall_last5, goals_for_overall_last5, goals_against_overall_last5,
                points_overall_last5, clean_sheets_overall_last5,
                form_home_last5, wins_home_last5, draws_home_last5, losses_home_last5,
                goals_for_home_last5, goals_against_home_last5, points_home_last5,
                form_away_last5, wins_away_last5, draws_away_last5, losses_away_last5,
                goals_for_away_last5, goals_against_away_last5, points_away_last5
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                team_id,
                league_key,
                team_name,
                scraped_at,
                overall_standing.get("rank"),
                overall_standing.get("points"),
                overall_standing.get("matches"),
                overall_standing.get("goals_for"),
                overall_standing.get("goals_against"),
                overall_standing.get("goal_diff"),
                overall_form.get("form_sequence"),
                overall_form.get("wins"),
                overall_form.get("draws"),
                overall_form.get("losses"),
                overall_form.get("goals_for"),
                overall_form.get("goals_against"),
                overall_form.get("points"),
                clean_sheets_overall_last5,
                home_form.get("form_sequence"),
                home_form.get("wins"),
                home_form.get("draws"),
                home_form.get("losses"),
                home_form.get("goals_for"),
                home_form.get("goals_against"),
                home_form.get("points"),
                away_form.get("form_sequence"),
                away_form.get("wins"),
                away_form.get("draws"),
                away_form.get("losses"),
                away_form.get("goals_for"),
                away_form.get("goals_against"),
                away_form.get("points"),
            ),
        )


def _infer_league_from_player_url(player_team_url: str):
    if not player_team_url:
        return None

    m = re.search(r"/Show/([^/]+)", player_team_url)
    if not m:
        return None

    slug = m.group(1)
    country = slug.split("-")[0].lower().strip()
    return COUNTRY_TO_LEAGUE_KEY.get(country)


def _build_player_links(conn: sqlite3.Connection, scraped_at: str, players_db_path: str = PLAYERS_DB_PATH) -> int:
    if not os.path.exists(players_db_path):
        log.warning("Players DB not found at %s. Skipping team-player linking.", players_db_path)
        return 0

    teams_rows = conn.execute(
        """
        SELECT t.id, t.team_name, t.team_url, l.league_key
        FROM teams t
        JOIN leagues l ON l.id = t.league_id
        WHERE t.scraped_at = ?
        """,
        (scraped_at,),
    ).fetchall()

    teams_by_league = {}
    for team_id, team_name, team_url, league_key in teams_rows:
        teams_by_league.setdefault(league_key, []).append(
            {
                "team_id": team_id,
                "team_name": team_name,
                "team_url": team_url,
                "norm_name": _normalize_team_name(team_name),
            }
        )

    linked = 0
    pconn = sqlite3.connect(players_db_path)
    try:
        player_rows = pconn.execute(
            """
            SELECT DISTINCT team_name, team_url
            FROM players
            WHERE team_name IS NOT NULL AND TRIM(team_name) != ''
            """
        ).fetchall()
    finally:
        pconn.close()

    for player_team_name, player_team_url in player_rows:
        league_key = _infer_league_from_player_url(player_team_url)
        candidates = teams_by_league.get(league_key, [])
        if not candidates:
            continue

        norm_player_team = _normalize_team_name(player_team_name)
        match = None
        matched_by = ""

        for cand in candidates:
            if cand["norm_name"] == norm_player_team:
                match = cand
                matched_by = "normalized_exact"
                break

        if not match:
            contains_matches = [
                cand
                for cand in candidates
                if cand["norm_name"] in norm_player_team or norm_player_team in cand["norm_name"]
            ]
            if len(contains_matches) == 1:
                match = contains_matches[0]
                matched_by = "normalized_contains"

        if not match:
            continue

        with conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO team_player_links (
                    team_id, player_team_name, player_team_url,
                    players_db_path, matched_by, scraped_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    match["team_id"],
                    player_team_name,
                    player_team_url,
                    players_db_path,
                    matched_by,
                    scraped_at,
                ),
            )
        linked += 1

    return linked


def scrape_team_recent_form(
    db_path: str = TEAM_FORM_DB_PATH,
    top_n: int = TOP_TEAMS_PER_LEAGUE,
    sample_size: int = RECENT_FORM_SAMPLE_SIZE,
) -> dict:
    scraped_at = datetime.now().strftime("%Y-%m-%d")
    conn = init_db(db_path)
    driver = _make_driver()

    total_teams = 0
    total_links = 0

    try:
        first_page = True

        for league in LEAGUE_STANDINGS:
            league_key = league["league_key"]
            league_name = league["league_name"]
            standings_url = league["standings_overall_url"]

            log.info("Scraping %s (%s)", league_name, league_key)
            league_id = _upsert_league(conn, league_key, league_name, standings_url)

            _safe_get(driver, standings_url)
            if first_page:
                _dismiss_consent(driver)
                first_page = False

            _wait_rows(driver)
            overall_standings_rows = _parse_table_rows(driver)
            if TARGET_TEAMS:
                overall_standings_rows = [
                    row for row in overall_standings_rows if _is_target_team(row["team_name"])
                ]
            elif top_n is not None:
                overall_standings_rows = overall_standings_rows[:top_n]
            if not overall_standings_rows:
                raise RuntimeError(f"No standings rows parsed for {league_name}")

            top_team_keys = {row["team_key"] for row in overall_standings_rows}
            team_ids = {}
            standings_by_team = {}

            for row in overall_standings_rows:
                team_id = _insert_team(conn, league_id, row, scraped_at)
                team_ids[row["team_key"]] = team_id
                standings_by_team[row["team_key"]] = row

            form_urls = _build_form_urls(standings_url, sample_size)

            forms_by_scope = {"overall": {}, "home": {}, "away": {}}
            for scope, scope_url in form_urls.items():
                _safe_get(driver, scope_url)
                _wait_rows(driver)
                scope_rows = _parse_table_rows(driver, allowed_team_keys=top_team_keys)
                for row in scope_rows:
                    forms_by_scope[scope][row["team_key"]] = row
                    _insert_form(conn, team_ids[row["team_key"]], scope, row, scraped_at)

            for team_key in top_team_keys:
                team_id = team_ids[team_key]
                overall_form = forms_by_scope["overall"].get(team_key, {})
                home_form = forms_by_scope["home"].get(team_key, {})
                away_form = forms_by_scope["away"].get(team_key, {})

                clean_sheets = 0
                match_links = overall_form.get("form_links", [])[:sample_size]
                for idx, item in enumerate(match_links, start=1):
                    token = item.get("token")
                    match_url = item.get("url")
                    score_data = _fetch_match_result_selenium(
                        driver, match_url, team_key, result_token=token
                    )

                    if score_data:
                        clean_sheets += score_data["clean_sheet"]
                        goals_for = score_data["goals_for"]
                        goals_against = score_data["goals_against"]
                        clean_sheet = score_data["clean_sheet"]
                    else:
                        goals_for = None
                        goals_against = None
                        clean_sheet = None

                    _insert_recent_match(
                        conn=conn,
                        team_id=team_id,
                        scope="overall_last5",
                        match_url=match_url,
                        result_token=token,
                        goals_for=goals_for,
                        goals_against=goals_against,
                        clean_sheet=clean_sheet,
                        sequence_index=idx,
                        scraped_at=scraped_at,
                    )

                _insert_model_features(
                    conn=conn,
                    team_id=team_id,
                    league_key=league_key,
                    team_name=standings_by_team[team_key]["team_name"],
                    overall_standing=standings_by_team[team_key],
                    overall_form=overall_form,
                    home_form=home_form,
                    away_form=away_form,
                    clean_sheets_overall_last5=clean_sheets,
                    scraped_at=scraped_at,
                )

            total_teams += len(top_team_keys)
            log.info("Finished league %s: %d teams saved.", league_name, len(top_team_keys))

        total_links = _build_player_links(conn=conn, scraped_at=scraped_at, players_db_path=PLAYERS_DB_PATH)

        return {
            "scraped_at": scraped_at,
            "teams_saved": total_teams,
            "player_team_links_saved": total_links,
            "db_path": db_path,
        }

    finally:
        driver.quit()
        conn.close()


if __name__ == "__main__":
    summary = scrape_team_recent_form()
    log.info(
        "Done. Date=%s teams=%d links=%d db=%s",
        summary["scraped_at"],
        summary["teams_saved"],
        summary["player_team_links_saved"],
        summary["db_path"],
    )
