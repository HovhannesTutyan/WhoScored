from __future__ import annotations

from apps.math_utils.monte_carlo import run_poisson_simulation


def build_simulation_result(lambda_a: float, lambda_b: float, runs: int) -> dict[str, object]:
    return run_poisson_simulation(lambda_a, lambda_b, runs)
