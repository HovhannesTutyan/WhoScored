from apps.common.exceptions import ApiError


def validate_player_has_team(player) -> None:
    if player.team_id is None:
        raise ApiError("Player is not linked to a team.", code="VALIDATION_ERROR")
