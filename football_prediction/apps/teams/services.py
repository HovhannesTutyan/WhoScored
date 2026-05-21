from __future__ import annotations

from apps.players.services import build_team_player_impact_payload
from apps.statistics.services import build_attack_and_defense_strength, build_team_derived_stats
from apps.statistics.strengths_weaknesses_service import build_strengths_and_weaknesses
from apps.statistics.team_strength_service import build_team_strength
from apps.teams.selectors import get_latest_goalkeeper_stat


def _build_goalkeeper_payload(team) -> dict[str, object] | None:
    goalkeeper = get_latest_goalkeeper_stat(team)
    if goalkeeper is None:
        return None
    return {
        "team_id": team.id,
        "team_name": team.name,
        "league_name": goalkeeper.league_name,
        "season": goalkeeper.season,
        "ga": goalkeeper.ga,
        "save_pct": goalkeeper.save_pct,
        "cs": goalkeeper.cs,
        "psxg_net": goalkeeper.psxg_net,
        "saves": goalkeeper.saves,
    }


def build_team_stats_payload(team) -> dict[str, object]:
    return {
        "team": {
            "id": team.id,
            "name": team.name,
            "league_name": team.league_name,
        },
        "derived_stats": build_team_derived_stats(team),
        "attack_and_defense": build_attack_and_defense_strength(team),
        "team_strength": build_team_strength(team),
        "player_impact": build_team_player_impact_payload(team),
        "goalkeeper": _build_goalkeeper_payload(team),
    }


def build_strengths_weaknesses_payload(team) -> dict[str, object]:
    analysis = build_strengths_and_weaknesses(team)
    return {
        "team": {
            "id": team.id,
            "name": team.name,
        },
        **analysis,
    }
