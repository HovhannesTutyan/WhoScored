"""
Soccerway team recent-form scraper configuration.
"""

try:
    from .config import TARGET_TEAMS
except ImportError:
    from config import TARGET_TEAMS

BASE_URL = "https://www.soccerway.com"
TOP_TEAMS_PER_LEAGUE = 5
RECENT_FORM_SAMPLE_SIZE = 5
TEAM_FORM_DB_PATH = "team_recent_form.db"
PLAYERS_DB_PATH = "players.db"
REQUEST_TIMEOUT = 25

LEAGUE_STANDINGS = [
    {
        "league_key": "laliga",
        "league_name": "LaLiga",
        "standings_overall_url": "https://www.soccerway.com/spain/laliga/standings/vcm2MhGk/standings/overall/",
    },
    {
        "league_key": "premier_league",
        "league_name": "Premier League",
        "standings_overall_url": "https://www.soccerway.com/england/premier-league/standings/OEEq9Yvp/standings/overall/",
    },
    {
        "league_key": "serie_a",
        "league_name": "Serie A",
        "standings_overall_url": "https://www.soccerway.com/italy/serie-a/standings/6PWwAsA7/standings/overall/",
    },
    {
        "league_key": "bundesliga",
        "league_name": "Bundesliga",
        "standings_overall_url": "https://www.soccerway.com/germany/bundesliga/standings/8UYeqfiD/standings/overall/",
    },
    {
        "league_key": "ligue_1",
        "league_name": "Ligue 1",
        "standings_overall_url": "https://www.soccerway.com/france/ligue-1/standings/j9QeTLPP/standings/overall/",
    },
]

COUNTRY_TO_LEAGUE_KEY = {
    "spain": "laliga",
    "england": "premier_league",
    "italy": "serie_a",
    "germany": "bundesliga",
    "france": "ligue_1",
}

TEAM_NAME_ALIASES = {
    "paris sg": "paris saint germain",
    "psg": "paris saint germain",
    "atl madrid": "atletico madrid",
    "athletic club": "ath bilbao",
    "inter milan": "inter",
    "man utd": "manchester united",
    "manchester utd": "manchester united",
    "man city": "manchester city",
    "borussia dortmund": "dortmund",
    "dortmund": "dortmund",
    "bayern munchen": "bayern munich",
    "vfb stuttgart": "stuttgart",
    "stuttgart": "stuttgart",
    "real betis": "betis",
    "betis": "betis",
    "as roma": "roma",
    "koln": "koln",
    "st etienne": "saint etienne",
}


class Timeouts:
    PAGE_LOAD = 30
    ROWS_WAIT = 30


class Selectors:
    CONSENT_BUTTONS_XPATH = [
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'i agree')]",
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'agree')]",
    ]
    ROWS = ".ui-table__row"
    CELLS = ":scope > div.table__cell"
    TEAM_LINK = "a.tableCellParticipant__name"
    FORM_LINKS = "div.table__cell--form a"
