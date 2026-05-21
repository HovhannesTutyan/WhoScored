"""
FBref Squad Goalkeeping scraper.

Scrapes the 2025-2026 Squad Goalkeeping table from FBref for all configured
leagues and upserts rows into the `goalkeeper_stats` table in
team_recent_form.db, linked to the `teams` table by team_id FK.

Uses undetected-chromedriver to bypass Cloudflare bot detection, then
BeautifulSoup to parse FBref's HTML-comment-wrapped stats tables.

Usage:
    python scraping/fbrefGoalkeepers.py
"""

import logging
import re
import sqlite3
import sys
import time
import types
import unicodedata
from datetime import date

try:
    import winreg
except ImportError:
    winreg = None

try:
    import distutils.version  # type: ignore
except ModuleNotFoundError:
    class _LooseVersion:
        def __init__(self, vstring: str):
            self.vstring = str(vstring)
            self.version = [
                int(token) if token.isdigit() else token.lower()
                for token in re.split(r"[.\-+_]", self.vstring)
                if token
            ]

        def _cmp_key(self):
            return tuple(
                (0, part) if isinstance(part, int) else (1, part)
                for part in self.version
            )

        def _coerce_other(self, other):
            if isinstance(other, _LooseVersion):
                return other._cmp_key()
            return _LooseVersion(str(other))._cmp_key()

        def __lt__(self, other):
            return self._cmp_key() < self._coerce_other(other)

        def __le__(self, other):
            return self._cmp_key() <= self._coerce_other(other)

        def __eq__(self, other):
            return self._cmp_key() == self._coerce_other(other)

        def __gt__(self, other):
            return self._cmp_key() > self._coerce_other(other)

        def __ge__(self, other):
            return self._cmp_key() >= self._coerce_other(other)

        def __repr__(self):
            return self.vstring

    distutils_module = types.ModuleType("distutils")
    version_module = types.ModuleType("distutils.version")
    version_module.LooseVersion = _LooseVersion
    distutils_module.version = version_module
    sys.modules["distutils"] = distutils_module
    sys.modules["distutils.version"] = version_module

import undetected_chromedriver as uc
from bs4 import BeautifulSoup, Comment
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

try:
    from .fbref_gk_config import (
        LEAGUE_GK, TEAM_NAME_ALIASES, TARGET_TEAMS, DB_PATH, SEASON,
        Selectors, Timeouts,
    )
except ImportError:
    from fbref_gk_config import (
        LEAGUE_GK, TEAM_NAME_ALIASES, TARGET_TEAMS, DB_PATH, SEASON,
        Selectors, Timeouts,
    )
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


# ── Name normalisation ────────────────────────────────────────────────────────

