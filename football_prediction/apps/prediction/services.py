from __future__ import annotations

from apps.comparison.services import build_team_comparison
from apps.math_utils.blended_poisson import calculate_blended_lambdas, predict_with_blended_poisson
from apps.math_utils.poisson import score_matrix, summarize_score_matrix
from apps.math_utils.xg_poisson import calculate_xg_lambdas, predict_with_xg_poisson
from apps.players.services import build_team_player_impact_payload
from apps.prediction.confidence_service import build_confidence_report
from apps.prediction.ensemble_service import build_ensemble_prediction, score_to_outcome_probabilities
from apps.ratings.power_rating_service import build_power_rating
from apps.simulation.services import build_simulation_result
from apps.statistics.services import build_attack_and_defense_strength, build_league_context, build_team_derived_stats
from apps.statistics.strengths_weaknesses_service import build_strengths_and_weaknesses
from apps.statistics.team_strength_service import build_team_strength


def build_goals_poisson_model(team_a, team_b) -> dict[str, object]:
    team_a_snapshot = build_attack_and_defense_strength(team_a)
    team_b_snapshot = build_attack_and_defense_strength(team_b)
    league_context = build_league_context()
    league_avg_goals_per_team = float(league_context.get("league_avg_goals_per_team") or 1.35)

    lambda_a = league_avg_goals_per_team * float(team_a_snapshot.get("attack_strength") or 1.0) * float(team_b_snapshot.get("defense_weakness") or 1.0)
    lambda_b = league_avg_goals_per_team * float(team_b_snapshot.get("attack_strength") or 1.0) * float(team_a_snapshot.get("defense_weakness") or 1.0)
    matrix = score_matrix(lambda_a, lambda_b)
    return {
        "lambda_a": lambda_a,
        "lambda_b": lambda_b,
        "summary": summarize_score_matrix(matrix),
    }


def build_xg_poisson_model(team_a, team_b) -> dict[str, object] | None:
    team_a_stats = build_team_derived_stats(team_a)
    team_b_stats = build_team_derived_stats(team_b)
    league_context = build_league_context()
    lambda_a, lambda_b = calculate_xg_lambdas(
        team_a_stats.get("xg_for_per_game"),
        team_a_stats.get("xg_against_per_game"),
        team_b_stats.get("xg_for_per_game"),
        team_b_stats.get("xg_against_per_game"),
        league_context.get("league_avg_xg_per_team"),
    )
    if lambda_a is None or lambda_b is None:
        return None
    return predict_with_xg_poisson(lambda_a, lambda_b)


def build_blended_poisson_model(goals_model: dict[str, object], xg_model: dict[str, object] | None) -> dict[str, object] | None:
    if xg_model is None:
        return None
    lambda_a, lambda_b = calculate_blended_lambdas(
        goals_model["lambda_a"],
        goals_model["lambda_b"],
        xg_model["lambda_a"],
        xg_model["lambda_b"],
    )
    if lambda_a is None or lambda_b is None:
        return None
    return predict_with_blended_poisson(lambda_a, lambda_b)


def build_prediction_models(team_a, team_b) -> dict[str, object]:
    goals_model = build_goals_poisson_model(team_a, team_b)
    xg_model = build_xg_poisson_model(team_a, team_b)
    blended_model = build_blended_poisson_model(goals_model, xg_model)

    team_a_strength = build_team_strength(team_a)
    team_b_strength = build_team_strength(team_b)
    team_strength_probabilities = score_to_outcome_probabilities(
        team_a_strength.get("overall_team_strength"),
        team_b_strength.get("overall_team_strength"),
    )

    team_a_player_impact = build_team_player_impact_payload(team_a)
    team_b_player_impact = build_team_player_impact_payload(team_b)
    player_impact_probabilities = score_to_outcome_probabilities(
        team_a_player_impact.get("average_total_player_impact"),
        team_b_player_impact.get("average_total_player_impact"),
    )

    team_a_power = build_power_rating(team_a)
    team_b_power = build_power_rating(team_b)
    power_probabilities = score_to_outcome_probabilities(
        team_a_power.get("power_rating"),
        team_b_power.get("power_rating"),
    )

    model_probabilities = {
        "poisson": goals_model["summary"]["outcomes"],
        "xg_poisson": xg_model["summary"]["outcomes"] if xg_model else None,
        "blended_poisson": blended_model["summary"]["outcomes"] if blended_model else None,
        "team_strength": team_strength_probabilities,
        "player_impact": player_impact_probabilities,
        "power_rating": power_probabilities,
    }

    ensemble = build_ensemble_prediction(model_probabilities)
    selected_model = blended_model or xg_model or goals_model

    return {
        "goals_model": goals_model,
        "xg_model": xg_model,
        "blended_model": blended_model,
        "team_strength": {"team_a": team_a_strength, "team_b": team_b_strength, "probabilities": team_strength_probabilities},
        "player_impact": {"team_a": team_a_player_impact, "team_b": team_b_player_impact, "probabilities": player_impact_probabilities},
        "power_rating": {"team_a": team_a_power, "team_b": team_b_power, "probabilities": power_probabilities},
        "ensemble": ensemble,
        "selected_model": selected_model,
        "model_probabilities": model_probabilities,
    }


