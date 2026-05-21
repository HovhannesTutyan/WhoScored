from django.test import TestCase

from tests.factories import create_player, create_team


class PlayerModelTests(TestCase):
    def test_player_string_representation(self):
        team = create_team(name="Arsenal")
        player = create_player(team, name="Bukayo Saka")
        self.assertIn("Bukayo Saka", str(player))
