"""
Unified WhoScored team scraper.

Scrapes the Summary and Defensive stat tabs for any team and upserts all
player rows into a local SQLite database (players.db in the project root).

Usage (CLI):
    python scraping/scraper.py                          # default: Bayer Leverkusen
    python scraping/scraper.py 36 Germany-Bayer-Leverkusen "Bayer Leverkusen"
    python scraping/scraper.py --debug                  # saves screenshot + page source on error

Usage (import):
    from scraping.scraper import scrape_team
    scrape_team(team_id=36, team_slug="Germany-Bayer-Leverkusen", team_name="Bayer Leverkusen")
"""

import os
import sys
import time
import logging
import sqlite3
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

try:
    from .config import IDs, Selectors, ColumnIndex, Timeouts, BASE_TEAM_URL
except ImportError:
    from config import IDs, Selectors, ColumnIndex, Timeouts, BASE_TEAM_URL

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

DB_PATH = "players.db"

# ── Database ──────────────────────────────────────────────────────────────────

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Create (or open) the players database and ensure the schema exists."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name           TEXT    NOT NULL,
                team_url            TEXT    NOT NULL,
                scraped_at          TEXT    NOT NULL,
                name                TEXT    NOT NULL,
                age                 TEXT,
                position            TEXT,
                height              TEXT,
                weight              TEXT,
                appearances         INTEGER,
                min_played          INTEGER,
                goals               INTEGER,
                assists             INTEGER,
                yellow_cards        INTEGER,
                red_cards           INTEGER,
                shots_per_game      REAL,
                pass_success        TEXT,
                aerial_won_per_game REAL,
                man_of_the_match    INTEGER,
                tackles             REAL,
                interceptions       REAL,
                fouls               REAL,
                offsides            REAL,
                clearances          REAL,
                dribbled_past       REAL,
                blocks              REAL,
                own_goals           INTEGER,
                rating              REAL,
                UNIQUE (team_url, name, scraped_at)
            )
        """)
    return conn


# ── Browser ───────────────────────────────────────────────────────────────────

def _make_driver() -> webdriver.Chrome:
    """Return a Chrome WebDriver with bot-detection mitigations applied."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"},
    )
    return driver


# ── Cookie / consent wall ─────────────────────────────────────────────────────

def _dismiss_consent(driver: webdriver.Chrome, timeout: int = None) -> bool:
    """Try every known consent-wall selector. Returns True if one was clicked."""
    if timeout is None:
        timeout = Timeouts.CONSENT_BANNER
    
    for by, selector in Selectors.CONSENT_BUTTONS:
        try:
            btn = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, selector))
            )
            btn.click()
            log.info("Dismissed consent banner via: %s = %s", by, selector)
            time.sleep(2)
            return True
        except (TimeoutException, NoSuchElementException):
            continue
    log.info("No consent banner detected (or already dismissed)")
    return False


# ── Helpers ───────────────────────────────────────────────────────────────────

def _cell_text(cell, xpath: str = None) -> str:
    try:
        if xpath:
            return cell.find_element(By.XPATH, xpath).text.strip()
        return cell.text.strip()
    except Exception:
        return ""


def _rows_loaded(driver: webdriver.Chrome, tbody_id: str = None, min_rows: int = 1) -> bool:
    """Return True when tbody contains at least min_rows <tr> elements."""
    if tbody_id is None:
        tbody_id = IDs.STATS_TABLE_BODY
    try:
        tbody = driver.find_element(By.ID, tbody_id)
        return len(tbody.find_elements(By.TAG_NAME, "tr")) >= min_rows
    except NoSuchElementException:
        return False


def _wait_for_rows(driver: webdriver.Chrome, tbody_id: str = None,
                   timeout: int = None, min_rows: int = 1) -> None:
    """Block until the tbody has at least min_rows rows, or raise TimeoutException."""
    if tbody_id is None:
        tbody_id = IDs.STATS_TABLE_BODY
    if timeout is None:
        timeout = Timeouts.WAIT_DEFAULT
    
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _rows_loaded(driver, tbody_id, min_rows):
            return
        time.sleep(1)
    raise TimeoutException(
        f"Timed out waiting for {min_rows}+ rows in #{tbody_id}"
    )


