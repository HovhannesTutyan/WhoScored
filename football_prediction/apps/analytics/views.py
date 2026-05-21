from rest_framework.views import APIView

from apps.analytics.serializers import AnalyticsResponseSerializer
from apps.analytics.services import build_correlation_report, build_feature_importance_report, build_league_averages_report
from apps.common.responses import success_response


class CorrelationView(APIView):
    def get(self, request):
        serializer = AnalyticsResponseSerializer({"result": build_correlation_report()})
        return success_response(serializer.data)


class FeatureImportanceView(APIView):
    def get(self, request):
        serializer = AnalyticsResponseSerializer({"result": build_feature_importance_report()})
        return success_response(serializer.data)


class LeagueAveragesView(APIView):
    def get(self, request):
        serializer = AnalyticsResponseSerializer({"result": build_league_averages_report()})
        return success_response(serializer.data)
