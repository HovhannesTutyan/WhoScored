"""
WhoScored scraper configuration: URLs, selectors, and DOM structure.
"""

from selenium.webdriver.common.by import By

# ── URLs ──────────────────────────────────────────────────────────────────────

BASE_TEAM_URL = "https://www.whoscored.com/Teams/{team_id}/Show/{team_slug}"

# ── DOM Structure & Selectors ─────────────────────────────────────────────────

class IDs:
    """HTML element IDs used throughout the page."""
    STATS_TABLE_BODY = "player-table-statistics-body"
    SQUAD_STATS_OPTIONS = "team-squad-stats-options"
    DEFENSIVE_STATS_CONTAINER = "team-squad-stats-defensive"


class Selectors:
    """CSS Selectors and XPaths for navigating the page."""
    
    # Consent banner / cookie wall (tried in order)
    CONSENT_BUTTONS = [
        (By.ID,         "onetrust-accept-btn-handler"),
        (By.ID,         "accept-choices"),
        (By.XPATH,      "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept all')]"),
        (By.XPATH,      "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'i agree')]"),
        (By.XPATH,      "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'agree')]"),
        (By.CSS_SELECTOR, ".qc-cmp2-summary-buttons button:last-child"),
        (By.CSS_SELECTOR, "button.fc-cta-consent"),
    ]
    
    # Defensive tab (tried in order)
    DEFENSIVE_TAB = [
        (By.XPATH,       '//*[@id="team-squad-stats-options"]/li[2]/a'),
        (By.CSS_SELECTOR, '#team-squad-stats-options li:nth-child(2) a'),
        (By.XPATH,       '//ul[@id="team-squad-stats-options"]//a[contains(text(),"Defensive")]'),
    ]
    
    # Player name (inside player link - matches both iconize and iconize-icon-left)
    PLAYER_NAME = "span.iconize"


# ── Table Column Layouts ──────────────────────────────────────────────────────

class ColumnIndex:
    """0-indexed column positions in player tables."""
    
    # Summary tab columns (current layout as of 2026)
    # Note: Shirt number is now embedded in the first cell as a ranking
    SUMMARY_NAME_AGE_POS = 0      # Player name, age, position (ranking inside this cell)
    SUMMARY_GHOST_CELL = 1         # Ghost cell (duplicate data for display purposes)
    SUMMARY_HEIGHT = 2
    SUMMARY_WEIGHT = 3
    SUMMARY_APPEARANCES = 4
    SUMMARY_MIN_PLAYED = 5
    SUMMARY_GOALS = 6
    SUMMARY_ASSISTS = 7
    SUMMARY_YELLOW_CARDS = 8
    SUMMARY_RED_CARDS = 9
    SUMMARY_SHOTS_PER_GAME = 10
    SUMMARY_PASS_SUCCESS = 11
    SUMMARY_AERIAL_WON_PER_GAME = 12
    SUMMARY_MAN_OF_THE_MATCH = 13
    SUMMARY_RATING = 14
    
    # Defensive tab columns (current layout as of 2026)
    DEFENSIVE_NAME_AGE_POS = 0     # Player name, age, position
    DEFENSIVE_GHOST_CELL = 1       # Ghost cell
    DEFENSIVE_HEIGHT = 2           # (skipped)
    DEFENSIVE_WEIGHT = 3           # (skipped)
    DEFENSIVE_APPEARANCES = 4      # (skipped)
    DEFENSIVE_MIN_PLAYED = 5       # (skipped)
    DEFENSIVE_TACKLES = 6
    DEFENSIVE_INTERCEPTIONS = 7
    DEFENSIVE_FOULS = 8
    DEFENSIVE_OFFSIDES = 9
    DEFENSIVE_CLEARANCES = 10
    DEFENSIVE_DRIBBLED_PAST = 11
    DEFENSIVE_BLOCKS = 12
    DEFENSIVE_OWN_GOALS = 13
    DEFENSIVE_RATING = 14          # (skipped — already captured in summary)


# ── Timeouts ──────────────────────────────────────────────────────────────────

class Timeouts:
    """Wait timeouts (in seconds) for various page operations."""
    CONSENT_BANNER = 10
    WAIT_DEFAULT = 30
    DEFENSIVE_TAB = 20
    TABLE_SCROLL = 3
    TAB_CLICK = 1
