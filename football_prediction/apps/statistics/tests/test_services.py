from django.test import TestCase

from apps.statistics.player_impact_service import build_player_impact
from apps.statistics.strengths_weaknesses_service import build_strengths_and_weaknesses
from apps.statistics.team_strength_service import build_team_strength
from tests.factories import create_goalkeeper_stat, create_player, create_team


class StatisticsServiceTests(TestCase):
    def test_player_impact_service(self):
        team = create_team()
        player = create_player(team, goals=10, assists=5, shots_per_game=2.0, dribbles=1.5)
        result = build_player_impact(player)
        self.assertGreater(result["attack_impact"], 0)
        self.assertIn("total_player_impact", result)

    def test_team_strength_service(self):
        team_a = create_team(name="Team A", points_overall=45, goals_for_overall=40, goals_against_overall=18, xg_for=36.0, xg_against=18.0)
        team_b = create_team(name="Team B", points_overall=25, wins_overall=7, losses_overall=8, goals_for_overall=24, goals_against_overall=28, xg_for=22.0, xg_against=27.0)
        create_player(team_a, goals=8, assists=6)
        create_player(team_b, goals=2, assists=1)
        strength_a = build_team_strength(team_a)
        strength_b = build_team_strength(team_b)
        self.assertGreater(strength_a["overall_team_strength"], strength_b["overall_team_strength"])

    def test_strengths_and_weaknesses_service(self):
        team = create_team(name="Strong Team", goals_for_overall=45, goals_against_overall=16, xg_for=38.0, xg_against=18.0)
        create_player(team, goals=9, assists=4)
        create_goalkeeper_stat(team, saves=70, ga=16)
        result = build_strengths_and_weaknesses(team)
        self.assertIn("strengths", result)
        self.assertIn("weaknesses", result)
        self.assertIn("risk_notes", result)
