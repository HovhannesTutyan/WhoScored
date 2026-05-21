from __future__ import annotations

from apps.common.constants import STRENGTH_THRESHOLDS
from apps.math_utils.regression import regression_risk_notes
from apps.statistics.player_impact_service import build_team_player_impact
from apps.statistics.services import build_attack_and_defense_strength, build_team_derived_stats


def build_strengths_and_weaknesses(team) -> dict[str, list[str]]:
    strengths: list[str] = []
    weaknesses: list[str] = []

    derived_stats = build_team_derived_stats(team)
    attack_defense = build_attack_and_defense_strength(team)
    player_impact = build_team_player_impact(team)
    goalkeeper_stat = team.goalkeeper_stats.order_by("-updated_at").first()

    attack_strength = attack_defense.get("attack_strength") or 0.0
    defense_weakness = attack_defense.get("defense_weakness") or 0.0
    xg_attack_strength = attack_defense.get("xg_attack_strength") or 0.0
    xg_defense_weakness = attack_defense.get("xg_defense_weakness") or 0.0
    discipline_impact = player_impact.get("average_discipline_impact", 0.0)
    goalkeeper_impact = 0.0
    if goalkeeper_stat is not None:
        goalkeeper_impact = (float(goalkeeper_stat.saves or 0) * 0.4) - (float(goalkeeper_stat.ga or 0) * 0.4)

    if attack_strength >= STRENGTH_THRESHOLDS["elite_attack"]:
        strengths.append("elite attack")
    if attack_strength <= STRENGTH_THRESHOLDS["weak_attack"]:
        weaknesses.append("weak attack")
    if defense_weakness <= STRENGTH_THRESHOLDS["strong_defense"]:
        strengths.append("strong defense")
    if defense_weakness >= STRENGTH_THRESHOLDS["weak_defense"]:
        weaknesses.append("weak defense")
    if xg_attack_strength >= STRENGTH_THRESHOLDS["strong_xg_profile"] and xg_defense_weakness <= 1.0:
        strengths.append("strong xG profile")
    if xg_attack_strength <= STRENGTH_THRESHOLDS["poor_xg_profile"] or xg_defense_weakness >= 1.15:
        weaknesses.append("poor xG profile")
    if discipline_impact <= STRENGTH_THRESHOLDS["discipline_risk"]:
        weaknesses.append("discipline risk")
    if goalkeeper_impact >= STRENGTH_THRESHOLDS["goalkeeper_strength"]:
        strengths.append("goalkeeper strength")
    if goalkeeper_impact <= STRENGTH_THRESHOLDS["goalkeeper_weakness"]:
        weaknesses.append("goalkeeper weakness")
    if (derived_stats.get("attacking_overperformance") or 0.0) > 0:
        strengths.append("finishing overperformance")
    if (derived_stats.get("attacking_overperformance") or 0.0) < 0:
        weaknesses.append("finishing underperformance")
    if (derived_stats.get("defensive_overperformance") or 0.0) > 0:
        weaknesses.append("defensive regression risk")

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "risk_notes": regression_risk_notes(derived_stats),
    }
