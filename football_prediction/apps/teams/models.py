from __future__ import annotations

from django.db import models


class Team(models.Model):
    source_team_id = models.IntegerField(unique=True, null=True, blank=True)
    league_name = models.CharField(max_length=120, blank=True, default="")
    name = models.CharField(max_length=255, unique=True)
    matches_overall = models.PositiveIntegerField(default=0)
    wins_overall = models.PositiveIntegerField(default=0)
    draws_overall = models.PositiveIntegerField(default=0)
    losses_overall = models.PositiveIntegerField(default=0)
    goals_for_overall = models.PositiveIntegerField(default=0)
    goals_against_overall = models.PositiveIntegerField(default=0)
    points_overall = models.PositiveIntegerField(default=0)
    xg_for = models.FloatField(null=True, blank=True)
    xg_against = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-points_overall", "name"]

    def __str__(self) -> str:
        return self.name


class GoalkeeperStat(models.Model):
    source_goalkeeper_id = models.IntegerField(unique=True, null=True, blank=True)
    team = models.ForeignKey(Team, related_name="goalkeeper_stats", on_delete=models.CASCADE)
    team_name = models.CharField(max_length=255)
    league_name = models.CharField(max_length=120)
    season = models.CharField(max_length=30)
    games = models.PositiveIntegerField(null=True, blank=True)
    minutes_90s = models.FloatField(null=True, blank=True)
    ga = models.PositiveIntegerField(null=True, blank=True)
    ga90 = models.FloatField(null=True, blank=True)
    sota = models.PositiveIntegerField(null=True, blank=True)
    saves = models.PositiveIntegerField(null=True, blank=True)
    save_pct = models.FloatField(null=True, blank=True)
    cs = models.PositiveIntegerField(null=True, blank=True)
    cs_pct = models.FloatField(null=True, blank=True)
    pens_att = models.PositiveIntegerField(null=True, blank=True)
    pens_allowed = models.PositiveIntegerField(null=True, blank=True)
    pens_saved = models.PositiveIntegerField(null=True, blank=True)
    pens_missed = models.PositiveIntegerField(null=True, blank=True)
    pens_save_pct = models.FloatField(null=True, blank=True)
    psxg = models.FloatField(null=True, blank=True)
    psxg_per_sot = models.FloatField(null=True, blank=True)
    psxg_net = models.FloatField(null=True, blank=True)
    psxg_net_per90 = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["team__name"]
        constraints = [
            models.UniqueConstraint(fields=["team", "season"], name="unique_team_goalkeeper_season"),
        ]

    def __str__(self) -> str:
        return f"{self.team_name} ({self.season})"
