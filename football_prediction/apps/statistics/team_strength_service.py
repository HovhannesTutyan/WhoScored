from __future__ import annotations

from apps.common.constants import TEAM_STRENGTH_WEIGHTS
from apps.math_utils.normalization import min_max_normalize, reverse_normalize
from apps.statistics.player_impact_service import build_team_player_impact
from apps.statistics.services import build_attack_and_defense_strength, build_team_derived_stats
from apps.statistics.selectors import team_dataset


def build_team_strength(team) -> dict[str, float | None]:
    teams = team_dataset()
    team_stats = build_team_derived_stats(team)
    strength_stats = build_attack_and_defense_strength(team)
    player_impact = build_team_player_impact(team)

    points_values = [build_team_derived_stats(item)["points_per_game"] for item in teams]
    goal_diff_values = [build_team_derived_stats(item)["goal_difference_per_game"] for item in teams]
    xg_diff_values = [build_team_derived_stats(item)["xg_difference_per_game"] for item in teams]
    attack_values = [build_attack_and_defense_strength(item)["attack_strength"] for item in teams]
    defense_values = [build_attack_and_defense_strength(item)["defense_weakness"] for item in teams]
    player_values = [build_team_player_impact(item)["average_total_player_impact"] for item in teams]

    component_scores = {
        "points_per_game_score": min_max_normalize(team_stats["points_per_game"], points_values),
        "goal_difference_score": min_max_normalize(team_stats["goal_difference_per_game"], goal_diff_values),
        "xg_difference_score": min_max_normalize(team_stats["xg_difference_per_game"], xg_diff_values),
        "attacking_score": min_max_normalize(strength_stats["attack_strength"], attack_values),
        "defensive_score": reverse_normalize(strength_stats["defense_weakness"], defense_values),
        "player_impact_score": min_max_normalize(player_impact["average_total_player_impact"], player_values),
    }

    overall_score = 0.0
    if component_scores["points_per_game_score"] is not None:
        overall_score += component_scores["points_per_game_score"] * TEAM_STRENGTH_WEIGHTS["points_per_game"]
    if component_scores["goal_difference_score"] is not None:
        overall_score += component_scores["goal_difference_score"] * TEAM_STRENGTH_WEIGHTS["goal_difference"]
    if component_scores["xg_difference_score"] is not None:
        overall_score += component_scores["xg_difference_score"] * TEAM_STRENGTH_WEIGHTS["xg_difference"]
    if component_scores["attacking_score"] is not None:
        overall_score += component_scores["attacking_score"] * TEAM_STRENGTH_WEIGHTS["attacking"]
    if component_scores["defensive_score"] is not None:
        overall_score += component_scores["defensive_score"] * TEAM_STRENGTH_WEIGHTS["defensive"]
    if component_scores["player_impact_score"] is not None:
        overall_score += component_scores["player_impact_score"] * TEAM_STRENGTH_WEIGHTS["player_impact"]

    return {
        **component_scores,
        "overall_team_strength": overall_score * 100,
    }
