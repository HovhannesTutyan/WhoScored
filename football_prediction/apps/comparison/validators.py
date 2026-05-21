from apps.common.exceptions import ApiError


def validate_distinct_teams(team_a_id: int, team_b_id: int) -> None:
    if team_a_id == team_b_id:
        raise ApiError("team_a and team_b must be different.", code="VALIDATION_ERROR")
