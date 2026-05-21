from __future__ import annotations

import math

from apps.common.constants import DEFAULT_MAX_GOALS, DEFAULT_OVER_UNDER_LINES
from apps.math_utils.probability import normalize_probability_map


def poisson_probability(lmbda: float, goals: int) -> float:
    if lmbda < 0 or goals < 0:
        return 0.0
    return (lmbda ** goals) * math.exp(-lmbda) / math.factorial(goals)


def goal_distribution(lmbda: float, max_goals: int = DEFAULT_MAX_GOALS) -> list[float]:
    distribution = [poisson_probability(lmbda, goals) for goals in range(max_goals + 1)]
    total = sum(distribution)
    if total == 0:
        return distribution
    return [value / total for value in distribution]


def score_matrix(lambda_a: float, lambda_b: float, max_goals: int = DEFAULT_MAX_GOALS) -> list[list[float]]:
    dist_a = goal_distribution(lambda_a, max_goals=max_goals)
    dist_b = goal_distribution(lambda_b, max_goals=max_goals)
    return [[goals_a * goals_b for goals_b in dist_b] for goals_a in dist_a]


def outcome_probabilities(matrix: list[list[float]]) -> dict[str, float]:
    team_a_win = 0.0
    draw = 0.0
    team_b_win = 0.0
    for goals_a, row in enumerate(matrix):
        for goals_b, probability in enumerate(row):
            if goals_a > goals_b:
                team_a_win += probability
            elif goals_a == goals_b:
                draw += probability
            else:
                team_b_win += probability
    return normalize_probability_map(
        {
            "team_a_win": team_a_win,
            "draw": draw,
            "team_b_win": team_b_win,
        }
    )


def most_likely_scorelines(matrix: list[list[float]], top_n: int = 5) -> list[dict[str, float | str]]:
    scorelines: list[tuple[str, float]] = []
    for goals_a, row in enumerate(matrix):
        for goals_b, probability in enumerate(row):
            scorelines.append((f"{goals_a}-{goals_b}", probability))
    scorelines.sort(key=lambda item: item[1], reverse=True)
    return [
        {"score": score, "probability": probability}
        for score, probability in scorelines[:top_n]
    ]


def over_under_probabilities(matrix: list[list[float]], lines: tuple[float, ...] = DEFAULT_OVER_UNDER_LINES) -> dict[str, float]:
    results: dict[str, float] = {}
    for line in lines:
        over_probability = 0.0
        under_probability = 0.0
        for goals_a, row in enumerate(matrix):
            for goals_b, probability in enumerate(row):
                total_goals = goals_a + goals_b
                if total_goals > line:
                    over_probability += probability
                else:
                    under_probability += probability
        normalized = normalize_probability_map({"over": over_probability, "under": under_probability})
        results[f"over_{str(line).replace('.', '_')}"] = normalized["over"]
        results[f"under_{str(line).replace('.', '_')}"] = normalized["under"]
    return results


def both_teams_to_score_probability(matrix: list[list[float]]) -> dict[str, float]:
    yes_probability = 0.0
    no_probability = 0.0
    for goals_a, row in enumerate(matrix):
        for goals_b, probability in enumerate(row):
            if goals_a > 0 and goals_b > 0:
                yes_probability += probability
            else:
                no_probability += probability
    return normalize_probability_map({"yes": yes_probability, "no": no_probability})


def clean_sheet_probabilities(matrix: list[list[float]]) -> dict[str, float]:
    team_a_clean_sheet = sum(matrix[goals_a][0] for goals_a in range(len(matrix)))
    team_b_clean_sheet = sum(matrix[0][goals_b] for goals_b in range(len(matrix[0])))
    return {
        "team_a": team_a_clean_sheet,
        "team_b": team_b_clean_sheet,
    }


def summarize_score_matrix(matrix: list[list[float]], top_n: int = 5) -> dict[str, object]:
    return {
        "outcomes": outcome_probabilities(matrix),
        "scorelines": most_likely_scorelines(matrix, top_n=top_n),
        "over_under": over_under_probabilities(matrix),
        "btts": both_teams_to_score_probability(matrix),
        "clean_sheets": clean_sheet_probabilities(matrix),
    }
