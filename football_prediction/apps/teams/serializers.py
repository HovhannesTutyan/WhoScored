from rest_framework import serializers

from apps.players.serializers import PlayerListSerializer
from apps.teams.models import Team


class TeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "league_name",
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


class TeamDetailSerializer(TeamListSerializer):
    class Meta(TeamListSerializer.Meta):
        fields = TeamListSerializer.Meta.fields + ("created_at", "updated_at")


class TeamPlayersSerializer(serializers.Serializer):
    team = serializers.DictField()
    players = PlayerListSerializer(many=True)


class TeamStatsSerializer(serializers.Serializer):
    team = serializers.DictField()
    derived_stats = serializers.DictField()
    attack_and_defense = serializers.DictField()
    team_strength = serializers.DictField()
    player_impact = serializers.DictField()
    goalkeeper = serializers.DictField(allow_null=True)


class StrengthWeaknessSerializer(serializers.Serializer):
    team = serializers.DictField()
    strengths = serializers.ListField(child=serializers.CharField())
    weaknesses = serializers.ListField(child=serializers.CharField())
    risk_notes = serializers.ListField(child=serializers.CharField())
