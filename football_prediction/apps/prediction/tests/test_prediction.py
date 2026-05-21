from django.test import TestCase

from apps.prediction.services import build_prediction_payload
from tests.factories import create_goalkeeper_stat, create_player, create_team


class PredictionServiceTests(TestCase):
    def test_build_prediction_payload(self):
        team_a = create_team(name="Team A", points_overall=45, goals_for_overall=40, goals_against_overall=18, xg_for=39.0, xg_against=19.0)
        team_b = create_team(name="Team B", points_overall=35, goals_for_overall=32, goals_against_overall=24, xg_for=30.0, xg_against=25.0)
        create_goalkeeper_stat(team_a)
        create_goalkeeper_stat(team_b)
        create_player(team_a, goals=9, assists=5)
        create_player(team_b, goals=6, assists=3)
        payload = build_prediction_payload(team_a, team_b)
        self.assertIn("overall_prediction", payload)
        self.assertIn("expected_goals", payload)
        self.assertIn("model_breakdown", payload)
