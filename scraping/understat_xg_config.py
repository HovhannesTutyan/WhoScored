"""
Understat xG scraper configuration.

Covers the same top-5 leagues and top-5 teams per league as teamRecentForm.
xG, xGA and xGD (season totals) are written into the teams table of
team_recent_form.db.
"""

try:
    from .config import TARGET_TEAMS
except ImportError:
    from config import TARGET_TEAMS

TEAM_FORM_DB_PATH = "team_recent_form.db"
TOP_TEAMS_PER_LEAGUE = 5

# Understat league URLs — season 2025/26 (year = start of season)
LEAGUE_XG = [
    {
        "league_key": "laliga",
        "league_name": "LaLiga",
        "url": "https://understat.com/league/La_liga/2025",
    },
    {
        "league_key": "premier_league",
        "league_name": "Premier League",
        "url": "https://understat.com/league/EPL/2025",
    },
    {
        "league_key": "serie_a",
        "league_name": "Serie A",
        "url": "https://understat.com/league/Serie_A/2025",
    },
    {
        "league_key": "bundesliga",
        "league_name": "Bundesliga",
        "url": "https://understat.com/league/Bundesliga/2025",
    },
    {
        "league_key": "ligue_1",
        "league_name": "Ligue 1",
        "url": "https://understat.com/league/Ligue_1/2025",
    },
]

# Aliases applied BEFORE the generic prefix-strip regex.
# Keys are already-lowercased / dot-replaced forms; values are the canonical
# normalized name that matches what _normalize_team_name() produces for our
# DB team names.
TEAM_NAME_ALIASES = {
    # DB side (Soccerway short names)
    "atl madrid":               "atletico madrid",
    "psg":                      "paris saint germain",
    "paris sg":                 "paris saint germain",
    "manchester utd":           "manchester united",
    "man utd":                  "manchester united",
    "man city":                 "manchester city",
    "bayern munchen":           "bayern munich",
    # Understat full names → DB canonical form
    "atletico de madrid":       "atletico madrid",
    "atletico madrid":          "atletico madrid",
    "real betis balompie":      "betis",
    "real betis":               "betis",
    "borussia dortmund":        "dortmund",
    "vfb stuttgart":            "stuttgart",
    "as roma":                  "roma",
    "tsg hoffenheim":           "hoffenheim",
    "tsg 1899 hoffenheim":      "hoffenheim",
    "inter milan":              "inter",
    "fc internazionale":        "inter",
    "internazionale":           "inter",
    "rc lens":                  "lens",
    "losc lille":               "lille",
    "lille osc":                "lille",
    "olympique lyonnais":       "lyon",
    "olympique de marseille":   "marseille",
    "paris saint-germain":      "paris saint germain",
    "paris saint germain":      "paris saint germain",
    "fc bayern":                "bayern munich",
    "fc bayern munchen":        "bayern munich",
    "como 1907":                "como",
    "rasenballsport leipzig":   "rb leipzig",
    "rasen ball sport leipzig": "rb leipzig",
    "leipzig":                  "rb leipzig",
}


class Timeouts:
    PAGE_LOAD = 30        # driver.set_page_load_timeout seconds
    TABLE_ROWS_WAIT = 15  # WebDriverWait seconds for first tbody tr
    CONSENT_WAIT = 5      # WebDriverWait seconds for consent button
    JS_RENDER_WAIT = 3.0  # flat sleep after page load for JS to finish


class Selectors:
    TABLE_ROWS = "table tbody tr"
    TABLE_HEADER_CELLS = "table thead tr th"
    TEAM_LINK = "td a"
    CONSENT_BUTTONS_XPATH = [
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
        "//button[@id='onetrust-accept-btn-handler']",
        "//button[contains(@class, 'accept')]",
    ]
