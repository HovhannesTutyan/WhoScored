from __future__ import annotations

from apps.teams.models import Team


def rating_team_queryset():
    return Team.objects.prefetch_related("players", "goalkeeper_stats").all().order_by("name")
