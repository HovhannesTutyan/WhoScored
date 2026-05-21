"""
Understat xG scraper.

Scrapes season-total xG, xGA and xGD for the top-5 teams in each of the
top-5 leagues from Understat.com and stores them as three new columns in
the teams table of team_recent_form.db.

Strategy
--------
Understat injects all team data into the page as a JavaScript variable
(teamsData).  After Selenium renders the page we first try to read that
variable directly from the JS context — it is the most reliable source
because it contains per-match xG values we can aggregate.  If the variable
is absent (e.g. Understat changes their embed), the scraper falls back to
parsing the rendered HTML table, dynamically finding the xG/xGA columns by
their header text.
"""

import logging
import re
import sqlite3
import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

try:
    from .understat_xg_config import (
        LEAGUE_XG,
        TEAM_NAME_ALIASES,
        TEAM_FORM_DB_PATH,
        TARGET_TEAMS,
        TOP_TEAMS_PER_LEAGUE,
        Selectors,
        Timeouts,
    )
except ImportError:
    from understat_xg_config import (
        LEAGUE_XG,
        TEAM_NAME_ALIASES,
        TEAM_FORM_DB_PATH,
        TARGET_TEAMS,
        TOP_TEAMS_PER_LEAGUE,
        Selectors,
        Timeouts,
    )

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def _add_xg_columns(conn: sqlite3.Connection) -> None:
    """Add xg_for / xg_against / xg_diff / xg_scraped_at to teams if absent."""
    existing = {row[1] for row in conn.execute("PRAGMA table_info(teams)").fetchall()}
    with conn:
        for col, coltype in [
            ("xg_for",        "REAL"),
            ("xg_against",    "REAL"),
            ("xg_diff",       "REAL"),
            ("xg_scraped_at", "TEXT"),
        ]:
            if col not in existing:
                conn.execute(f"ALTER TABLE teams ADD COLUMN {col} {coltype}")
                log.info("Added column teams.%s (%s)", col, coltype)


# ---------------------------------------------------------------------------
# Selenium helpers  (same patterns as teamRecentForm.py)
# ---------------------------------------------------------------------------

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
    driver.set_page_load_timeout(Timeouts.PAGE_LOAD)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


def _safe_get(driver: webdriver.Chrome, url: str, attempts: int = 3, wait_after: float = 2.0) -> None:
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
            btn = WebDriverWait(driver, Timeouts.CONSENT_WAIT).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            time.sleep(1.0)
            log.info("Consent banner dismissed.")
            return
        except Exception:
            continue


# ---------------------------------------------------------------------------
# xG extraction helpers
# ---------------------------------------------------------------------------

