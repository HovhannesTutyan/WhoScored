from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action

from apps.common.responses import success_response
from apps.players.serializers import PlayerDetailSerializer, PlayerListSerializer, PlayerStatsSerializer
from apps.players.selectors import get_player, player_list_queryset
from apps.players.services import build_player_stats_payload


class PlayerViewSet(ReadOnlyModelViewSet):
    queryset = player_list_queryset()
    serializer_class = PlayerListSerializer

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

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayerDetailSerializer
        if self.action == "stats":
            return PlayerStatsSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["get"], url_path="stats")
    def stats(self, request, pk=None):
        player = get_player(pk)
        payload = build_player_stats_payload(player)
        serializer = self.get_serializer(payload)
        return success_response(serializer.data)
