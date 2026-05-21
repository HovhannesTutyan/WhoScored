from __future__ import annotations

from collections import defaultdict

from apps.teams.models import Team


def analytics_team_dataset() -> list[Team]:
    return list(Team.objects.prefetch_related("players", "goalkeeper_stats").all().order_by("name"))


def grouped_teams_by_league() -> dict[str, list[Team]]:
    grouped: dict[str, list[Team]] = defaultdict(list)
    for team in analytics_team_dataset():
        grouped[team.league_name or "Unknown"].append(team)
    return dict(grouped)
