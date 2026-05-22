import React, { useMemo } from "react";
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

import { StatBar } from "@/components/StatBar";
import { TeamBadge } from "@/components/TeamCard";
import { useColors } from "@/hooks/useColors";
import { usePlayerDetailQuery } from "@/hooks/useFootballData";

function BigStat({ label, value, color, icon }: { label: string; value: string | number; color: string; icon: string }) {
  const colors = useColors();

  return (
    <View style={[styles.bigStat, { backgroundColor: colors.card, borderColor: colors.border }]}> 
      <MaterialCommunityIcons name={icon as never} size={20} color={color} />
      <Text style={[styles.bigStatValue, { color }]}>{value}</Text>
      <Text style={[styles.bigStatLabel, { color: colors.mutedForeground }]}>{label}</Text>
    </View>
  );
}

function HighlightItem({ label, value, color }: { label: string; value: string | number; color: string }) {
  const colors = useColors();

  return (
    <View style={styles.highlightItem}>
      <Text style={[styles.highlightValue, { color }]}>{value}</Text>
      <Text style={[styles.highlightLabel, { color: colors.mutedForeground }]}>{label}</Text>
    </View>
  );
}

function ImpactRow({ label, value, pct, color }: { label: string; value: string; pct: number; color: string }) {
  const colors = useColors();

  return (
    <View style={styles.impactRow}>
      <Text style={[styles.impactRowLabel, { color: colors.mutedForeground }]}>{label}</Text>
      <View style={[styles.impactRowTrack, { backgroundColor: colors.border }]}> 
        <View style={[styles.impactRowFill, { width: `${Math.max(0, Math.min(pct, 1)) * 100}%`, backgroundColor: color }]} />
      </View>
      <Text style={[styles.impactRowValue, { color }]}>{value}</Text>
    </View>
  );
}

function formatMetric(value: number | null | undefined, digits = 1) {
  if (value === null || value === undefined) {
    return null;
  }

  return Number(value.toFixed(digits));
}

