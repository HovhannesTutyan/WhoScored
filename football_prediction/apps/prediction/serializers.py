from rest_framework import serializers

from apps.common.constants import DEFAULT_SIMULATION_RUNS
from apps.comparison.serializers import TeamPairQuerySerializer
from apps.prediction.validators import validate_line_value
from apps.simulation.validators import validate_runs


class PredictionQuerySerializer(TeamPairQuerySerializer):
    pass


class PredictionOverUnderQuerySerializer(TeamPairQuerySerializer):
    line = serializers.FloatField(required=False, default=2.5)

    def validate_line(self, value):
        return validate_line_value(value)


class PredictionSimulationQuerySerializer(TeamPairQuerySerializer):
    runs = serializers.IntegerField(required=False, default=DEFAULT_SIMULATION_RUNS)

    def validate_runs(self, value):
        return validate_runs(value)


class PredictionResponseSerializer(serializers.Serializer):
    teams = serializers.DictField()
    overall_prediction = serializers.DictField()
    expected_goals = serializers.DictField()
    most_likely_scores = serializers.ListField(child=serializers.DictField())
    over_under = serializers.DictField()
    both_teams_to_score = serializers.DictField()
    team_comparison = serializers.DictField()
    strengths = serializers.DictField()
    weaknesses = serializers.DictField()
    risk_notes = serializers.ListField(child=serializers.CharField())
    model_breakdown = serializers.DictField()
