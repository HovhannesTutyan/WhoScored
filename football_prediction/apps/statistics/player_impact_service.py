from __future__ import annotations

from apps.common.constants import PLAYER_IMPACT_WEIGHTS
from apps.math_utils.statistics import average


def _value(source, field_name: str) -> float:
    return float(getattr(source, field_name, 0) or 0.0)


def build_player_impact(player) -> dict[str, float]:
    attack_impact = (
        (_value(player, "goals") * PLAYER_IMPACT_WEIGHTS["attack"]["goals"])
        + (_value(player, "assists") * PLAYER_IMPACT_WEIGHTS["attack"]["assists"])
        + (_value(player, "shots_per_game") * PLAYER_IMPACT_WEIGHTS["attack"]["shots_per_game"])
        + (_value(player, "dribbles") * PLAYER_IMPACT_WEIGHTS["attack"]["dribbles"])
        + (_value(player, "aerial_won_per_game") * PLAYER_IMPACT_WEIGHTS["attack"]["aerial_won_per_game"])
    )
    defensive_impact = (
        (_value(player, "tackles") * PLAYER_IMPACT_WEIGHTS["defense"]["tackles"])
        + (_value(player, "aerial_won_per_game") * PLAYER_IMPACT_WEIGHTS["defense"]["aerial_won_per_game"])
        + (_value(player, "fouls") * PLAYER_IMPACT_WEIGHTS["defense"]["fouls"])
        + (_value(player, "cards") * PLAYER_IMPACT_WEIGHTS["defense"]["cards"])
    )
    goalkeeper_impact = (
        (_value(player, "saves") * PLAYER_IMPACT_WEIGHTS["goalkeeper"]["saves"])
        + (_value(player, "goals_conceded") * PLAYER_IMPACT_WEIGHTS["goalkeeper"]["goals_conceded"])
    )
    discipline_impact = (
        (_value(player, "cards") * PLAYER_IMPACT_WEIGHTS["discipline"]["cards"])
        + (_value(player, "fouls") * PLAYER_IMPACT_WEIGHTS["discipline"]["fouls"])
        + (_value(player, "offsides") * PLAYER_IMPACT_WEIGHTS["discipline"]["offsides"])
    )
    total_player_impact = attack_impact + defensive_impact + goalkeeper_impact + discipline_impact
    return {
        "attack_impact": attack_impact,
        "defensive_impact": defensive_impact,
        "discipline_impact": discipline_impact,
        "goalkeeper_impact": goalkeeper_impact,
        "total_player_impact": total_player_impact,
    }


def build_team_player_impact(team) -> dict[str, object]:
    players = list(team.players.all())
    if not players:
        return {
            "average_total_player_impact": 0.0,
            "player_count": 0,
            "warning": "No player data available.",
            "players": [],
        }

    impacts = [{"player": player, **build_player_impact(player)} for player in players]
    return {
        "average_total_player_impact": average([item["total_player_impact"] for item in impacts]) or 0.0,
        "average_attack_impact": average([item["attack_impact"] for item in impacts]) or 0.0,
        "average_defensive_impact": average([item["defensive_impact"] for item in impacts]) or 0.0,
        "average_discipline_impact": average([item["discipline_impact"] for item in impacts]) or 0.0,
        "average_goalkeeper_impact": average([item["goalkeeper_impact"] for item in impacts]) or 0.0,
        "player_count": len(players),
        "warning": "Starting lineup data is not available; impacts are normalized across all available players.",
        "players": impacts,
    }
