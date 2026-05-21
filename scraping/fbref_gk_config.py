"""FBref Squad Goalkeeping scraper configuration."""

DB_PATH = "team_recent_form.db"
SEASON = "2025-2026"

LEAGUE_GK = [
    {
        "league_key": "premier_league",
        "league_name": "Premier League",
        "url": "https://fbref.com/en/comps/9/keepers/Premier-League-Stats",
    },
    {
        "league_key": "serie_a",
        "league_name": "Serie A",
        "url": "https://fbref.com/en/comps/11/keepers/Serie-A-Stats",
    },
    {
        "league_key": "laliga",
        "league_name": "La Liga",
        "url": "https://fbref.com/en/comps/12/keepers/La-Liga-Stats",
    },
    {
        "league_key": "ligue_1",
        "league_name": "Ligue 1",
        "url": "https://fbref.com/en/comps/13/keepers/Ligue-1-Stats",
    },
    {
        "league_key": "bundesliga",
        "league_name": "Bundesliga",
        "url": "https://fbref.com/en/comps/20/keepers/Bundesliga-Stats",
    },
]

TARGET_TEAMS = {
    "Bayern Munich",
    "RB Leipzig",
    "Borussia Dortmund",
    "VfB Stuttgart",
    "Bayer Leverkusen",
    "Barcelona",
    "Real Madrid",
    "Real Betis",
    "Atletico Madrid",
    "Villarreal",
    "Arsenal",
    "Manchester City",
    "Manchester United",
    "Everton",
    "Liverpool",
    "Paris Saint-Germain",
    "Como",
    "Inter",
    "Roma",
}

TEAM_NAME_ALIASES = {
    "paris s-g": "paris saint germain",
    "paris sg": "paris saint germain",
    "paris saint-germain": "paris saint germain",
    "paris saint germain": "paris saint germain",
    "psg": "paris saint germain",
    "manchester utd": "manchester united",
    "man utd": "manchester united",
    "man city": "manchester city",
    "borussia dortmund": "dortmund",
    "dortmund": "dortmund",
    "vfb stuttgart": "stuttgart",
    "tsg hoffenheim": "hoffenheim",
    "1899 hoffenheim": "hoffenheim",
    "tsg 1899 hoffenheim": "hoffenheim",
    "bayer leverkusen": "bayer leverkusen",
    "leverkusen": "bayer leverkusen",
    "rb leipzig": "rb leipzig",
    "rasenballsport leipzig": "rb leipzig",
    "fc bayern munich": "bayern munich",
    "fc bayern munchen": "bayern munich",
    "bayern munchen": "bayern munich",
    "atl madrid": "atletico madrid",
    "atletico madrid": "atletico madrid",
    "atletico de madrid": "atletico madrid",
    "atl  madrid": "atletico madrid",
    "real betis balompie": "betis",
    "real betis": "betis",
    "betis": "betis",
    "as roma": "roma",
    "inter milan": "inter",
    "internazionale": "inter",
    "fc internazionale": "inter",
    "como 1907": "como",
    "fc barcelona": "barcelona",
    "paris fc": "paris fc",
}


class Timeouts:
    PAGE_LOAD = 30
    TABLE_WAIT = 20
    BETWEEN_REQUESTS = 5.0
    AFTER_LOAD = 3.0


class Selectors:
    TABLE_IDS = [
        "stats_squads_keeper_for",
        "stats_squads_keeper",
    ]
    CONSENT_BUTTONS_XPATH = [
        "//button[@id='onetrust-accept-btn-handler']",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept all')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'i agree')]",
        "//button[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'agree')]",
    ]
