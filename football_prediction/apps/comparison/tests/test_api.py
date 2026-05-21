from rest_framework.test import APITestCase

from tests.factories import create_goalkeeper_stat, create_player, create_team


class ComparisonApiTests(APITestCase):
    def setUp(self):
        self.team_a = create_team(name="Team A")
        self.team_b = create_team(name="Team B", points_overall=32, goals_for_overall=30, goals_against_overall=27, xg_for=28.0, xg_against=26.0)
        create_goalkeeper_stat(self.team_a)
        create_goalkeeper_stat(self.team_b)
        create_player(self.team_a, goals=6)
        create_player(self.team_b, goals=4)

    def test_compare_endpoint(self):
        response = self.client.get(f"/api/compare/?team_a={self.team_a.id}&team_b={self.team_b.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("comparison", response.data["data"])

    def test_same_team_validation_error(self):
        response = self.client.get(f"/api/compare/?team_a={self.team_a.id}&team_b={self.team_a.id}")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])

    def test_team_not_found_error(self):
        response = self.client.get(f"/api/compare/?team_a={self.team_a.id}&team_b=99999")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])
