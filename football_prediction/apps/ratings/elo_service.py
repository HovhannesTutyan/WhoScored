from __future__ import annotations

from apps.ratings.selectors import rating_team_queryset


def build_elo_ratings() -> dict[str, object]:
    return {
        "available": False,
        "message": "Not enough historical data.",
        "ratings": [
            {
                "team": {"id": team.id, "name": team.name},
                "rating": None,
            }
            for team in rating_team_queryset()
        ],
    }


def build_elo_rating_detail(team) -> dict[str, object]:
    return {
        "available": False,
        "message": "Not enough historical data.",
        "team": {"id": team.id, "name": team.name},
        "rating": None,
    }
