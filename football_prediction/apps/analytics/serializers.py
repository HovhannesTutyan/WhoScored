from rest_framework import serializers


class AnalyticsResponseSerializer(serializers.Serializer):
    result = serializers.DictField()
