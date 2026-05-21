from __future__ import annotations


def build_head_to_head_response(team_a, team_b) -> dict[str, object]:
    return {
        "teams": {
            "team_a": {"id": team_a.id, "name": team_a.name},
            "team_b": {"id": team_b.id, "name": team_b.name},
        },
        "history_available": False,
        "message": "Not enough historical data.",
        "matches": [],
    }