def _normalize_team_name(name: str) -> str:
    if not name:
        return ""
    n = name.lower().strip()
    n = n.replace(".", " ").replace("-", " ").replace("'", "")
    n = re.sub(r"\s+", " ", n)

    alias = TEAM_NAME_ALIASES.get(n)
    if alias is not None:
        return alias

    # Strip common corporate prefixes that differ between sources
    n = re.sub(r"\b(fc|cf|ac|sc|afc|cfc|u\.?s\.?|s\.s\.c\.)\b", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n


def _is_target_team(team_name: str) -> bool:
    target_names = {_normalize_team_name(name) for name in TARGET_TEAMS}
    return _normalize_team_name(team_name) in target_names


def _extract_xg_from_js(driver: webdriver.Chrome) -> dict:
    """Read teamsData from the JS context and aggregate xG/xGA per team.

    Understat injects ``var teamsData = JSON.parse('...')`` into every league
    page.  Once Selenium has rendered the page the variable is available in
    ``window.teamsData``.

    Returns ``{normalized_name: {xg_for, xg_against, xg_diff, raw_name}}``
    or an empty dict if teamsData is not present.
    """
    try:
        data = driver.execute_script(
            "return typeof teamsData !== 'undefined' ? teamsData : null;"
        )
    except Exception as exc:
        log.debug("execute_script for teamsData failed: %s", exc)
        return {}

    if not data:
        return {}

    result = {}
    for _team_id, team in data.items():
        title = team.get("title", "")
        history = team.get("history", [])
        if not title:
            continue
        try:
            xg  = sum(float(m.get("xG",  0) or 0) for m in history)
            xga = sum(float(m.get("xGA", 0) or 0) for m in history)
        except (ValueError, TypeError) as exc:
            log.debug("Could not parse xG history for '%s': %s", title, exc)
            continue
        norm = _normalize_team_name(title)
        result[norm] = {
            "xg_for":     round(xg, 2),
            "xg_against": round(xga, 2),
            "xg_diff":    round(xg - xga, 2),
            "raw_name":   title,
        }

    return result


def _extract_xg_from_table(driver: webdriver.Chrome) -> dict:
    """Parse the rendered HTML league table to find xG and xGA columns.

    Dynamically reads the header row to locate the xG and xGA column indices
    so the scraper is not tied to a fixed column position.

    Returns ``{normalized_name: {xg_for, xg_against, xg_diff, raw_name}}``
    or an empty dict on failure.
    """
    try:
        WebDriverWait(driver, Timeouts.TABLE_ROWS_WAIT).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Selectors.TABLE_ROWS))
        )
    except TimeoutException:
        log.warning("Table rows did not appear within %ds.", Timeouts.TABLE_ROWS_WAIT)
        return {}

    header_cells = driver.find_elements(By.CSS_SELECTOR, Selectors.TABLE_HEADER_CELLS)
    headers = [th.text.strip() for th in header_cells]
    log.debug("Table headers: %s", headers)

    xg_idx  = next((i for i, h in enumerate(headers) if h == "xG"),  None)
    xga_idx = next((i for i, h in enumerate(headers) if h == "xGA"), None)

    if xg_idx is None or xga_idx is None:
        log.warning(
            "Could not locate xG (idx=%s) or xGA (idx=%s) in headers: %s",
            xg_idx, xga_idx, headers,
        )
        return {}

    result = {}
    rows = driver.find_elements(By.CSS_SELECTOR, Selectors.TABLE_ROWS)
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) <= max(xg_idx, xga_idx):
            continue
        try:
            team_link = row.find_element(By.CSS_SELECTOR, Selectors.TEAM_LINK)
            team_name = team_link.text.strip()
        except Exception:
            continue
        try:
            xg  = float(cells[xg_idx].text.strip()  or 0)
            xga = float(cells[xga_idx].text.strip() or 0)
        except (ValueError, TypeError):
            continue
        norm = _normalize_team_name(team_name)
        result[norm] = {
            "xg_for":     round(xg, 2),
            "xg_against": round(xga, 2),
            "xg_diff":    round(xg - xga, 2),
            "raw_name":   team_name,
        }

    return result


def _fetch_league_xg(driver: webdriver.Chrome, url: str) -> dict:
    """Load one Understat league page and return xG data for all teams."""
    _safe_get(driver, url, wait_after=Timeouts.JS_RENDER_WAIT)
    _dismiss_consent(driver)
    # Give React/JS a moment to finish populating the table and teamsData
    time.sleep(Timeouts.JS_RENDER_WAIT)

    xg_data = _extract_xg_from_js(driver)
    if xg_data:
        log.info("  Extracted %d teams via teamsData JS variable.", len(xg_data))
        return xg_data

    log.info("  teamsData not in JS context — falling back to HTML table.")
    xg_data = _extract_xg_from_table(driver)
    log.info("  Extracted %d teams from HTML table.", len(xg_data))
    return xg_data


# ---------------------------------------------------------------------------
# DB update
# ---------------------------------------------------------------------------

