from __future__ import annotations

from collections import Counter

import numpy as np

from apps.common.constants import DEFAULT_OVER_UNDER_LINES


def run_poisson_simulation(lambda_a: float, lambda_b: float, runs: int, *, lines: tuple[float, ...] = DEFAULT_OVER_UNDER_LINES, top_n: int = 5) -> dict[str, object]:
    goals_a = np.random.poisson(lambda_a, runs)
    goals_b = np.random.poisson(lambda_b, runs)

    team_a_win = float(np.sum(goals_a > goals_b) / runs)
    draw = float(np.sum(goals_a == goals_b) / runs)
    team_b_win = float(np.sum(goals_a < goals_b) / runs)

    over_under: dict[str, float] = {}
    total_goals = goals_a + goals_b
    for line in lines:
        over = float(np.sum(total_goals > line) / runs)
        under = float(np.sum(total_goals <= line) / runs)
        line_key = str(line).replace('.', '_')
        over_under[f"over_{line_key}"] = over
        over_under[f"under_{line_key}"] = under

    btts_yes = float(np.sum((goals_a > 0) & (goals_b > 0)) / runs)
    btts_no = 1.0 - btts_yes

    score_counter = Counter(zip(goals_a.tolist(), goals_b.tolist(), strict=False))
    most_common = [
        {"score": f"{score_a}-{score_b}", "probability": count / runs}
        for (score_a, score_b), count in score_counter.most_common(top_n)
    ]

    return {
        "outcomes": {
            "team_a_win": team_a_win,
            "draw": draw,
            "team_b_win": team_b_win,
        },
        "scorelines": most_common,
        "over_under": over_under,
        "btts": {
            "yes": btts_yes,
            "no": btts_no,
        },
    }
