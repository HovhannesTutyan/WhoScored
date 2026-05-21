from __future__ import annotations

from apps.teams.models import Team
from apps.teams.selectors import team_detail_queryset


def get_team_pair(team_a_id: int, team_b_id: int) -> tuple[Team | None, Team | None]:
    teams = {team.id: team for team in team_detail_queryset().filter(id__in=[team_a_id, team_b_id])}
    return teams.get(team_a_id), teams.get(team_b_id)
