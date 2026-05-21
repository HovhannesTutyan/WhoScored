from django.test import TestCase

from tests.factories import create_goalkeeper_stat, create_team


class TeamModelTests(TestCase):
    def test_team_string_representation(self):
        team = create_team(name="Arsenal")
        self.assertEqual(str(team), "Arsenal")

    def test_goalkeeper_stat_string_representation(self):
        team = create_team(name="Arsenal")
        goalkeeper = create_goalkeeper_stat(team)
        self.assertIn("Arsenal", str(goalkeeper))
