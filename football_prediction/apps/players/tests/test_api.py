from rest_framework.test import APITestCase

from tests.factories import create_player, create_team


class PlayerApiTests(APITestCase):
    def setUp(self):
        self.team = create_team(name="Arsenal")
        self.player = create_player(self.team, name="Bukayo Saka")

    def test_list_players(self):
        response = self.client.get("/api/players/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])

    def test_player_stats_endpoint(self):
        response = self.client.get(f"/api/players/{self.player.id}/stats/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("impact", response.data["data"])
