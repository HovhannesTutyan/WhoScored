from django.test import TestCase

from apps.players.services import build_player_stats_payload
from tests.factories import create_player, create_team


class PlayerServiceTests(TestCase):
    def test_build_player_stats_payload(self):
        team = create_team(name="Arsenal")
        player = create_player(team, name="Bukayo Saka")
        payload = build_player_stats_payload(player)
        self.assertIn("impact", payload)
        self.assertEqual(payload["player"]["name"], "Bukayo Saka")
