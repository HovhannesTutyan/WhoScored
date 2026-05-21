from __future__ import annotations

import itertools

from apps.players.models import Player
from apps.teams.models import GoalkeeperStat, Team

_team_counter = itertools.count(1)
_player_counter = itertools.count(1)


def create_team(name: str | None = None, **overrides) -> Team:
    index = next(_team_counter)
    defaults = {
        "name": name or f"Team {index}",
        "league_name": "Premier League",
        "matches_overall": 20,
        "wins_overall": 12,
        "draws_overall": 4,
        "losses_overall": 4,
        "goals_for_overall": 36,
        "goals_against_overall": 20,
        "points_overall": 40,
        "xg_for": 32.0,
        "xg_against": 22.0,
    }
    defaults.update(overrides)
    return Team.objects.create(**defaults)


def create_player(team: Team, name: str | None = None, **overrides) -> Player:
    index = next(_player_counter)
    defaults = {
        "team": team,
        "name": name or f"Player {index}",
        "goals": 5,
        "assists": 3,
        "cards": 2,
        "shots_per_game": 1.5,
        "aerial_won_per_game": 1.2,
        "tackles": 1.4,
        "fouls": 0.8,
        "offsides": 0.3,
        "dribbles": 1.1,
        "goals_conceded": 0.0,
        "saves": 0.0,
    }
    defaults.update(overrides)
    return Player.objects.create(**defaults)


def create_goalkeeper_stat(team: Team, **overrides) -> GoalkeeperStat:
    defaults = {
        "team": team,
        "team_name": team.name,
        "league_name": team.league_name,
        "season": "2025-2026",
        "games": 20,
        "minutes_90s": 20.0,
        "ga": 20,
        "ga90": 1.0,
        "sota": 80,
        "saves": 60,
        "save_pct": 75.0,
        "cs": 8,
        "cs_pct": 40.0,
        "psxg_net": 2.5,
    }
    defaults.update(overrides)
    return GoalkeeperStat.objects.create(**defaults)
