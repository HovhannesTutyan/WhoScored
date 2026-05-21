from django.test import TestCase

from apps.teams.services import build_team_stats_payload
from tests.factories import create_goalkeeper_stat, create_player, create_team


class TeamServiceTests(TestCase):
    def test_build_team_stats_payload(self):
        team = create_team(name="Arsenal")
        create_goalkeeper_stat(team)
        create_player(team, name="Bukayo Saka")
        payload = build_team_stats_payload(team)
        self.assertIn("derived_stats", payload)
        self.assertIn("goalkeeper", payload)
