from apps.common.exceptions import ApiError


def validate_team_has_matches(team) -> None:
    if team.matches_overall <= 0:
        raise ApiError(
            "matches must be greater than 0 before per-game calculations.",
            code="NOT_ENOUGH_DATA",
            status_code=422,
        )
