from rest_framework.views import APIView

from apps.common.responses import success_response
from apps.prediction.serializers import PredictionOverUnderQuerySerializer, PredictionQuerySerializer, PredictionResponseSerializer, PredictionSimulationQuerySerializer
from apps.prediction.services import (
    build_btts_payload,
    build_exact_score_payload,
    build_model_breakdown_payload,
    build_over_under_payload,
    build_prediction_payload,
    build_probabilities_payload,
    build_simulation_payload,
)


class PredictView(APIView):
    def get(self, request):
        serializer = PredictionQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        payload = build_prediction_payload(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"])
        output = PredictionResponseSerializer(payload)
        return success_response(output.data)


class PredictProbabilitiesView(APIView):
    def get(self, request):
        serializer = PredictionQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return success_response(build_probabilities_payload(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"]))


class PredictExactScoreView(APIView):
    def get(self, request):
        serializer = PredictionQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return success_response(build_exact_score_payload(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"]))


class PredictOverUnderView(APIView):
    def get(self, request):
        serializer = PredictionOverUnderQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return success_response(
            build_over_under_payload(
                serializer.validated_data["team_a_obj"],
                serializer.validated_data["team_b_obj"],
                serializer.validated_data["line"],
            )
        )


class PredictBttsView(APIView):
    def get(self, request):
        serializer = PredictionQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return success_response(build_btts_payload(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"]))


class PredictSimulationView(APIView):
    def get(self, request):
        serializer = PredictionSimulationQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return success_response(
            build_simulation_payload(
                serializer.validated_data["team_a_obj"],
                serializer.validated_data["team_b_obj"],
                serializer.validated_data["runs"],
            )
        )


class PredictModelBreakdownView(APIView):
    def get(self, request):
        serializer = PredictionQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return success_response(build_model_breakdown_payload(serializer.validated_data["team_a_obj"], serializer.validated_data["team_b_obj"]))
