from django.contrib import admin

from apps.teams.models import GoalkeeperStat, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "league_name", "points_overall", "matches_overall", "xg_for", "xg_against")
    search_fields = ("name", "league_name")
    list_filter = ("league_name",)


@admin.register(GoalkeeperStat)
class GoalkeeperStatAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "season", "ga", "save_pct", "cs", "psxg_net")
    search_fields = ("team_name", "season")
    list_filter = ("league_name", "season")
