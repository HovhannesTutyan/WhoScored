from __future__ import annotations

from apps.common.constants import POWER_RATING_WEIGHTS
from apps.math_utils.normalization import min_max_normalize, reverse_normalize
from apps.statistics.player_impact_service import build_team_player_impact
from apps.statistics.services import build_attack_and_defense_strength, build_team_derived_stats
from apps.statistics.selectors import team_dataset


def _effective_weights() -> dict[str, float]:
    weights = dict(POWER_RATING_WEIGHTS)
    elo_weight = weights.pop("elo")
    weights["xg_rating"] += elo_weight / 2
    weights["goal_difference_rating"] += elo_weight / 2
    return weights


def build_power_rating(team) -> dict[str, float | None]:
    teams = team_dataset()
    weights = _effective_weights()
    team_stats = build_team_derived_stats(team)
    defense_snapshot = build_attack_and_defense_strength(team)
    team_player_impact = build_team_player_impact(team)

    xg_values = [build_team_derived_stats(item)["xg_difference_per_game"] for item in teams]
    goal_diff_values = [build_team_derived_stats(item)["goal_difference_per_game"] for item in teams]
    player_values = [build_team_player_impact(item)["average_total_player_impact"] for item in teams]
    defense_values = [build_attack_and_defense_strength(item)["defense_weakness"] for item in teams]

    component_scores = {
        "elo": None,
        "xg_rating": min_max_normalize(team_stats["xg_difference_per_game"], xg_values),
        "goal_difference_rating": min_max_normalize(team_stats["goal_difference_per_game"], goal_diff_values),
        "player_rating": min_max_normalize(team_player_impact["average_total_player_impact"], player_values),
        "defensive_rating": reverse_normalize(defense_snapshot["defense_weakness"], defense_values),
    }

    rating = 0.0
    for key, weight in weights.items():
        value = component_scores.get(key)
        if value is not None:
            rating += value * weight

    component_scores["power_rating"] = rating * 100
    component_scores["weights_used"] = weights
    return component_scores


def build_power_ratings() -> dict[str, object]:
    return {
        "available": True,
        "ratings": [
            {
                "team": {"id": team.id, "name": team.name},
                **build_power_rating(team),
            }
            for team in team_dataset()
        ],
    }