def _match_and_update(
    conn: sqlite3.Connection,
    league_key: str,
    xg_data: dict,
    scraped_at: str,
) -> int:
    """Match Understat teams to DB teams and write xG columns.

    Matching order:
    1. Exact normalized name
    2. One name is a substring of the other (single unambiguous match)

    Returns number of teams updated.
    """
    rows = conn.execute(
        """
        SELECT t.id, t.team_name
        FROM   teams t
        JOIN   leagues l ON t.league_id = l.id
        WHERE  l.league_key = ?
        """,
        (league_key,),
    ).fetchall()

    if not rows:
        log.warning("No DB teams found for league_key=%s", league_key)
        return 0

    updated = 0
    for team_id, db_name in rows:
        if TARGET_TEAMS and not _is_target_team(db_name):
            continue

        db_norm = _normalize_team_name(db_name)

        # 1. Exact normalized match
        matched = xg_data.get(db_norm)
        match_method = "exact"

        # 2. Substring fallback
        if not matched:
            candidates = [
                (xg_norm, vals)
                for xg_norm, vals in xg_data.items()
                if db_norm in xg_norm or xg_norm in db_norm
            ]
            if len(candidates) == 1:
                matched = candidates[0][1]
                match_method = "substring"
                log.debug("  Substring match: '%s' ~ '%s'", db_norm, candidates[0][0])
            elif len(candidates) > 1:
                log.warning(
                    "  Ambiguous substring matches for '%s': %s",
                    db_norm, [c[0] for c in candidates],
                )

        if not matched:
            log.warning(
                "  No xG match for '%s' (norm: '%s') in %s — skipping.",
                db_name, db_norm, league_key,
            )
            continue

        with conn:
            conn.execute(
                """
                UPDATE teams
                SET    xg_for = ?, xg_against = ?, xg_diff = ?, xg_scraped_at = ?
                WHERE  id = ?
                """,
                (
                    matched["xg_for"],
                    matched["xg_against"],
                    matched["xg_diff"],
                    scraped_at,
                    team_id,
                ),
            )
        log.info(
            "  %-25s [%s]  xG=%.2f  xGA=%.2f  xGD=%+.2f  (matched via %s, raw='%s')",
            db_name,
            league_key,
            matched["xg_for"],
            matched["xg_against"],
            matched["xg_diff"],
            match_method,
            matched["raw_name"],
        )
        updated += 1

    return updated


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def scrape_xg(
    db_path: str = TEAM_FORM_DB_PATH,
    top_n: int = TOP_TEAMS_PER_LEAGUE,
) -> dict:
    """Scrape Understat xG data and persist to the teams table.

    Returns a summary dict: scraped_at, teams_updated, db_path.
    """
    scraped_at = str(date.today())
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    _add_xg_columns(conn)

    driver = _make_driver()
    total_updated = 0
    first_page = True

    try:
        for league in LEAGUE_XG:
            log.info("Scraping xG for %s (%s)", league["league_name"], league["league_key"])
            try:
                xg_data = _fetch_league_xg(driver, league["url"])
                if first_page:
                    first_page = False
                if not xg_data:
                    log.warning("No xG data retrieved for %s — skipping.", league["league_name"])
                    continue
                n = _match_and_update(conn, league["league_key"], xg_data, scraped_at)
                log.info("Finished %s: %d teams updated.", league["league_name"], n)
                total_updated += n
            except Exception as exc:
                log.error(
                    "Error scraping xG for %s: %s",
                    league["league_name"], exc, exc_info=True,
                )
    finally:
        driver.quit()
        conn.close()

    log.info(
        "Done. Date=%s  teams_updated=%d  db=%s",
        scraped_at, total_updated, db_path,
    )
    return {
        "scraped_at":    scraped_at,
        "teams_updated": total_updated,
        "db_path":       db_path,
    }


if __name__ == "__main__":
    result = scrape_xg()
    log.info(
        "Result: date=%s  teams_updated=%d  db=%s",
        result["scraped_at"],
        result["teams_updated"],
        result["db_path"],
    )
