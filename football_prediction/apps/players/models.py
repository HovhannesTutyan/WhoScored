from __future__ import annotations

from django.db import models

from apps.teams.models import Team


class Player(models.Model):
    source_player_id = models.IntegerField(unique=True, null=True, blank=True)
    team = models.ForeignKey(Team, related_name="players", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    goals = models.FloatField(null=True, blank=True)
    assists = models.FloatField(null=True, blank=True)
    cards = models.FloatField(null=True, blank=True)
    shots_per_game = models.FloatField(null=True, blank=True)
    aerial_won_per_game = models.FloatField(null=True, blank=True)
    tackles = models.FloatField(null=True, blank=True)
    fouls = models.FloatField(null=True, blank=True)
    offsides = models.FloatField(null=True, blank=True)
    dribbles = models.FloatField(null=True, blank=True)
    goals_conceded = models.FloatField(null=True, blank=True)
    saves = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["team", "name"], name="unique_player_team_name"),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.team.name})"
