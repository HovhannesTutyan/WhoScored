from __future__ import annotations

from apps.common.constants import ENSEMBLE_MODEL_WEIGHTS
from apps.math_utils.probability import redistribute_weights


def score_to_outcome_probabilities(score_a: float | None, score_b: float | None) -> dict[str, float] | None:
    if score_a is None or score_b is None:
        return None

    adjusted_a = float(score_a)
    adjusted_b = float(score_b)
    minimum = min(adjusted_a, adjusted_b)
    if minimum <= 0:
        adjusted_a = adjusted_a - minimum + 1.0
        adjusted_b = adjusted_b - minimum + 1.0

    total = adjusted_a + adjusted_b
    if total <= 0:
        return None

    base_a = adjusted_a / total
    base_b = adjusted_b / total
    gap = abs(base_a - base_b)
    draw = max(0.12, 0.30 - (gap * 0.20))
    remaining = 1.0 - draw

    return {
        "team_a_win": base_a * remaining,
        "draw": draw,
        "team_b_win": base_b * remaining,
    }


def build_ensemble_prediction(model_probabilities: dict[str, dict[str, float] | None]) -> dict[str, object]:
    available_keys = [key for key, value in model_probabilities.items() if value is not None]
    weights = redistribute_weights(ENSEMBLE_MODEL_WEIGHTS, available_keys)
    combined = {
        "team_a_win": 0.0,
        "draw": 0.0,
        "team_b_win": 0.0,
    }
    for key, probability_map in model_probabilities.items():
        if probability_map is None or key not in weights:
            continue
        for outcome, value in probability_map.items():
            combined[outcome] += value * weights[key]

    predicted_winner = "Draw"
    if combined["team_a_win"] > max(combined["draw"], combined["team_b_win"]):
        predicted_winner = "team_a"
    elif combined["team_b_win"] > max(combined["draw"], combined["team_a_win"]):
        predicted_winner = "team_b"

    return {
        "weights_used": weights,
        "probabilities": combined,
        "predicted_winner": predicted_winner,
    }
