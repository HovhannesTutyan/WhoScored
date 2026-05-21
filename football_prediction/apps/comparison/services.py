from __future__ import annotations

from apps.math_utils.linear_algebra import cosine_similarity, feature_vector
from apps.statistics.player_impact_service import build_team_player_impact
from apps.statistics.services import build_attack_and_defense_strength, build_team_derived_stats
from apps.statistics.team_strength_service import build_team_strength
from apps.teams.selectors import get_latest_goalkeeper_stat


PROFILE_FIELDS = [
    "points_overall",
    "goals_for_overall",
    "goals_against_overall",
    "xg_for",
    "xg_against",
]


def _winner_label(team_a, team_b, value_a: float | None, value_b: float | None, *, lower_is_better: bool = False) -> str:
    if value_a is None or value_b is None:
        return "Unavailable"
    if abs(value_a - value_b) < 1e-9:
        return "Even"
    if lower_is_better:
        return team_a.name if value_a < value_b else team_b.name
    return team_a.name if value_a > value_b else team_b.name


def build_team_comparison(team_a, team_b) -> dict[str, object]:
    team_a_strength = build_team_strength(team_a)
    team_b_strength = build_team_strength(team_b)
    team_a_stats = build_team_derived_stats(team_a)
    team_b_stats = build_team_derived_stats(team_b)
    team_a_attack_defense = build_attack_and_defense_strength(team_a)
    team_b_attack_defense = build_attack_and_defense_strength(team_b)
    team_a_player_impact = build_team_player_impact(team_a)
    team_b_player_impact = build_team_player_impact(team_b)
    team_a_goalkeeper = get_latest_goalkeeper_stat(team_a)
    team_b_goalkeeper = get_latest_goalkeeper_stat(team_b)

    vector_a = feature_vector(
        {
            "points_overall": team_a.points_overall,
            "goals_for_overall": team_a.goals_for_overall,
            "goals_against_overall": team_a.goals_against_overall,
            "xg_for": team_a.xg_for,
            "xg_against": team_a.xg_against,
        },
        PROFILE_FIELDS,
    )
    vector_b = feature_vector(
        {
            "points_overall": team_b.points_overall,
            "goals_for_overall": team_b.goals_for_overall,
            "goals_against_overall": team_b.goals_against_overall,
            "xg_for": team_b.xg_for,
            "xg_against": team_b.xg_against,
        },
        PROFILE_FIELDS,
    )

    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "comparison": {
            "overall": _winner_label(team_a, team_b, team_a_strength["overall_team_strength"], team_b_strength["overall_team_strength"]),
            "attack": _winner_label(team_a, team_b, team_a_attack_defense["attack_strength"], team_b_attack_defense["attack_strength"]),
            "defense": _winner_label(team_a, team_b, team_a_attack_defense["defense_weakness"], team_b_attack_defense["defense_weakness"], lower_is_better=True),
            "xg": _winner_label(team_a, team_b, team_a_stats["xg_difference_per_game"], team_b_stats["xg_difference_per_game"]),
            "discipline": _winner_label(team_a, team_b, team_a_player_impact["average_discipline_impact"], team_b_player_impact["average_discipline_impact"]),
            "goalkeeper": _winner_label(team_a, team_b, getattr(team_a_goalkeeper, "save_pct", None), getattr(team_b_goalkeeper, "save_pct", None)),
            "player_impact": _winner_label(team_a, team_b, team_a_player_impact["average_total_player_impact"], team_b_player_impact["average_total_player_impact"]),
        },
        "metrics": {
            "team_a": {
                "team_strength": team_a_strength["overall_team_strength"],
                "attack_strength": team_a_attack_defense["attack_strength"],
                "defense_weakness": team_a_attack_defense["defense_weakness"],
                "xg_difference_per_game": team_a_stats["xg_difference_per_game"],
                "player_impact": team_a_player_impact["average_total_player_impact"],
            },
            "team_b": {
                "team_strength": team_b_strength["overall_team_strength"],
                "attack_strength": team_b_attack_defense["attack_strength"],
                "defense_weakness": team_b_attack_defense["defense_weakness"],
                "xg_difference_per_game": team_b_stats["xg_difference_per_game"],
                "player_impact": team_b_player_impact["average_total_player_impact"],
            },
        },
        "profile_similarity": cosine_similarity(vector_a, vector_b),
    }


def build_comparison_summary(team_a, team_b) -> dict[str, object]:
    return build_team_comparison(team_a, team_b)
