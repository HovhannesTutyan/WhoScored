from __future__ import annotations

from apps.statistics.player_impact_service import build_player_impact, build_team_player_impact


def build_player_stats_payload(player) -> dict[str, object]:
    return {
        "player": {
            "id": player.id,
            "name": player.name,
            "team": {
                "id": player.team_id,
                "name": player.team.name,
            },
        },
        "raw_stats": {
            "goals": player.goals,
            "assists": player.assists,
            "cards": player.cards,
            "shots_per_game": player.shots_per_game,
            "aerial_won_per_game": player.aerial_won_per_game,
            "tackles": player.tackles,
            "fouls": player.fouls,
            "offsides": player.offsides,
            "dribbles": player.dribbles,
            "goals_conceded": player.goals_conceded,
            "saves": player.saves,
        },
        "impact": build_player_impact(player),
    }


def build_team_player_impact_payload(team) -> dict[str, object]:
    payload = build_team_player_impact(team)
    payload["players"] = [
        {
            "id": item["player"].id,
            "name": item["player"].name,
            "team_id": item["player"].team_id,
            "attack_impact": item["attack_impact"],
            "defensive_impact": item["defensive_impact"],
            "discipline_impact": item["discipline_impact"],
            "goalkeeper_impact": item["goalkeeper_impact"],
            "total_player_impact": item["total_player_impact"],
        }
        for item in payload["players"]
    ]
    return payload
