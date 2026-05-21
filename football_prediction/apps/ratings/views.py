from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from apps.common.responses import success_response
from apps.ratings.elo_service import build_elo_rating_detail, build_elo_ratings
from apps.ratings.power_rating_service import build_power_rating, build_power_ratings
from apps.ratings.serializers import RatingsResponseSerializer
from apps.teams.models import Team


class EloRatingsView(APIView):
    def get(self, request):
        serializer = RatingsResponseSerializer(build_elo_ratings())
        return success_response(serializer.data)


class EloRatingDetailView(APIView):
    def get(self, request, team_id: int):
        team = get_object_or_404(Team, pk=team_id)
        serializer = RatingsResponseSerializer(build_elo_rating_detail(team))
        return success_response(serializer.data)


class PowerRatingsView(APIView):
    def get(self, request):
        serializer = RatingsResponseSerializer(build_power_ratings())
        return success_response(serializer.data)


class PowerRatingDetailView(APIView):
    def get(self, request, team_id: int):
        team = get_object_or_404(Team, pk=team_id)
        serializer = RatingsResponseSerializer(
            {
                "available": True,
                "team": {"id": team.id, "name": team.name},
                "ratings": [],
                "rating": build_power_rating(team)["power_rating"],
            }
        )
        return success_response(serializer.data)
