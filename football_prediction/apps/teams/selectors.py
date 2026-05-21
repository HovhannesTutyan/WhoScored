from __future__ import annotations

from django.db.models import Prefetch, QuerySet
from django.shortcuts import get_object_or_404

from apps.players.models import Player
from apps.teams.models import GoalkeeperStat, Team


def team_list_queryset() -> QuerySet[Team]:
    return Team.objects.all().order_by("-points_overall", "name")


def team_detail_queryset() -> QuerySet[Team]:
    return Team.objects.prefetch_related(
        Prefetch("players", queryset=Player.objects.order_by("name")),
        Prefetch("goalkeeper_stats", queryset=GoalkeeperStat.objects.order_by("-updated_at")),
    )


def get_team(team_id: int) -> Team:
    return get_object_or_404(team_detail_queryset(), pk=team_id)


def get_team_players(team: Team) -> QuerySet[Player]:
    return team.players.all().order_by("name")


def get_latest_goalkeeper_stat(team: Team) -> GoalkeeperStat | None:
    return team.goalkeeper_stats.order_by("-updated_at").first()
