from rest_framework import serializers


class DerivedStatsSerializer(serializers.Serializer):
    win_rate = serializers.FloatField(allow_null=True)
    draw_rate = serializers.FloatField(allow_null=True)
    loss_rate = serializers.FloatField(allow_null=True)
    goals_for_per_game = serializers.FloatField(allow_null=True)
    goals_against_per_game = serializers.FloatField(allow_null=True)
    points_per_game = serializers.FloatField(allow_null=True)
    xg_for_per_game = serializers.FloatField(allow_null=True)
    xg_against_per_game = serializers.FloatField(allow_null=True)
    goal_difference = serializers.FloatField(allow_null=True)
    goal_difference_per_game = serializers.FloatField(allow_null=True)
    xg_difference = serializers.FloatField(allow_null=True)
    xg_difference_per_game = serializers.FloatField(allow_null=True)
    finishing_efficiency = serializers.FloatField(allow_null=True)
    attacking_overperformance = serializers.FloatField(allow_null=True)
    defensive_overperformance = serializers.FloatField(allow_null=True)
