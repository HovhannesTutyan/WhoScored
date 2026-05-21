from rest_framework import serializers

from apps.comparison.selectors import get_team_pair
from apps.comparison.validators import validate_distinct_teams


class TeamPairQuerySerializer(serializers.Serializer):
    team_a = serializers.IntegerField(required=True)
    team_b = serializers.IntegerField(required=True)

    def validate(self, attrs):
        validate_distinct_teams(attrs["team_a"], attrs["team_b"])
        team_a, team_b = get_team_pair(attrs["team_a"], attrs["team_b"])
        errors = {}
        if team_a is None:
            errors["team_a"] = "team_a was not found."
        if team_b is None:
            errors["team_b"] = "team_b was not found."
        if errors:
            raise serializers.ValidationError(errors)
        attrs["team_a_obj"] = team_a
        attrs["team_b_obj"] = team_b
        return attrs


class ComparisonResponseSerializer(serializers.Serializer):
    teams = serializers.DictField()
    comparison = serializers.DictField()
    metrics = serializers.DictField()
    profile_similarity = serializers.FloatField(allow_null=True)


class HeadToHeadResponseSerializer(serializers.Serializer):
    teams = serializers.DictField()
    history_available = serializers.BooleanField()
    message = serializers.CharField()
    matches = serializers.ListField(child=serializers.DictField(), required=False)
