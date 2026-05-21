from rest_framework.test import APITestCase

from tests.factories import create_goalkeeper_stat, create_player, create_team


class PredictionApiTests(APITestCase):
    def setUp(self):
        self.team_a = create_team(name="Team A", points_overall=45, goals_for_overall=40, goals_against_overall=18, xg_for=39.0, xg_against=19.0)
        self.team_b = create_team(name="Team B", points_overall=35, goals_for_overall=32, goals_against_overall=24, xg_for=30.0, xg_against=25.0)
        create_goalkeeper_stat(self.team_a)
        create_goalkeeper_stat(self.team_b)
        create_player(self.team_a, goals=9, assists=4)
        create_player(self.team_b, goals=6, assists=2)

    def test_predict_endpoint(self):
        response = self.client.get(f"/api/predict/?team_a={self.team_a.id}&team_b={self.team_b.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("overall_prediction", response.data["data"])

    def test_predict_exact_score_endpoint(self):
        response = self.client.get(f"/api/predict/exact-score/?team_a={self.team_a.id}&team_b={self.team_b.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("most_likely_scores", response.data["data"])

    def test_predict_simulation_endpoint(self):
        response = self.client.get(f"/api/predict/simulation/?team_a={self.team_a.id}&team_b={self.team_b.id}&runs=1000")
        self.assertEqual(response.status_code, 200)
        self.assertIn("simulation", response.data["data"])

    def test_predict_same_team_error(self):
        response = self.client.get(f"/api/predict/?team_a={self.team_a.id}&team_b={self.team_a.id}")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])

    def test_predict_team_not_found_error(self):
        response = self.client.get(f"/api/predict/?team_a={self.team_a.id}&team_b=99999")
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data["success"])
