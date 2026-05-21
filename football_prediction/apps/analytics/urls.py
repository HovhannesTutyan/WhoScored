from django.urls import path

from apps.analytics.views import CorrelationView, FeatureImportanceView, LeagueAveragesView

urlpatterns = [
    path("analytics/correlation/", CorrelationView.as_view(), name="analytics-correlation"),
    path("analytics/feature-importance/", FeatureImportanceView.as_view(), name="analytics-feature-importance"),
    path("analytics/league-averages/", LeagueAveragesView.as_view(), name="analytics-league-averages"),
]