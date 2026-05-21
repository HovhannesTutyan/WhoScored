from rest_framework import serializers

from apps.players.models import Player


class PlayerListSerializer(serializers.ModelSerializer):
    team_id = serializers.IntegerField(source="team.id", read_only=True)
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = Player
        fields = (
            "id",
            "team_id",
            "team_name",
            "name",
            "goals",
            "assists",
            "cards",
        )


class PlayerDetailSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()

    class Meta:
        model = Player
        fields = (
            "id",
            "team",
            "name",
            "goals",
            "assists",
            "cards",
            "shots_per_game",
            "aerial_won_per_game",
            "tackles",
            "fouls",
            "offsides",
            "dribbles",
            "goals_conceded",
            "saves",
            "created_at",
            "updated_at",
        )

    def get_team(self, obj):
        return {"id": obj.team_id, "name": obj.team.name}


class PlayerStatsSerializer(serializers.Serializer):
    player = serializers.DictField()
    raw_stats = serializers.DictField()
    impact = serializers.DictField()
