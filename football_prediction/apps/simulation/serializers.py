from rest_framework import serializers

from apps.common.constants import DEFAULT_SIMULATION_RUNS
from apps.comparison.serializers import TeamPairQuerySerializer
from apps.simulation.validators import validate_runs


class SimulationQuerySerializer(TeamPairQuerySerializer):
    runs = serializers.IntegerField(required=False, default=DEFAULT_SIMULATION_RUNS)

    def validate_runs(self, value):
        return validate_runs(value)


class SimulationResponseSerializer(serializers.Serializer):
    outcomes = serializers.DictField()
    scorelines = serializers.ListField(child=serializers.DictField())
    over_under = serializers.DictField()
    btts = serializers.DictField()