def _strip_accents(text: str) -> str:
    """Remove diacritics: Atlético → atletico, München → munchen."""
    nfkd = unicodedata.normalize("NFD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _normalize_team_name(name: str) -> str:
    if not name:
        return ""
    n = _strip_accents(name).lower().strip()
    n = n.replace(".", " ").replace("-", " ").replace("'", "")
    n = re.sub(r"\s+", " ", n)
    alias = TEAM_NAME_ALIASES.get(n)
    if alias is not None:
        return alias   # return immediately — skip prefix stripping for aliased names
    n = re.sub(r"\b(fc|cf|ac|sc|afc|cfc|u\.?s\.?|s\.s\.c\.)\b", "", n)
    n = re.sub(r"\s+", " ", n).strip()
    return n


def _resolve_team_id(conn: sqlite3.Connection, team_name: str):
    """Return teams.id for team_name (exact then substring match), or None."""
    try:
        rows = conn.execute("SELECT id, team_name FROM teams").fetchall()
    except sqlite3.OperationalError:
        return None
    norm = _normalize_team_name(team_name)
    for tid, tname in rows:
        if _normalize_team_name(tname) == norm:
            return tid
    for tid, tname in rows:
        tn = _normalize_team_name(tname)
        if norm and tn and (norm in tn or tn in norm):
            return tid
    return None


# ── Database ──────────────────────────────────────────────────────────────────

def init_db(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Open (or create) the DB and ensure the goalkeeper_stats table exists."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS goalkeeper_stats (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id         INTEGER REFERENCES teams(id),
                team_name       TEXT    NOT NULL,
                league_name     TEXT    NOT NULL,
                season          TEXT    NOT NULL,
                scraped_at      TEXT    NOT NULL,
                -- Playing time
                games           INTEGER,
                minutes_90s     REAL,
                -- Core GK stats
                ga              INTEGER,
                ga90            REAL,
                sota            INTEGER,
                saves           INTEGER,
                save_pct        REAL,
                cs              INTEGER,
                cs_pct          REAL,
                -- Penalty kicks
                pens_att        INTEGER,
                pens_allowed    INTEGER,
                pens_saved      INTEGER,
                pens_missed     INTEGER,
                pens_save_pct   REAL,
                -- Post-shot xG
                psxg            REAL,
                psxg_per_sot    REAL,
                psxg_net        REAL,
                psxg_net_per90  REAL,
                UNIQUE (team_name, season)
            )
        """)
    log.info("DB ready: %s", db_path)
    return conn


# ── Selenium helpers (undetected-chromedriver bypasses Cloudflare) ────────────

def _detect_chrome_major_version():
    if winreg is None:
        return None

    registry_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome\BLBeacon"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Google\Chrome\BLBeacon"),
    ]

    for hive, path in registry_paths:
        try:
            with winreg.OpenKey(hive, path) as key:
                version, _ = winreg.QueryValueEx(key, "version")
        except OSError:
            continue

        try:
            return int(str(version).split(".", 1)[0])
        except (TypeError, ValueError):
            continue

    return None

def _make_driver() -> uc.Chrome:
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    version_main = _detect_chrome_major_version() or 0
    if version_main:
        log.info("Using Chrome major version %s for undetected-chromedriver", version_main)
    driver = uc.Chrome(options=options, use_subprocess=True, version_main=version_main)
    driver.set_page_load_timeout(Timeouts.PAGE_LOAD)
    return driver


def _safe_get(driver: uc.Chrome, url: str, attempts: int = 3) -> None:
    last_exc = None
    for attempt in range(1, attempts + 1):
        try:
            driver.get(url)
            time.sleep(Timeouts.AFTER_LOAD)
            return
        except (TimeoutException, WebDriverException) as exc:
            last_exc = exc
            log.warning("Attempt %d/%d failed for %s: %s", attempt, attempts, url, exc)
            try:
                driver.execute_script("window.stop();")
            except Exception:
                pass
            time.sleep(2.0)
    raise RuntimeError(f"Failed to load {url} after {attempts} attempts") from last_exc


def _dismiss_consent(driver: uc.Chrome) -> None:
    for xpath in Selectors.CONSENT_BUTTONS_XPATH:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            time.sleep(1.0)
            log.info("Consent banner dismissed.")
            return
        except Exception:
            continue


# ── Table parsing (BeautifulSoup — handles FBref HTML-comment-wrapped tables) ──

def _to_float(val: str):
    v = str(val).strip().replace(",", "")
    if not v or v in ("-", "—", ""):
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _to_int(val: str):
    v = str(val).strip().replace(",", "")
    if not v or v in ("-", "—", ""):
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def _is_target(norm: str) -> bool:
    """True if norm matches any team in TARGET_TEAMS (exact or substring)."""
    for target in TARGET_TEAMS:
        tnorm = _normalize_team_name(target)
        if norm == tnorm:
            return True
    for target in TARGET_TEAMS:
        tnorm = _normalize_team_name(target)
        if norm and tnorm and (norm in tnorm or tnorm in norm):
            return True
    return False


def _find_table_in_source(page_source: str, table_ids: list):
    """Find the goalkeeper stats <table> in page_source.

    FBref wraps stats tables in HTML comments inside wrapper divs, so normal
    Selenium element lookups fail.  We parse the raw source with BeautifulSoup
    which exposes comments, then search inside each comment string.
    """
    soup = BeautifulSoup(page_source, "lxml")

    # Try direct (not commented-out)
    for tid in table_ids:
        tbl = soup.find("table", id=tid)
        if tbl:
            log.info("Found table #%s directly in DOM", tid)
            return tbl

    # FBref hides tables inside HTML comments — search comment nodes
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        for tid in table_ids:
            if f'id="{tid}"' in comment:
                inner = BeautifulSoup(str(comment), "lxml")
                tbl = inner.find("table", id=tid)
                if tbl:
                    log.info("Found table #%s inside HTML comment", tid)
                    return tbl
    return None


def _parse_bs_row(row, stat: str) -> str:
    """Return stripped text of a BeautifulSoup <td> by its data-stat."""
    cell = row.find(["td", "th"], attrs={"data-stat": stat})
    if cell is None:
        return ""
    return cell.get_text(strip=True)


def _parse_league_table(driver: uc.Chrome, league_name: str) -> list:
    """Extract goalkeeper rows for target teams from the current page."""
    source = driver.page_source
    tbl = _find_table_in_source(source, Selectors.TABLE_IDS)

    if tbl is None:
        log.warning("No goalkeeper table found for %s", league_name)
        return []

    results = []
    tbody = tbl.find("tbody")
    if tbody is None:
        log.warning("Table has no <tbody> for %s", league_name)
        return []

    for row in tbody.find_all("tr"):
        row_class = " ".join(row.get("class", []))
        if any(cls in row_class for cls in ("thead", "spacer", "partial_table")):
            continue

        # FBref keeper table uses data-stat="team" for squad name
        squad_raw = _parse_bs_row(row, "team")
        if not squad_raw:
            continue

        norm = _normalize_team_name(squad_raw)
        if not _is_target(norm):
            continue

        # FBref keeper stats use gk_ prefix on most columns
        results.append({
            "squad_raw":      squad_raw,
            "games":          _to_int  (_parse_bs_row(row, "gk_games")),
            "minutes_90s":    _to_float(_parse_bs_row(row, "minutes_90s")),
            "ga":             _to_int  (_parse_bs_row(row, "gk_goals_against")),
            "ga90":           _to_float(_parse_bs_row(row, "gk_goals_against_per90")),
            "sota":           _to_int  (_parse_bs_row(row, "gk_shots_on_target_against")),
            "saves":          _to_int  (_parse_bs_row(row, "gk_saves")),
            "save_pct":       _to_float(_parse_bs_row(row, "gk_save_pct")),
            "cs":             _to_int  (_parse_bs_row(row, "gk_clean_sheets")),
            "cs_pct":         _to_float(_parse_bs_row(row, "gk_clean_sheets_pct")),
            "pens_att":       _to_int  (_parse_bs_row(row, "gk_pens_att")),
            "pens_allowed":   _to_int  (_parse_bs_row(row, "gk_pens_allowed")),
            "pens_saved":     _to_int  (_parse_bs_row(row, "gk_pens_saved")),
            "pens_missed":    _to_int  (_parse_bs_row(row, "gk_pens_missed")),
            "pens_save_pct":  _to_float(_parse_bs_row(row, "gk_pens_save_pct")),
            "psxg":           None,
            "psxg_per_sot":   None,
            "psxg_net":       None,
            "psxg_net_per90": None,
        })
        log.info("  Parsed: '%s'  GA=%s  Save%%=%s  CS=%s  PSxG+/-=%s",
                 squad_raw,
                 results[-1]["ga"],
                 results[-1]["save_pct"],
                 results[-1]["cs"],
                 results[-1]["psxg_net"])

    return results



def _upsert_rows(
    conn: sqlite3.Connection,
    league_name: str,
    season: str,
    scraped_at: str,
    rows: list,
) -> int:
    count = 0
    with conn:
        for r in rows:
            team_id = _resolve_team_id(conn, r["squad_raw"])
            if team_id is None:
                log.info("  team_id=NULL for '%s' (not in top-5 of league)", r["squad_raw"])
            conn.execute("""
                INSERT INTO goalkeeper_stats (
                    team_id, team_name, league_name, season, scraped_at,
                    games, minutes_90s,
                    ga, ga90, sota, saves, save_pct,
                    cs, cs_pct,
                    pens_att, pens_allowed, pens_saved, pens_missed, pens_save_pct,
                    psxg, psxg_per_sot, psxg_net, psxg_net_per90
                ) VALUES (
                    ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?,
                    ?, ?, ?, ?, ?,
                    ?, ?, ?, ?
                )
                ON CONFLICT(team_name, season) DO UPDATE SET
                    team_id        = excluded.team_id,
                    league_name    = excluded.league_name,
                    scraped_at     = excluded.scraped_at,
                    games          = excluded.games,
                    minutes_90s    = excluded.minutes_90s,
                    ga             = excluded.ga,
                    ga90           = excluded.ga90,
                    sota           = excluded.sota,
                    saves          = excluded.saves,
                    save_pct       = excluded.save_pct,
                    cs             = excluded.cs,
                    cs_pct         = excluded.cs_pct,
                    pens_att       = excluded.pens_att,
                    pens_allowed   = excluded.pens_allowed,
                    pens_saved     = excluded.pens_saved,
                    pens_missed    = excluded.pens_missed,
                    pens_save_pct  = excluded.pens_save_pct,
                    psxg           = excluded.psxg,
                    psxg_per_sot   = excluded.psxg_per_sot,
                    psxg_net       = excluded.psxg_net,
                    psxg_net_per90 = excluded.psxg_net_per90
            """, (
                team_id, r["squad_raw"], league_name, season, scraped_at,
                r["games"], r["minutes_90s"],
                r["ga"], r["ga90"], r["sota"], r["saves"], r["save_pct"],
                r["cs"], r["cs_pct"],
                r["pens_att"], r["pens_allowed"], r["pens_saved"],
                r["pens_missed"], r["pens_save_pct"],
                r["psxg"], r["psxg_per_sot"], r["psxg_net"], r["psxg_net_per90"],
            ))
            count += 1
    return count


# ── Entry point ───────────────────────────────────────────────────────────────

def scrape_gk(db_path: str = DB_PATH, season: str = SEASON) -> None:
    conn = init_db(db_path)
    scraped_at = date.today().isoformat()
    total = 0
    failed = []

    try:
        for i, league in enumerate(LEAGUE_GK):
            if i > 0:
                log.info(
                    "Waiting %.0fs before next request (FBref rate limit)...",
                    Timeouts.BETWEEN_REQUESTS,
                )
                time.sleep(Timeouts.BETWEEN_REQUESTS)

            league_name = league["league_name"]
            url = league["url"]
            log.info("── %s ──", league_name)
            log.info("   %s", url)

            success = False
            for attempt in range(1, 4):
                driver = None
                try:
                    log.info("Starting WebDriver for %s (attempt %d/3)...", league_name, attempt)
                    driver = _make_driver()
                    _safe_get(driver, url)
                    _dismiss_consent(driver)

                    try:
                        WebDriverWait(driver, Timeouts.TABLE_WAIT).until(
                            lambda d: any(
                                f'id="{tid}"' in d.page_source
                                for tid in Selectors.TABLE_IDS
                            )
                        )
                    except TimeoutException:
                        title = driver.title or ""
                        raise RuntimeError(
                            f"Basic keeper table not found for {league_name}; page title: {title}"
                        )

                    rows = _parse_league_table(driver, league_name)
                    if not rows:
                        raise RuntimeError(f"No target goalkeeper rows parsed for {league_name}")

                    n = _upsert_rows(conn, league_name, season, scraped_at, rows)
                    total += n
                    log.info("Upserted %d rows for %s", n, league_name)
                    success = True
                    break

                except Exception:
                    log.exception("Error scraping %s (attempt %d/3)", league_name, attempt)
                finally:
                    if driver is not None:
                        try:
                            driver.quit()
                        except Exception:
                            pass

                time.sleep(2.0)

            if not success:
                failed.append(league_name)
    finally:
        conn.close()

    log.info("Scrape complete. Total rows upserted: %d", total)
    if failed:
        log.error("Failed leagues: %s", ", ".join(failed))


if __name__ == "__main__":
    scrape_gk()
