from django.test import TestCase

from apps.comparison.services import build_team_comparison
from tests.factories import create_goalkeeper_stat, create_player, create_team


class ComparisonServiceTests(TestCase):
    def test_build_team_comparison(self):
        team_a = create_team(name="Team A", points_overall=45, goals_for_overall=40, goals_against_overall=20, xg_for=38.0, xg_against=22.0)
        team_b = create_team(name="Team B", points_overall=30, goals_for_overall=28, goals_against_overall=26, xg_for=24.0, xg_against=29.0)
        create_player(team_a, goals=10, assists=4)
        create_player(team_b, goals=3, assists=1)
        create_goalkeeper_stat(team_a, save_pct=76.0)
        create_goalkeeper_stat(team_b, save_pct=68.0)
        result = build_team_comparison(team_a, team_b)
        self.assertIn("comparison", result)
        self.assertIn("profile_similarity", result)
