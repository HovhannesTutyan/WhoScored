from django.urls import path

from apps.prediction.views import (
    PredictBttsView,
    PredictExactScoreView,
    PredictModelBreakdownView,
    PredictOverUnderView,
    PredictProbabilitiesView,
    PredictSimulationView,
    PredictView,
)

urlpatterns = [
    path("predict/", PredictView.as_view(), name="predict"),
    path("predict/probabilities/", PredictProbabilitiesView.as_view(), name="predict-probabilities"),
    path("predict/exact-score/", PredictExactScoreView.as_view(), name="predict-exact-score"),
    path("predict/over-under/", PredictOverUnderView.as_view(), name="predict-over-under"),
    path("predict/btts/", PredictBttsView.as_view(), name="predict-btts"),
    path("predict/simulation/", PredictSimulationView.as_view(), name="predict-simulation"),
    path("predict/model-breakdown/", PredictModelBreakdownView.as_view(), name="predict-model-breakdown"),
]