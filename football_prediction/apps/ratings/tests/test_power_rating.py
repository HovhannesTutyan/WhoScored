from django.test import TestCase

from apps.ratings.power_rating_service import build_power_rating
from tests.factories import create_goalkeeper_stat, create_player, create_team


class PowerRatingTests(TestCase):
    def test_build_power_rating(self):
        team_a = create_team(name="Team A")
        team_b = create_team(name="Team B", points_overall=32, goals_for_overall=28, goals_against_overall=24, xg_for=26.0, xg_against=24.0)
        create_goalkeeper_stat(team_a)
        create_goalkeeper_stat(team_b)
        create_player(team_a, goals=8)
        create_player(team_b, goals=4)
        rating = build_power_rating(team_a)
        self.assertIn("power_rating", rating)
        self.assertGreaterEqual(rating["power_rating"], 0)
