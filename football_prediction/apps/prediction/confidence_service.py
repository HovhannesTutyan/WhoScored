from __future__ import annotations

from apps.common.constants import CONFIDENCE_HIGH_THRESHOLD, CONFIDENCE_LOW_THRESHOLD
from apps.statistics.services import build_team_derived_stats


def _confidence_level(score: float) -> str:
    if score >= CONFIDENCE_HIGH_THRESHOLD:
        return "High"
    if score >= CONFIDENCE_LOW_THRESHOLD:
        return "Medium"
    return "Low"


def build_confidence_report(team_a, team_b, model_probabilities: dict[str, dict[str, float] | None], ensemble_prediction: dict[str, object]) -> dict[str, object]:
    available_models = [value for value in model_probabilities.values() if value is not None]
    agreement_targets = []
    for model in available_models:
        winner = max(model, key=model.get)
        agreement_targets.append(winner)

    ensemble_probs = ensemble_prediction["probabilities"]
    difference_score = abs(ensemble_probs["team_a_win"] - ensemble_probs["team_b_win"]) * 100
    agreement_score = 0.0
    if agreement_targets:
        most_common = max(set(agreement_targets), key=agreement_targets.count)
        agreement_score = (agreement_targets.count(most_common) / len(agreement_targets)) * 100

    min_matches = min(team_a.matches_overall, team_b.matches_overall)
    sample_size_score = min((min_matches / 38.0) * 100.0, 100.0)

    derived_a = build_team_derived_stats(team_a)
    derived_b = build_team_derived_stats(team_b)
    xg_consistency = max(
        0.0,
        100.0 - (
            abs(float(derived_a.get("attacking_overperformance") or 0.0))
            + abs(float(derived_b.get("attacking_overperformance") or 0.0))
        ) * 5.0,
    )

    player_completeness = min((min(team_a.players.count(), team_b.players.count()) / 18.0) * 100.0, 100.0)
    goalkeeper_completeness = 100.0 if team_a.goalkeeper_stats.exists() and team_b.goalkeeper_stats.exists() else 50.0
    data_completeness = (player_completeness + goalkeeper_completeness + sample_size_score) / 3.0

    confidence_score = (
        (data_completeness * 0.30)
        + (difference_score * 0.20)
        + (agreement_score * 0.20)
        + (sample_size_score * 0.10)
        + (xg_consistency * 0.10)
        + (player_completeness * 0.10)
    )
    confidence_score = round(min(confidence_score, 100.0), 2)
    confidence_level = _confidence_level(confidence_score)

    explanation = (
        f"Data completeness={data_completeness:.1f}, model agreement={agreement_score:.1f}, "
        f"team separation={difference_score:.1f}, sample size={sample_size_score:.1f}."
    )
    return {
        "confidence_score": confidence_score,
        "confidence_level": confidence_level,
        "confidence_explanation": explanation,
    }
