from __future__ import annotations

from django.db.models import Avg, QuerySet

from apps.teams.models import Team


TEAM_FEATURE_FIELDS = (
    "matches_overall",
    "wins_overall",
    "draws_overall",
    "losses_overall",
    "goals_for_overall",
    "goals_against_overall",
    "points_overall",
    "xg_for",
    "xg_against",
)


def team_queryset() -> QuerySet[Team]:
    return Team.objects.all().order_by("name")


def team_dataset() -> list[Team]:
    return list(team_queryset())


def league_average_snapshot() -> dict[str, float | None]:
    return Team.objects.aggregate(
        league_avg_goals_for_per_game=Avg("goals_for_overall") / Avg("matches_overall"),
        league_avg_goals_against_per_game=Avg("goals_against_overall") / Avg("matches_overall"),
        league_avg_xg_for_per_game=Avg("xg_for") / Avg("matches_overall"),
        league_avg_xg_against_per_game=Avg("xg_against") / Avg("matches_overall"),
        league_avg_goals_per_team=Avg("goals_for_overall") / Avg("matches_overall"),
        league_avg_xg_per_team=Avg("xg_for") / Avg("matches_overall"),
    )


def analytics_dataset() -> list[dict[str, float | str | None]]:
    return list(
        Team.objects.values(
            "name",
            "matches_overall",
            "wins_overall",
            "draws_overall",
            "losses_overall",
            "goals_for_overall",
            "goals_against_overall",
            "points_overall",
            "xg_for",
            "xg_against",
        )
    )
