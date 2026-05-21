from apps.common.constants import MAX_SIMULATION_RUNS, MIN_SIMULATION_RUNS
from apps.common.validators import ensure_range


def validate_runs(runs: int) -> int:
    return ensure_range(runs, field_name="runs", minimum=MIN_SIMULATION_RUNS, maximum=MAX_SIMULATION_RUNS)
