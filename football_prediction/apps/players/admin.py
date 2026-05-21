from django.contrib import admin

from apps.players.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "team", "goals", "assists", "cards")
    search_fields = ("name", "team__name")
    list_filter = ("team__league_name",)
