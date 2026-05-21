from rest_framework import serializers


class RatingsResponseSerializer(serializers.Serializer):
    available = serializers.BooleanField()
    message = serializers.CharField(required=False)
    ratings = serializers.ListField(child=serializers.DictField(), required=False)
    team = serializers.DictField(required=False)
    rating = serializers.FloatField(required=False, allow_null=True)