def build_prediction_payload(team_a, team_b) -> dict[str, object]:
    models = build_prediction_models(team_a, team_b)
    comparison = build_team_comparison(team_a, team_b)
    strengths_a = build_strengths_and_weaknesses(team_a)
    strengths_b = build_strengths_and_weaknesses(team_b)
    confidence = build_confidence_report(team_a, team_b, models["model_probabilities"], models["ensemble"])
    selected_summary = models["selected_model"]["summary"]
    expected_goals = {
        "team_a": round(float(models["selected_model"]["lambda_a"]), 3),
        "team_b": round(float(models["selected_model"]["lambda_b"]), 3),
    }

    overall_probabilities = models["ensemble"]["probabilities"]
    predicted_winner = models["ensemble"]["predicted_winner"]
    if predicted_winner == "team_a":
        predicted_winner = team_a.name
    elif predicted_winner == "team_b":
        predicted_winner = team_b.name
    else:
        predicted_winner = "Draw"

    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "overall_prediction": {
            "team_a_win": overall_probabilities["team_a_win"],
            "draw": overall_probabilities["draw"],
            "team_b_win": overall_probabilities["team_b_win"],
            "predicted_winner": predicted_winner,
            "confidence_score": confidence["confidence_score"],
            "confidence_level": confidence["confidence_level"],
        },
        "expected_goals": expected_goals,
        "most_likely_scores": selected_summary["scorelines"],
        "over_under": selected_summary["over_under"],
        "both_teams_to_score": selected_summary["btts"],
        "team_comparison": comparison["comparison"],
        "strengths": {
            "team_a": strengths_a["strengths"],
            "team_b": strengths_b["strengths"],
        },
        "weaknesses": {
            "team_a": strengths_a["weaknesses"],
            "team_b": strengths_b["weaknesses"],
        },
        "risk_notes": strengths_a["risk_notes"] + strengths_b["risk_notes"],
        "model_breakdown": {
            "poisson": goals_model_payload(models["goals_model"]),
            "xg_poisson": model_payload(models["xg_model"]),
            "blended_poisson": model_payload(models["blended_model"]),
            "team_strength": models["team_strength"],
            "player_impact": models["player_impact"],
            "power_rating": models["power_rating"],
            "ensemble": models["ensemble"],
        },
    }


def model_payload(model: dict[str, object] | None) -> dict[str, object]:
    if model is None:
        return {"available": False, "message": "Model unavailable."}
    return {
        "available": True,
        "lambda_a": model["lambda_a"],
        "lambda_b": model["lambda_b"],
        **model["summary"],
    }


def goals_model_payload(model: dict[str, object]) -> dict[str, object]:
    return model_payload(model)


def build_probabilities_payload(team_a, team_b) -> dict[str, object]:
    payload = build_prediction_payload(team_a, team_b)
    return {
        "teams": payload["teams"],
        "overall_prediction": payload["overall_prediction"],
        "expected_goals": payload["expected_goals"],
    }


def build_exact_score_payload(team_a, team_b) -> dict[str, object]:
    payload = build_prediction_payload(team_a, team_b)
    return {
        "teams": payload["teams"],
        "expected_goals": payload["expected_goals"],
        "most_likely_scores": payload["most_likely_scores"],
    }


def build_over_under_payload(team_a, team_b, line: float) -> dict[str, object]:
    models = build_prediction_models(team_a, team_b)
    selected_summary = models["selected_model"]["summary"]["over_under"]
    line_key = str(line).replace('.', '_')
    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "line": line,
        "probabilities": {
            "over": selected_summary.get(f"over_{line_key}"),
            "under": selected_summary.get(f"under_{line_key}"),
        },
    }


def build_btts_payload(team_a, team_b) -> dict[str, object]:
    models = build_prediction_models(team_a, team_b)
    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "both_teams_to_score": models["selected_model"]["summary"]["btts"],
    }


def build_model_breakdown_payload(team_a, team_b) -> dict[str, object]:
    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "model_breakdown": build_prediction_payload(team_a, team_b)["model_breakdown"],
    }


def build_simulation_payload(team_a, team_b, runs: int) -> dict[str, object]:
    models = build_prediction_models(team_a, team_b)
    simulation = build_simulation_result(models["selected_model"]["lambda_a"], models["selected_model"]["lambda_b"], runs)
    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "runs": runs,
        "simulation": simulation,
    }
