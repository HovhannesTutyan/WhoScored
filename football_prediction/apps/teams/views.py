from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.common.responses import success_response
from apps.players.serializers import PlayerListSerializer
from apps.players.services import build_team_player_impact_payload
from apps.teams.serializers import StrengthWeaknessSerializer, TeamDetailSerializer, TeamListSerializer, TeamPlayersSerializer, TeamStatsSerializer
from apps.teams.selectors import get_team, get_team_players, team_detail_queryset, team_list_queryset
from apps.teams.services import build_strengths_weaknesses_payload, build_team_stats_payload


class TeamViewSet(ReadOnlyModelViewSet):
    queryset = team_list_queryset()
    serializer_class = TeamListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            paginator = self.paginator.page.paginator
            meta = {
                "count": paginator.count,
                "page": self.paginator.page.number,
                "num_pages": paginator.num_pages,
            }
            return success_response(serializer.data, meta=meta)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return success_response(serializer.data)

    def get_queryset(self):
        if self.action in {"retrieve", "stats", "strengths_weaknesses", "players", "player_impact"}:
            return team_detail_queryset()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TeamDetailSerializer
        if self.action == "stats":
            return TeamStatsSerializer
        if self.action == "strengths_weaknesses":
            return StrengthWeaknessSerializer
        if self.action == "players":
            return TeamPlayersSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["get"], url_path="stats")
    def stats(self, request, pk=None):
        team = get_team(pk)
        serializer = self.get_serializer(build_team_stats_payload(team))
        return success_response(serializer.data)

    @action(detail=True, methods=["get"], url_path="strengths-weaknesses")
    def strengths_weaknesses(self, request, pk=None):
        team = get_team(pk)
        serializer = self.get_serializer(build_strengths_weaknesses_payload(team))
        return success_response(serializer.data)

    @action(detail=True, methods=["get"], url_path="players")
    def players(self, request, pk=None):
        team = get_team(pk)
        payload = {
            "team": {"id": team.id, "name": team.name},
            "players": PlayerListSerializer(get_team_players(team), many=True).data,
        }
        serializer = self.get_serializer(payload)
        return success_response(serializer.data)

    @action(detail=True, methods=["get"], url_path="player-impact")
    def player_impact(self, request, pk=None):
        team = get_team(pk)
        return success_response(build_team_player_impact_payload(team))
