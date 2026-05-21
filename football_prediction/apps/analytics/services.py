from __future__ import annotations

from apps.analytics.selectors import analytics_team_dataset, grouped_teams_by_league
from apps.math_utils.correlation import feature_relationships
from apps.statistics.services import build_team_derived_stats


def build_correlation_report() -> dict[str, object]:
    dataset = [
        {
            "wins_overall": float(team.wins_overall),
            "goals_for_overall": float(team.goals_for_overall),
            "goals_against_overall": float(team.goals_against_overall),
            "xg_for": float(team.xg_for or 0.0),
            "xg_against": float(team.xg_against or 0.0),
            "points_overall": float(team.points_overall),
        }
        for team in analytics_team_dataset()
    ]
    return feature_relationships(dataset, target_field="points_overall")


def build_feature_importance_report() -> dict[str, object]:
    relationships = build_correlation_report()
    ranked = []
    for feature_name, values in relationships.items():
        pearson = values.get("pearson") if isinstance(values, dict) else None
        ranked.append(
            {
                "feature": feature_name,
                "importance": abs(float(pearson)) if pearson is not None else 0.0,
                "details": values,
            }
        )
    ranked.sort(key=lambda item: item["importance"], reverse=True)
    return {"features": ranked}


def build_league_averages_report() -> dict[str, object]:
    result: dict[str, object] = {}
    for league_name, teams in grouped_teams_by_league().items():
        if not teams:
            continue
        derived = [build_team_derived_stats(team) for team in teams]
        result[league_name] = {
            "teams": len(teams),
            "avg_points": sum(team.points_overall for team in teams) / len(teams),
            "avg_goals_for": sum(team.goals_for_overall for team in teams) / len(teams),
            "avg_goals_against": sum(team.goals_against_overall for team in teams) / len(teams),
            "avg_xg_for": sum(float(team.xg_for or 0.0) for team in teams) / len(teams),
            "avg_xg_against": sum(float(team.xg_against or 0.0) for team in teams) / len(teams),
            "avg_points_per_game": sum(float(item["points_per_game"] or 0.0) for item in derived) / len(derived),
        }
    return result
