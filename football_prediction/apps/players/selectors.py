from __future__ import annotations

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.players.models import Player


def player_list_queryset() -> QuerySet[Player]:
    return Player.objects.select_related("team").all().order_by("name")


def get_player(player_id: int) -> Player:
    return get_object_or_404(player_list_queryset(), pk=player_id)
