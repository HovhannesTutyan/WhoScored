from django.urls import path

from apps.ratings.views import EloRatingDetailView, EloRatingsView, PowerRatingDetailView, PowerRatingsView

urlpatterns = [
    path("ratings/elo/", EloRatingsView.as_view(), name="ratings-elo"),
    path("ratings/elo/<int:team_id>/", EloRatingDetailView.as_view(), name="ratings-elo-detail"),
    path("ratings/power/", PowerRatingsView.as_view(), name="ratings-power"),
    path("ratings/power/<int:team_id>/", PowerRatingDetailView.as_view(), name="ratings-power-detail"),
]