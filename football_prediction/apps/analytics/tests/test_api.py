from rest_framework.test import APITestCase

from tests.factories import create_team


class AnalyticsApiTests(APITestCase):
    def setUp(self):
        create_team(name="Team A", league_name="Premier League")
        create_team(name="Team B", league_name="Premier League", points_overall=32, goals_for_overall=28, goals_against_overall=24, xg_for=26.0, xg_against=24.0)
        create_team(name="Team C", league_name="LaLiga", points_overall=42, goals_for_overall=37, goals_against_overall=18, xg_for=35.0, xg_against=20.0)

    def test_league_averages_endpoint(self):
        response = self.client.get("/api/analytics/league-averages/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.data["data"])
