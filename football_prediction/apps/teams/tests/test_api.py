from rest_framework.test import APITestCase

from tests.factories import create_goalkeeper_stat, create_player, create_team


class TeamApiTests(APITestCase):
    def setUp(self):
        self.team = create_team(name="Arsenal")
        create_goalkeeper_stat(self.team)
        create_player(self.team, name="Bukayo Saka")

    def test_list_teams(self):
        response = self.client.get("/api/teams/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["success"])

    def test_team_stats_endpoint(self):
        response = self.client.get(f"/api/teams/{self.team.id}/stats/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("derived_stats", response.data["data"])

    def test_team_players_endpoint(self):
        response = self.client.get(f"/api/teams/{self.team.id}/players/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]["players"]), 1)
