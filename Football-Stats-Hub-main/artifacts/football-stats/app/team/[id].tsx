import React from "react";
import {
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { useLocalSearchParams, useRouter } from "expo-router";
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { PlayerCard } from "@/components/PlayerCard";
import { StatBar } from "@/components/StatBar";
import { TeamBadge } from "@/components/TeamCard";
import { useColors } from "@/hooks/useColors";
import { useTeamDetailQuery } from "@/hooks/useFootballData";

function StatChip({ label, value, color }: { label: string; value: string | number; color?: string }) {
  const colors = useColors();

  return (
    <View style={[styles.statChip, { backgroundColor: colors.card, borderColor: colors.border }]}> 
      <Text style={[styles.statChipValue, { color: color ?? colors.primary }]}>{value}</Text>
      <Text style={[styles.statChipLabel, { color: colors.mutedForeground }]}>{label}</Text>
    </View>
  );
}

function InsightChip({ label, color }: { label: string; color: string }) {
  return (
    <View style={[styles.insightChip, { backgroundColor: color + "18", borderColor: color + "44" }]}> 
      <Text style={[styles.insightChipText, { color }]}>{label}</Text>
    </View>
  );
}

function roundValue(value: number, digits = 2) {
  return Number(value.toFixed(digits));
}

export default function TeamDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const teamId = Number(id);
  const { data, isLoading, error } = useTeamDetailQuery(Number.isFinite(teamId) ? teamId : null);

  if (isLoading) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="progress-clock" size={36} color={colors.primary} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Loading team profile</Text>
      </View>
    );
  }

  if (error || !data) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="shield-off-outline" size={36} color={colors.statRed} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Team not available</Text>
        <Text style={[styles.stateText, { color: colors.mutedForeground }]}> 
          {error instanceof Error ? error.message : "The team could not be loaded."}
        </Text>
      </View>
    );
  }

  const { team, derivedStats, attackAndDefense, teamStrength, playerImpact, goalkeeper, strengths, weaknesses, riskNotes, players } = data;
  const gd = team.stats.goalsFor - team.stats.goalsAgainst;
  const winRate = Math.round(derivedStats.winRate * 100);

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}> 
      <View
        style={[
          styles.hero,
          {
            paddingTop: insets.top + 8,
            backgroundColor: team.primaryColor + "18",
            borderBottomColor: team.primaryColor + "33",
          },
        ]}
      >
        <Pressable onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="chevron-back" size={22} color={colors.foreground} />
        </Pressable>
        <View style={styles.heroContent}>
          <TeamBadge team={team} size={68} />
          <View style={styles.heroInfo}>
            <Text style={[styles.heroName, { color: colors.foreground }]}>{team.name}</Text>
            <View style={styles.heroMeta}>
              <View style={[styles.leaguePill, { backgroundColor: team.primaryColor + "22" }]}> 
                <Text style={[styles.leaguePillText, { color: team.primaryColor }]}>{team.league}</Text>
              </View>
            </View>
            <View style={styles.heroRecord}>
              <Text style={[styles.heroRecordText, { color: colors.statGreen }]}>{team.stats.won}W</Text>
              <Text style={[styles.heroRecordSep, { color: colors.mutedForeground }]}>/</Text>
              <Text style={[styles.heroRecordText, { color: colors.statOrange }]}>{team.stats.drawn}D</Text>
              <Text style={[styles.heroRecordSep, { color: colors.mutedForeground }]}>/</Text>
              <Text style={[styles.heroRecordText, { color: colors.statRed }]}>{team.stats.lost}L</Text>
            </View>
          </View>
          <View style={[styles.ptsBadge, { backgroundColor: team.primaryColor }]}> 
            <Text style={[styles.ptsNumber, { color: "#fff" }]}>{team.stats.points}</Text>
            <Text style={[styles.ptsLabel, { color: "#ffffff99" }]}>PTS</Text>
          </View>
        </View>
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 30 }]}> 
        <View style={styles.chipGrid}>
          <StatChip label="Goals" value={team.stats.goalsFor} color={colors.statGreen} />
          <StatChip label="Conceded" value={team.stats.goalsAgainst} color={colors.statRed} />
          <StatChip label="GD" value={gd > 0 ? `+${gd}` : gd} color={gd >= 0 ? colors.statGreen : colors.statRed} />
          <StatChip label="Win Rate" value={`${winRate}%`} color={team.primaryColor} />
          <StatChip label="xG Diff" value={roundValue(derivedStats.xgDifferencePerGame)} color={colors.statOrange} />
          <StatChip label="Strength" value={Math.round(teamStrength.overallTeamStrength)} color={colors.accent} />
        </View>

        <View style={[styles.statsCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
          <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>LIVE TEAM METRICS</Text>
          <StatBar label="Points / Game" value={roundValue(derivedStats.pointsPerGame)} maxValue={3} color={team.primaryColor} delay={0} />
          <StatBar label="Goals / Game" value={roundValue(derivedStats.goalsForPerGame)} maxValue={4} color={colors.statGreen} delay={80} />
          <StatBar label="xG / Game" value={roundValue(derivedStats.xgForPerGame)} maxValue={4} color={colors.statOrange} delay={160} />
          <StatBar label="Overall Strength" value={Math.round(teamStrength.overallTeamStrength)} maxValue={100} color={colors.accent} delay={240} />
          <StatBar label="Attack Strength" value={Math.round(attackAndDefense.attackStrength * 100)} maxValue={150} color={colors.statBlue} delay={320} />
          <StatBar label="Finishing Efficiency" value={Math.round(derivedStats.finishingEfficiency * 100)} maxValue={150} color={colors.gold} suffix="%" delay={400} />
          {goalkeeper?.savePct !== null && goalkeeper?.savePct !== undefined && (
            <StatBar label="Goalkeeper Save %" value={Math.round(goalkeeper.savePct)} maxValue={100} color={colors.primary} suffix="%" delay={480} />
          )}
        </View>

        <View style={[styles.statsCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
          <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>SQUAD SIGNALS</Text>
          <Text style={[styles.noteText, { color: colors.foreground }]}>Average player impact: {playerImpact.averageTotalPlayerImpact.toFixed(2)}</Text>
          <Text style={[styles.noteText, { color: colors.foreground }]}>Players in sample: {playerImpact.playerCount}</Text>
          {playerImpact.warning ? (
            <Text style={[styles.noteText, { color: colors.mutedForeground }]}>{playerImpact.warning}</Text>
          ) : null}
          {goalkeeper ? (
            <Text style={[styles.noteText, { color: colors.mutedForeground }]}>Goalkeeper snapshot: {goalkeeper.season} · {goalkeeper.cleanSheets ?? 0} clean sheets · {goalkeeper.saves ?? 0} saves</Text>
          ) : null}
        </View>

        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>STRENGTHS</Text>
          <View style={styles.insightRow}>
            {strengths.length > 0 ? strengths.map((strength) => <InsightChip key={strength} label={strength} color={colors.statGreen} />) : <Text style={[styles.noteText, { color: colors.mutedForeground }]}>No strengths reported.</Text>}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>WEAKNESSES</Text>
          <View style={styles.insightRow}>
            {weaknesses.length > 0 ? weaknesses.map((weakness) => <InsightChip key={weakness} label={weakness} color={colors.statRed} />) : <Text style={[styles.noteText, { color: colors.mutedForeground }]}>No weaknesses reported.</Text>}
          </View>
        </View>

        {riskNotes.length > 0 && (
          <View style={[styles.statsCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>RISK NOTES</Text>
            {riskNotes.map((note) => (
              <Text key={note} style={[styles.noteText, { color: colors.mutedForeground }]}>• {note}</Text>
            ))}
          </View>
        )}

        {players.length > 0 && (
          <View style={styles.section}>
            <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>TOP PLAYERS</Text>
            {players.map((player) => (
              <PlayerCard key={player.id} player={player} team={team} onPress={() => router.push(`/player/${player.id}`)} />
            ))}
          </View>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  hero: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    borderBottomWidth: 1,
  },
  backBtn: {
    width: 36,
    height: 36,
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 6,
  },
  heroContent: {
    flexDirection: "row",
    alignItems: "center",
    gap: 14,
  },
  heroInfo: { flex: 1, gap: 6 },
  heroName: { fontSize: 20, fontFamily: "Inter_700Bold" },
  heroMeta: { flexDirection: "row" },
  leaguePill: { paddingHorizontal: 8, paddingVertical: 3, borderRadius: 6 },
  leaguePillText: { fontSize: 10, fontFamily: "Inter_600SemiBold" },
  heroRecord: { flexDirection: "row", gap: 4, alignItems: "center" },
  heroRecordText: { fontSize: 14, fontFamily: "Inter_700Bold" },
  heroRecordSep: { fontSize: 12, fontFamily: "Inter_400Regular" },
  ptsBadge: { width: 56, height: 56, borderRadius: 14, alignItems: "center", justifyContent: "center" },
  ptsNumber: { fontSize: 22, fontFamily: "Inter_700Bold" },
  ptsLabel: { fontSize: 9, fontFamily: "Inter_600SemiBold" },
  scroll: { padding: 16, gap: 16 },
  chipGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  statChip: {
    flex: 1,
    minWidth: "30%",
    borderRadius: 10,
    borderWidth: 1,
    padding: 10,
    alignItems: "center",
    gap: 2,
  },
  statChipValue: { fontSize: 18, fontFamily: "Inter_700Bold" },
  statChipLabel: { fontSize: 10, fontFamily: "Inter_500Medium" },
  section: { gap: 10 },
  sectionTitle: { fontSize: 10, fontFamily: "Inter_600SemiBold", letterSpacing: 1.5, marginBottom: 2 },
  statsCard: { borderRadius: 14, borderWidth: 1, padding: 16, gap: 8 },
  noteText: { fontSize: 12, fontFamily: "Inter_400Regular", lineHeight: 18 },
  insightRow: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  insightChip: {
    borderRadius: 999,
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 6,
  },
  insightChipText: { fontSize: 11, fontFamily: "Inter_500Medium" },
  state: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    gap: 10,
  },
  stateTitle: { fontSize: 18, fontFamily: "Inter_700Bold" },
  stateText: { fontSize: 13, fontFamily: "Inter_400Regular", textAlign: "center" },
});