export default function PlayerDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const playerId = Number(id);
  const { data, isLoading, error } = usePlayerDetailQuery(Number.isFinite(playerId) ? playerId : null);

  if (isLoading) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="progress-clock" size={36} color={colors.primary} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Loading player profile</Text>
      </View>
    );
  }

  if (error || !data) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="account-off-outline" size={36} color={colors.statRed} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Player not available</Text>
        <Text style={[styles.stateText, { color: colors.mutedForeground }]}> 
          {error instanceof Error ? error.message : "The player could not be loaded."}
        </Text>
      </View>
    );
  }

  const { player, team, rawStats, impact } = data;
  const impactColor =
    impact.totalPlayerImpact >= 10
      ? colors.gold
      : impact.totalPlayerImpact >= 5
      ? colors.primary
      : impact.totalPlayerImpact > 0
      ? colors.statBlue
      : colors.mutedForeground;
  const contribution = rawStats.goals + rawStats.assists;

  const highlightItems = useMemo(
    () => [
      rawStats.shotsPerGame !== null ? { label: "Shots / Game", value: rawStats.shotsPerGame.toFixed(1), color: colors.statGreen } : null,
      rawStats.aerialWonPerGame !== null ? { label: "Aerial Won / G", value: rawStats.aerialWonPerGame.toFixed(1), color: colors.accent } : null,
      rawStats.tackles !== null ? { label: "Tackles", value: rawStats.tackles.toFixed(1), color: colors.statOrange } : null,
      rawStats.fouls !== null ? { label: "Fouls", value: rawStats.fouls.toFixed(1), color: colors.statRed } : null,
      rawStats.dribbles !== null ? { label: "Dribbles", value: rawStats.dribbles.toFixed(1), color: colors.primary } : null,
      rawStats.saves !== null ? { label: "Saves", value: rawStats.saves.toFixed(1), color: colors.gold } : null,
      rawStats.goalsConceded !== null ? { label: "Goals Conceded", value: rawStats.goalsConceded.toFixed(1), color: colors.statRed } : null,
    ].filter((item): item is { label: string; value: string; color: string } => item !== null),
    [
      colors.accent,
      colors.gold,
      colors.primary,
      colors.statGreen,
      colors.statOrange,
      colors.statRed,
      rawStats.aerialWonPerGame,
      rawStats.dribbles,
      rawStats.fouls,
      rawStats.goalsConceded,
      rawStats.saves,
      rawStats.shotsPerGame,
      rawStats.tackles,
    ],
  );

  const metricBars = useMemo(
    () => [
      rawStats.shotsPerGame !== null ? { label: "Shots / Game", value: formatMetric(rawStats.shotsPerGame), maxValue: 6, color: colors.statGreen } : null,
      rawStats.aerialWonPerGame !== null ? { label: "Aerial Won / G", value: formatMetric(rawStats.aerialWonPerGame), maxValue: 5, color: colors.accent } : null,
      rawStats.tackles !== null ? { label: "Tackles", value: formatMetric(rawStats.tackles), maxValue: 5, color: colors.statOrange } : null,
      rawStats.fouls !== null ? { label: "Fouls", value: formatMetric(rawStats.fouls), maxValue: 4, color: colors.statRed } : null,
      rawStats.offsides !== null ? { label: "Offsides", value: formatMetric(rawStats.offsides), maxValue: 3, color: colors.primary } : null,
      rawStats.dribbles !== null ? { label: "Dribbles", value: formatMetric(rawStats.dribbles), maxValue: 5, color: colors.statBlue } : null,
      rawStats.saves !== null ? { label: "Saves", value: formatMetric(rawStats.saves), maxValue: 6, color: colors.gold } : null,
      rawStats.goalsConceded !== null ? { label: "Goals Conceded", value: formatMetric(rawStats.goalsConceded), maxValue: 3, color: colors.statRed } : null,
    ].filter((item): item is { label: string; value: number; maxValue: number; color: string } => item !== null && item.value !== null),
    [
      colors.accent,
      colors.gold,
      colors.primary,
      colors.statBlue,
      colors.statGreen,
      colors.statOrange,
      colors.statRed,
      rawStats.aerialWonPerGame,
      rawStats.dribbles,
      rawStats.fouls,
      rawStats.goalsConceded,
      rawStats.offsides,
      rawStats.saves,
      rawStats.shotsPerGame,
      rawStats.tackles,
    ],
  );

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
          <TeamBadge team={team} size={58} />
          <View style={styles.heroInfo}>
            <Text style={[styles.heroName, { color: colors.foreground }]}>{player.name}</Text>
            <Text style={[styles.teamName, { color: team.primaryColor }]}>{team.shortName}</Text>
            <Text style={[styles.heroMeta, { color: colors.mutedForeground }]}>Goals {rawStats.goals} · Assists {rawStats.assists} · Cards {rawStats.cards}</Text>
          </View>
          <View style={[styles.impactBadge, { borderColor: impactColor }]}> 
            <Text style={[styles.impactValue, { color: impactColor }]}>{impact.totalPlayerImpact.toFixed(1)}</Text>
            <Text style={[styles.impactLabel, { color: colors.mutedForeground }]}>IMPACT</Text>
          </View>
        </View>
      </View>

      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 30 }]}> 
        <View style={styles.bigStatsRow}>
          <BigStat label="Goals" value={rawStats.goals} color={colors.statGreen} icon="soccer" />
          <BigStat label="Assists" value={rawStats.assists} color={colors.statBlue} icon="handshake" />
          <BigStat label="Cards" value={rawStats.cards} color={colors.statOrange} icon="alert-circle-outline" />
          <BigStat label="Contrib" value={contribution} color={colors.gold} icon="chart-line" />
        </View>

        {highlightItems.length > 0 && (
          <View style={[styles.highlightCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>RAW STAT HIGHLIGHTS</Text>
            <View style={styles.highlightGrid}>
              {highlightItems.map((item) => (
                <HighlightItem key={item.label} label={item.label} value={item.value} color={item.color} />
              ))}
            </View>
          </View>
        )}

        {metricBars.length > 0 && (
          <View style={[styles.statsCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>AVAILABLE METRICS</Text>
            {metricBars.map((metric, index) => (
              <StatBar key={metric.label} label={metric.label} value={metric.value} maxValue={metric.maxValue} color={metric.color} delay={index * 80} />
            ))}
          </View>
        )}

        <View style={[styles.impactCard, { backgroundColor: colors.card, borderColor: impactColor + "55" }]}> 
          <Text style={[styles.sectionTitle, { color: colors.mutedForeground }]}>IMPACT BREAKDOWN</Text>
          <View style={styles.impactContent}>
            <View style={styles.impactLeft}>
              <View style={[styles.impactCircle, { borderColor: impactColor }]}> 
                <Text style={[styles.impactCircleValue, { color: impactColor }]}>{impact.totalPlayerImpact.toFixed(1)}</Text>
                <Text style={[styles.impactCircleLabel, { color: colors.mutedForeground }]}>total</Text>
              </View>
              <Text style={[styles.impactLevel, { color: impactColor }]}>
                {impact.totalPlayerImpact >= 10 ? "Elite" : impact.totalPlayerImpact >= 5 ? "High Impact" : impact.totalPlayerImpact > 0 ? "Positive" : "Limited"}
              </Text>
            </View>
            <View style={styles.impactRight}>
              <ImpactRow label="Attack" value={impact.attackImpact.toFixed(2)} pct={Math.abs(impact.attackImpact) / 20} color={colors.statGreen} />
              <ImpactRow label="Defense" value={impact.defensiveImpact.toFixed(2)} pct={Math.abs(impact.defensiveImpact) / 5} color={colors.statBlue} />
              <ImpactRow label="Discipline" value={impact.disciplineImpact.toFixed(2)} pct={Math.abs(impact.disciplineImpact) / 5} color={colors.statOrange} />
              <ImpactRow label="Goalkeeper" value={impact.goalkeeperImpact.toFixed(2)} pct={Math.abs(impact.goalkeeperImpact) / 5} color={colors.gold} />
            </View>
          </View>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  hero: { paddingHorizontal: 16, paddingBottom: 16, borderBottomWidth: 1 },
  backBtn: { width: 36, height: 36, alignItems: "center", justifyContent: "center", marginBottom: 6 },
  heroContent: { flexDirection: "row", alignItems: "center", gap: 12 },
  heroInfo: { flex: 1, gap: 5 },
  heroName: { fontSize: 18, fontFamily: "Inter_700Bold" },
  teamName: { fontSize: 12, fontFamily: "Inter_600SemiBold" },
  heroMeta: { fontSize: 12, fontFamily: "Inter_400Regular" },
  impactBadge: { width: 64, height: 64, borderRadius: 32, borderWidth: 2, alignItems: "center", justifyContent: "center" },
  impactValue: { fontSize: 18, fontFamily: "Inter_700Bold" },
  impactLabel: { fontSize: 8, fontFamily: "Inter_600SemiBold", letterSpacing: 0.5 },
  scroll: { padding: 16, gap: 16 },
  bigStatsRow: { flexDirection: "row", gap: 8 },
  bigStat: { flex: 1, borderRadius: 12, borderWidth: 1, padding: 10, alignItems: "center", gap: 3 },
  bigStatValue: { fontSize: 18, fontFamily: "Inter_700Bold" },
  bigStatLabel: { fontSize: 9, fontFamily: "Inter_500Medium" },
  highlightCard: { borderRadius: 14, borderWidth: 1, padding: 14 },
  sectionTitle: { fontSize: 10, fontFamily: "Inter_600SemiBold", letterSpacing: 1.5, marginBottom: 10 },
  highlightGrid: { flexDirection: "row", flexWrap: "wrap", gap: 12 },
  highlightItem: { width: "30%", gap: 2 },
  highlightValue: { fontSize: 18, fontFamily: "Inter_700Bold" },
  highlightLabel: { fontSize: 10, fontFamily: "Inter_400Regular" },
  statsCard: { borderRadius: 14, borderWidth: 1, padding: 16, gap: 4 },
  impactCard: { borderRadius: 14, borderWidth: 1, padding: 16 },
  impactContent: { flexDirection: "row", gap: 16, alignItems: "flex-start" },
  impactLeft: { alignItems: "center", gap: 8, width: 84 },
  impactCircle: { width: 74, height: 74, borderRadius: 37, borderWidth: 2.5, alignItems: "center", justifyContent: "center" },
  impactCircleValue: { fontSize: 22, fontFamily: "Inter_700Bold" },
  impactCircleLabel: { fontSize: 11, fontFamily: "Inter_500Medium" },
  impactLevel: { fontSize: 12, fontFamily: "Inter_700Bold", textAlign: "center" },
  impactRight: { flex: 1, gap: 10 },
  impactRow: { gap: 4 },
  impactRowLabel: { fontSize: 11, fontFamily: "Inter_500Medium" },
  impactRowTrack: { height: 4, borderRadius: 2, overflow: "hidden" },
  impactRowFill: { height: "100%", borderRadius: 2 },
  impactRowValue: { fontSize: 11, fontFamily: "Inter_600SemiBold" },
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