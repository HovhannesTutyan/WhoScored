PLAYER_IMPACT_WEIGHTS = {
    "attack": {
        "goals": 0.45,
        "assists": 0.30,
        "shots_per_game": 0.10,
        "dribbles": 0.10,
        "aerial_won_per_game": 0.05,
    },
    "defense": {
        "tackles": 0.35,
        "aerial_won_per_game": 0.20,
        "fouls": -0.15,
        "cards": -0.15,
    },
    "goalkeeper": {
        "saves": 0.40,
        "goals_conceded": -0.40,
    },
    "discipline": {
        "cards": -0.50,
        "fouls": -0.30,
        "offsides": -0.20,
    },
}

TEAM_STRENGTH_WEIGHTS = {
    "points_per_game": 0.20,
    "goal_difference": 0.20,
    "xg_difference": 0.25,
    "attacking": 0.15,
    "defensive": 0.15,
    "player_impact": 0.05,
}

POWER_RATING_WEIGHTS = {
    "elo": 0.30,
    "xg_rating": 0.30,
    "goal_difference_rating": 0.20,
    "player_rating": 0.10,
    "defensive_rating": 0.10,
}

BLENDED_POISSON_WEIGHTS = {
    "goals": 0.45,
    "xg": 0.55,
}

ENSEMBLE_MODEL_WEIGHTS = {
    "poisson": 0.20,
    "xg_poisson": 0.25,
    "blended_poisson": 0.25,
    "team_strength": 0.15,
    "player_impact": 0.10,
    "power_rating": 0.05,
}

DEFAULT_MAX_GOALS = 6
DEFAULT_OVER_UNDER_LINES = (0.5, 1.5, 2.5, 3.5)
DEFAULT_SIMULATION_RUNS = 100000
MIN_SIMULATION_RUNS = 1000
MAX_SIMULATION_RUNS = 200000

CONFIDENCE_LOW_THRESHOLD = 45
CONFIDENCE_HIGH_THRESHOLD = 70

REGRESSION_THRESHOLDS = {
    "finishing_overperformance": 4.0,
    "finishing_underperformance": -4.0,
    "defensive_overperformance": 4.0,
    "defensive_underperformance": -4.0,
}

STRENGTH_THRESHOLDS = {
    "elite_attack": 1.3,
    "weak_attack": 0.9,
    "strong_defense": 0.9,
    "weak_defense": 1.1,
    "strong_xg_profile": 1.15,
    "poor_xg_profile": 0.9,
    "discipline_risk": -1.0,
    "goalkeeper_strength": 0.5,
    "goalkeeper_weakness": -0.5,
}
