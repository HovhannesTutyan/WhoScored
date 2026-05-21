from __future__ import annotations

from apps.common.constants import REGRESSION_THRESHOLDS


def regression_risk_notes(derived_stats: dict[str, float | None]) -> list[str]:
    notes: list[str] = []
    attacking_overperformance = derived_stats.get("attacking_overperformance")
    defensive_overperformance = derived_stats.get("defensive_overperformance")

    if attacking_overperformance is not None and attacking_overperformance >= REGRESSION_THRESHOLDS["finishing_overperformance"]:
        notes.append("Team may be overperforming finishing quality.")
    if attacking_overperformance is not None and attacking_overperformance <= REGRESSION_THRESHOLDS["finishing_underperformance"]:
        notes.append("Team may be underperforming finishing quality.")
    if defensive_overperformance is not None and defensive_overperformance >= REGRESSION_THRESHOLDS["defensive_overperformance"]:
        notes.append("Team may be defensively overperforming or goalkeeper may be saving above expectation.")
    if defensive_overperformance is not None and defensive_overperformance <= REGRESSION_THRESHOLDS["defensive_underperformance"]:
        notes.append("Team may be allowing worse chances than the goals against column suggests.")
    return notes