def _save_debug(driver: webdriver.Chrome, label: str) -> None:
    """Save a screenshot and page source for post-mortem analysis."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shot = f"debug_{label}_{ts}.png"
    src  = f"debug_{label}_{ts}.html"
    driver.save_screenshot(shot)
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(driver.page_source)
    log.info("Debug files saved: %s  %s", shot, src)


# ── Tab scrapers ──────────────────────────────────────────────────────────────

def _scrape_summary_tab(driver: webdriver.Chrome, debug: bool = False) -> list:
    _wait_for_rows(driver, timeout=30, min_rows=1)
    tbody = driver.find_element(By.ID, IDs.STATS_TABLE_BODY)
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    results = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 15:
            continue
        # Name is inside the first cell's iconize span
        try:
            name = cells[ColumnIndex.SUMMARY_NAME_AGE_POS].find_element(By.CSS_SELECTOR, Selectors.PLAYER_NAME).text.strip()
        except Exception:
            name = ""
        if not name:
            continue
        position_raw = _cell_text(cells[ColumnIndex.SUMMARY_NAME_AGE_POS], "./span/span[2]")
        results.append({
            "name":                name,
            "age":                 _cell_text(cells[ColumnIndex.SUMMARY_NAME_AGE_POS], "./span/span[1]"),
            "position":            position_raw.lstrip(", "),
            "height":              _cell_text(cells[ColumnIndex.SUMMARY_HEIGHT]),
            "weight":              _cell_text(cells[ColumnIndex.SUMMARY_WEIGHT]),
            "appearances":         _cell_text(cells[ColumnIndex.SUMMARY_APPEARANCES]),
            "min_played":          _cell_text(cells[ColumnIndex.SUMMARY_MIN_PLAYED]),
            "goals":               _cell_text(cells[ColumnIndex.SUMMARY_GOALS]),
            "assists":             _cell_text(cells[ColumnIndex.SUMMARY_ASSISTS]),
            "yellow_cards":        _cell_text(cells[ColumnIndex.SUMMARY_YELLOW_CARDS]),
            "red_cards":           _cell_text(cells[ColumnIndex.SUMMARY_RED_CARDS]),
            "shots_per_game":      _cell_text(cells[ColumnIndex.SUMMARY_SHOTS_PER_GAME]),
            "pass_success":        _cell_text(cells[ColumnIndex.SUMMARY_PASS_SUCCESS]),
            "aerial_won_per_game": _cell_text(cells[ColumnIndex.SUMMARY_AERIAL_WON_PER_GAME]),
            "man_of_the_match":    _cell_text(cells[ColumnIndex.SUMMARY_MAN_OF_THE_MATCH]),
            "rating":              _cell_text(cells[ColumnIndex.SUMMARY_RATING]),
        })
    log.info("Summary tab: %d players found", len(results))
    if debug and len(results) == 0:
        _save_debug(driver, "summary_empty")
    return results


def _scrape_defensive_tab(driver: webdriver.Chrome, wait: WebDriverWait,
                           debug: bool = False) -> list:
    # Try multiple selectors for the Defensive tab link
    tab = None
    for by, sel in Selectors.DEFENSIVE_TAB:
        try:
            tab = wait.until(EC.element_to_be_clickable((by, sel)))
            log.info("Found defensive tab via: %s = %s", by, sel)
            break
        except TimeoutException:
            continue

    if tab is None:
        if debug:
            _save_debug(driver, "defensive_tab_not_found")
        raise RuntimeError(
            "Could not locate the Defensive tab. "
            "The page structure may have changed. "
            "Run with --debug to save a screenshot."
        )

    # Scroll the tab into view and click
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", tab)
    time.sleep(Timeouts.TAB_CLICK)
    try:
        tab.click()
    except Exception:
        driver.execute_script("arguments[0].click();", tab)

    # Wait for defensive rows
    _wait_for_rows(driver, timeout=Timeouts.DEFENSIVE_TAB, min_rows=1)
    time.sleep(1)

    # The defensive table reuses the same tbody id; grab rows from the
    # visible container if it exists, otherwise fall back to the shared id.
    try:
        container = driver.find_element(By.ID, IDs.DEFENSIVE_STATS_CONTAINER)
        tbody = container.find_element(By.ID, IDs.STATS_TABLE_BODY)
    except NoSuchElementException:
        tbody = driver.find_element(By.ID, IDs.STATS_TABLE_BODY)

    rows = tbody.find_elements(By.TAG_NAME, "tr")
    results = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) < 14:
            continue
        try:
            name = cells[ColumnIndex.DEFENSIVE_NAME_AGE_POS].find_element(By.CSS_SELECTOR, Selectors.PLAYER_NAME).text.strip()
        except Exception:
            name = ""
        if not name:
            continue
        results.append({
            "name":          name,
            "tackles":       _cell_text(cells[ColumnIndex.DEFENSIVE_TACKLES]),
            "interceptions": _cell_text(cells[ColumnIndex.DEFENSIVE_INTERCEPTIONS]),
            "fouls":         _cell_text(cells[ColumnIndex.DEFENSIVE_FOULS]),
            "offsides":      _cell_text(cells[ColumnIndex.DEFENSIVE_OFFSIDES]),
            "clearances":    _cell_text(cells[ColumnIndex.DEFENSIVE_CLEARANCES]),
            "dribbled_past": _cell_text(cells[ColumnIndex.DEFENSIVE_DRIBBLED_PAST]),
            "blocks":        _cell_text(cells[ColumnIndex.DEFENSIVE_BLOCKS]),
            "own_goals":     _cell_text(cells[ColumnIndex.DEFENSIVE_OWN_GOALS]),
        })
    log.info("Defensive tab: %d players found", len(results))
    if debug and len(results) == 0:
        _save_debug(driver, "defensive_empty")
    return results


# ── Type coercions ────────────────────────────────────────────────────────────

def _to_int(val: str):
    try:
        return int(str(val).replace(",", "").strip()) if val else None
    except ValueError:
        return None


def _to_float(val: str):
    try:
        return float(str(val).replace("%", "").replace(",", "").strip()) if val else None
    except ValueError:
        return None


# ── Public API ────────────────────────────────────────────────────────────────

def scrape_team(
    team_id: int,
    team_slug: str,
    team_name: str,
    db_path: str = DB_PATH,
    debug: bool = False,
) -> int:
    """
    Scrape Summary + Defensive tabs for a WhoScored team and upsert into SQLite.

    Args:
        team_id:   WhoScored numeric team ID   (e.g. 36 for Bayer Leverkusen)
        team_slug: URL slug                    (e.g. 'Germany-Bayer-Leverkusen')
        team_name: Human-readable name stored in DB
        db_path:   Path to the SQLite file (created if it does not exist)
        debug:     If True, saves screenshots + page source on failures

    Returns:
        Number of player rows upserted.
    """
    url = BASE_TEAM_URL.format(team_id=team_id, team_slug=team_slug)
    scraped_at = datetime.now().strftime("%Y-%m-%d")

    conn = init_db(db_path)
    driver = _make_driver()
    try:
        log.info("Opening %s", url)
        driver.get(url)
        wait = WebDriverWait(driver, Timeouts.WAIT_DEFAULT)

        # Step 1: dismiss cookie / consent wall before anything else
        _dismiss_consent(driver)

        # Step 2: wait for the squad stats section to be present
        try:
            wait.until(EC.presence_of_element_located((By.ID, IDs.STATS_TABLE_BODY)))
        except TimeoutException:
            if debug:
                _save_debug(driver, "no_stats_table")
            raise RuntimeError(
                "Stats table not found — the page may be behind a wall or the "
                "team URL may have changed. Run with --debug to capture the page."
            )

        # Step 3: scroll to the table so lazy-loaded content renders
        try:
            stats_section = driver.find_element(By.ID, IDs.STATS_TABLE_BODY)
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", stats_section)
        except NoSuchElementException:
            pass
        time.sleep(Timeouts.TABLE_SCROLL)

        summary_rows = _scrape_summary_tab(driver, debug=debug)

        if len(summary_rows) == 0:
            if debug:
                _save_debug(driver, "summary_zero_after_scroll")
            raise RuntimeError(
                "Summary tab returned 0 players. "
                "The table may still be behind an overlay or the selector is stale. "
                "Run with --debug to capture the page."
            )

        defensive_rows = _scrape_defensive_tab(driver, wait, debug=debug)

        # Merge by player name
        defensive_map = {r["name"]: r for r in defensive_rows}

        records = []
        for s in summary_rows:
            d = defensive_map.get(s["name"], {})
            records.append((
                team_name,
                url,
                scraped_at,
                s.get("name"),
                s.get("age") or None,
                s.get("position") or None,
                s.get("height") or None,
                s.get("weight") or None,
                _to_int(s.get("appearances")),
                _to_int(s.get("min_played")),
                _to_int(s.get("goals")),
                _to_int(s.get("assists")),
                _to_int(s.get("yellow_cards")),
                _to_int(s.get("red_cards")),
                _to_float(s.get("shots_per_game")),
                s.get("pass_success") or None,
                _to_float(s.get("aerial_won_per_game")),
                _to_int(s.get("man_of_the_match")),
                _to_float(d.get("tackles")),
                _to_float(d.get("interceptions")),
                _to_float(d.get("fouls")),
                _to_float(d.get("offsides")),
                _to_float(d.get("clearances")),
                _to_float(d.get("dribbled_past")),
                _to_float(d.get("blocks")),
                _to_int(d.get("own_goals")),
                _to_float(s.get("rating")),
            ))

        sql = """
            INSERT OR REPLACE INTO players (
                team_name, team_url, scraped_at,
                name, age, position, height, weight,
                appearances, min_played, goals, assists,
                yellow_cards, red_cards, shots_per_game, pass_success,
                aerial_won_per_game, man_of_the_match,
                tackles, interceptions, fouls, offsides,
                clearances, dribbled_past, blocks, own_goals,
                rating
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        with conn:
            conn.executemany(sql, records)

        log.info("Upserted %d players for '%s'", len(records), team_name)
        return len(records)

    except Exception:
        if debug:
            try:
                _save_debug(driver, "fatal_error")
            except Exception:
                pass
        raise

    finally:
        driver.quit()
        conn.close()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--debug"]
    debug_flag = "--debug" in sys.argv

    if len(args) == 3:
        scrape_team(
            team_id=int(args[0]),
            team_slug=args[1],
            team_name=args[2],
            debug=debug_flag,
        )
    else:
        # Default: Bayer Leverkusen
        scrape_team(
            team_id=36,
            team_slug="Germany-Bayer-Leverkusen",
            team_name="Bayer Leverkusen",
            debug=debug_flag,
        )
