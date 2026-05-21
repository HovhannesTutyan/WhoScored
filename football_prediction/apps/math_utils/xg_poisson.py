from __future__ import annotations

from apps.common.constants import DEFAULT_MAX_GOALS
from apps.math_utils.poisson import score_matrix, summarize_score_matrix
from apps.math_utils.statistics import safe_divide


def calculate_xg_lambdas(team_a_xg_for_per_game: float | None, team_a_xg_against_per_game: float | None, team_b_xg_for_per_game: float | None, team_b_xg_against_per_game: float | None, league_avg_xg_per_team: float | None) -> tuple[float | None, float | None]:
    if league_avg_xg_per_team in (None, 0):
        return None, None
    lambda_a = safe_divide((team_a_xg_for_per_game or 0.0) * (team_b_xg_against_per_game or 0.0), league_avg_xg_per_team)
    lambda_b = safe_divide((team_b_xg_for_per_game or 0.0) * (team_a_xg_against_per_game or 0.0), league_avg_xg_per_team)
    return lambda_a, lambda_b


def predict_with_xg_poisson(lambda_a: float, lambda_b: float, max_goals: int = DEFAULT_MAX_GOALS) -> dict[str, object]:
    matrix = score_matrix(lambda_a, lambda_b, max_goals=max_goals)
    return {
        "lambda_a": lambda_a,
        "lambda_b": lambda_b,
        "matrix": matrix,
        "summary": summarize_score_matrix(matrix),
    }
