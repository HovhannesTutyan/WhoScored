from __future__ import annotations

from apps.common.constants import BLENDED_POISSON_WEIGHTS, DEFAULT_MAX_GOALS
from apps.math_utils.poisson import score_matrix, summarize_score_matrix


def calculate_blended_lambdas(goals_lambda_a: float | None, goals_lambda_b: float | None, xg_lambda_a: float | None, xg_lambda_b: float | None, weights: dict[str, float] | None = None) -> tuple[float | None, float | None]:
    effective_weights = weights or BLENDED_POISSON_WEIGHTS
    if None in {goals_lambda_a, goals_lambda_b, xg_lambda_a, xg_lambda_b}:
        return None, None
    lambda_a = (goals_lambda_a * effective_weights["goals"]) + (xg_lambda_a * effective_weights["xg"])
    lambda_b = (goals_lambda_b * effective_weights["goals"]) + (xg_lambda_b * effective_weights["xg"])
    return lambda_a, lambda_b


def predict_with_blended_poisson(lambda_a: float, lambda_b: float, max_goals: int = DEFAULT_MAX_GOALS) -> dict[str, object]:
    matrix = score_matrix(lambda_a, lambda_b, max_goals=max_goals)
    return {
        "lambda_a": lambda_a,
        "lambda_b": lambda_b,
        "matrix": matrix,
        "summary": summarize_score_matrix(matrix),
    }
