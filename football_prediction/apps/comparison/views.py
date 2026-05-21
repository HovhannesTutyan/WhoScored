from rest_framework.views import APIView

from apps.common.responses import success_response
from apps.comparison.head_to_head_service import build_head_to_head_response
from apps.comparison.serializers import ComparisonResponseSerializer, HeadToHeadResponseSerializer, TeamPairQuerySerializer
from apps.comparison.services import build_comparison_summary, build_team_comparison


class CompareView(APIView):
    def get(self, request):
        serializer = TeamPairQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        payload = build_team_comparison(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"])
        output = ComparisonResponseSerializer(payload)
        return success_response(output.data)


class CompareSummaryView(APIView):
    def get(self, request):
        serializer = TeamPairQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        payload = build_comparison_summary(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"])
        output = ComparisonResponseSerializer(payload)
        return success_response(output.data)


class HeadToHeadView(APIView):
    def get(self, request):
        serializer = TeamPairQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        payload = build_head_to_head_response(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"])
        output = HeadToHeadResponseSerializer(payload)
        return success_response(output.data)
