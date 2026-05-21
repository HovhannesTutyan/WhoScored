from __future__ import annotations

from apps.math_utils.statistics import safe_divide, safe_subtract
from apps.statistics.selectors import league_average_snapshot


def build_team_derived_stats(team) -> dict[str, float | None]:
    matches = team.matches_overall
    goals_for = team.goals_for_overall
    goals_against = team.goals_against_overall
    xg_for = team.xg_for
    xg_against = team.xg_against
    goal_difference = safe_subtract(goals_for, goals_against)
    xg_difference = safe_subtract(xg_for, xg_against)

    return {
        "win_rate": safe_divide(team.wins_overall, matches),
        "draw_rate": safe_divide(team.draws_overall, matches),
        "loss_rate": safe_divide(team.losses_overall, matches),
        "goals_for_per_game": safe_divide(goals_for, matches),
        "goals_against_per_game": safe_divide(goals_against, matches),
        "points_per_game": safe_divide(team.points_overall, matches),
        "xg_for_per_game": safe_divide(xg_for, matches),
        "xg_against_per_game": safe_divide(xg_against, matches),
        "goal_difference": goal_difference,
        "goal_difference_per_game": safe_divide(goal_difference, matches),
        "xg_difference": xg_difference,
        "xg_difference_per_game": safe_divide(xg_difference, matches),
        "finishing_efficiency": safe_divide(goals_for, xg_for),
        "attacking_overperformance": safe_subtract(goals_for, xg_for),
        "defensive_overperformance": safe_subtract(xg_against, goals_against),
    }


def build_league_context() -> dict[str, float | None]:
    return league_average_snapshot()


def build_attack_and_defense_strength(team) -> dict[str, float | None]:
    team_stats = build_team_derived_stats(team)
    league_stats = build_league_context()
    return {
        "attack_strength": safe_divide(team_stats["goals_for_per_game"], league_stats.get("league_avg_goals_for_per_game")),
        "defense_weakness": safe_divide(team_stats["goals_against_per_game"], league_stats.get("league_avg_goals_against_per_game")),
        "xg_attack_strength": safe_divide(team_stats["xg_for_per_game"], league_stats.get("league_avg_xg_for_per_game")),
        "xg_defense_weakness": safe_divide(team_stats["xg_against_per_game"], league_stats.get("league_avg_xg_against_per_game")),
    }
