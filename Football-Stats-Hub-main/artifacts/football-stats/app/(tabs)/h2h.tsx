import React, { useMemo, useState } from "react";
import {
  FlatList,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import * as Haptics from "expo-haptics";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { DualStatBar } from "@/components/StatBar";
import { TeamBadge, TeamCard } from "@/components/TeamCard";
import { useColors } from "@/hooks/useColors";
import { usePairInsightsQuery, useTeamsQuery } from "@/hooks/useFootballData";
import type { TeamSummary } from "@/lib/football-data";

function TeamSelectorModal({
  teams,
  visible,
  onSelect,
  onClose,
  exclude,
}: {
  teams: TeamSummary[];
  visible: boolean;
  onSelect: (team: TeamSummary) => void;
  onClose: () => void;
  exclude?: number;
}) {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const availableTeams = teams.filter((team) => team.id !== exclude);

  return (
    <Modal visible={visible} animationType="slide" presentationStyle="pageSheet" onRequestClose={onClose}>
      <View style={[styles.modal, { backgroundColor: colors.background }]}> 
        <View style={[styles.modalHandle, { backgroundColor: colors.border }]} />
        <Text style={[styles.modalTitle, { color: colors.foreground }]}>Select Club</Text>
        <FlatList
          data={availableTeams}
          keyExtractor={(team) => String(team.id)}
          contentContainerStyle={[styles.modalList, { paddingBottom: insets.bottom + 20 }]}
          showsVerticalScrollIndicator={false}
          renderItem={({ item }) => (
            <TeamCard
              team={item}
              compact
              onPress={() => {
                Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
                onSelect(item);
                onClose();
              }}
            />
          )}
        />
      </View>
    </Modal>
  );
}

function SelectorSlot({
  team,
  onPress,
}: {
  team: TeamSummary | null;
  onPress: () => void;
}) {
  const colors = useColors();

  return (
    <Pressable
      onPress={() => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        onPress();
      }}
      style={({ pressed }) => [
        styles.slot,
        {
          backgroundColor: team ? team.primaryColor + "18" : colors.card,
          borderColor: team ? team.primaryColor + "55" : colors.border,
          opacity: pressed ? 0.8 : 1,
        },
      ]}
    >
      {team ? (
        <>
          <TeamBadge team={team} size={44} />
          <Text style={[styles.slotName, { color: colors.foreground }]} numberOfLines={1}>
            {team.shortName}
          </Text>
          <Text style={[styles.slotPts, { color: team.primaryColor }]}>{team.stats.points} pts</Text>
        </>
      ) : (
        <>
          <View style={[styles.slotEmpty, { backgroundColor: colors.border }]}> 
            <MaterialCommunityIcons name="shield-plus-outline" size={26} color={colors.mutedForeground} />
          </View>
          <Text style={[styles.slotPlaceholder, { color: colors.mutedForeground }]}>Select Club</Text>
        </>
      )}
    </Pressable>
  );
}

function humanizeLabel(label: string) {
  return label.replace(/_/g, " ").replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function H2HScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { data: teams = [], isLoading, error } = useTeamsQuery();
  const [homeTeamId, setHomeTeamId] = useState<number | null>(null);
  const [awayTeamId, setAwayTeamId] = useState<number | null>(null);
  const [selectorFor, setSelectorFor] = useState<"home" | "away" | null>(null);
  const insightsQuery = usePairInsightsQuery(homeTeamId, awayTeamId);

  const headerTop = Platform.OS === "web" ? 67 : insets.top;
  const homeTeam = useMemo(() => teams.find((team) => team.id === homeTeamId) ?? null, [homeTeamId, teams]);
  const awayTeam = useMemo(() => teams.find((team) => team.id === awayTeamId) ?? null, [awayTeamId, teams]);

  const stats = useMemo(() => {
    if (!homeTeam || !awayTeam || !insightsQuery.data) {
      return null;
    }

    return [
      { label: "Points", home: homeTeam.stats.points, away: awayTeam.stats.points, suffix: "" },
      { label: "Goals Scored", home: homeTeam.stats.goalsFor, away: awayTeam.stats.goalsFor, suffix: "" },
      { label: "Goals Against", home: homeTeam.stats.goalsAgainst, away: awayTeam.stats.goalsAgainst, suffix: "" },
      { label: "xG", home: Number(homeTeam.stats.xG.toFixed(1)), away: Number(awayTeam.stats.xG.toFixed(1)), suffix: "" },
      {
        label: "Team Strength",
        home: Math.round(insightsQuery.data.comparison.metrics.teamA.teamStrength),
        away: Math.round(insightsQuery.data.comparison.metrics.teamB.teamStrength),
        suffix: "",
      },
      {
        label: "Attack Strength",
        home: Math.round(insightsQuery.data.comparison.metrics.teamA.attackStrength * 100),
        away: Math.round(insightsQuery.data.comparison.metrics.teamB.attackStrength * 100),
        suffix: "",
      },
      {
        label: "Player Impact",
        home: Number(insightsQuery.data.comparison.metrics.teamA.playerImpact.toFixed(2)),
        away: Number(insightsQuery.data.comparison.metrics.teamB.playerImpact.toFixed(2)),
        suffix: "",
      },
    ];
  }, [awayTeam, homeTeam, insightsQuery.data]);

  const homeAdvantage = insightsQuery.data ? Math.round(insightsQuery.data.prediction.overallPrediction.teamAWin * 100) : null;

  if (isLoading) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="progress-clock" size={36} color={colors.primary} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Loading clubs</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="server-network-off" size={36} color={colors.statRed} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Unable to load comparison data</Text>
        <Text style={[styles.stateText, { color: colors.mutedForeground }]}>{error instanceof Error ? error.message : "The API is not reachable."}</Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}> 
      <View style={[styles.header, { paddingTop: headerTop + 10, backgroundColor: colors.background, borderBottomColor: colors.border }]}> 
        <View style={styles.titleRow}>
          <MaterialCommunityIcons name="swap-horizontal-bold" size={22} color={colors.primary} />
          <Text style={[styles.title, { color: colors.foreground }]}>Head to Head</Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 100 }]} showsVerticalScrollIndicator={false}>
        <View style={styles.selectorRow}>
          <SelectorSlot team={homeTeam} onPress={() => setSelectorFor("home")} />
          <View style={[styles.vsCircle, { backgroundColor: colors.primary }]}> 
            <Text style={[styles.vsText, { color: colors.primaryForeground }]}>VS</Text>
          </View>
          <SelectorSlot team={awayTeam} onPress={() => setSelectorFor("away")} />
        </View>

        {homeTeam && awayTeam && insightsQuery.isLoading && (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="chart-box-outline" size={52} color={colors.primary} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Building comparison</Text>
          </View>
        )}

        {homeTeam && awayTeam && insightsQuery.error && (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="alert-circle-outline" size={52} color={colors.statRed} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Comparison unavailable</Text>
            <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}> 
              {insightsQuery.error instanceof Error ? insightsQuery.error.message : "The selected teams could not be compared."}
            </Text>
          </View>
        )}

        {homeTeam && awayTeam && insightsQuery.data && homeAdvantage !== null && (
          <View style={[styles.verdictCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <Text style={[styles.verdictTitle, { color: colors.mutedForeground }]}>MODEL ADVANTAGE</Text>
            <View style={styles.verdictBar}>
              <View style={[styles.verdictFillHome, { backgroundColor: homeTeam.primaryColor, width: `${homeAdvantage}%` }]} />
              <View style={[styles.verdictFillAway, { backgroundColor: awayTeam.primaryColor, width: `${100 - homeAdvantage}%` }]} />
            </View>
            <View style={styles.verdictLabels}>
              <Text style={[styles.verdictPct, { color: homeTeam.primaryColor }]}>{homeAdvantage}%</Text>
              <Text style={[styles.verdictTeams, { color: colors.mutedForeground }]}>{homeTeam.shortName} · {awayTeam.shortName}</Text>
              <Text style={[styles.verdictPct, { color: awayTeam.primaryColor }]}>{100 - homeAdvantage}%</Text>
            </View>
            <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}>Predicted winner: {insightsQuery.data.prediction.overallPrediction.predictedWinner}</Text>
          </View>
        )}

        {stats && homeTeam && awayTeam && (
          <View style={[styles.statsCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <View style={styles.statsTeamHeaders}>
              <Text style={[styles.statsTeamName, { color: homeTeam.primaryColor }]} numberOfLines={1}>{homeTeam.shortName}</Text>
              <Text style={[styles.statsTeamName, { color: awayTeam.primaryColor, textAlign: "right" }]} numberOfLines={1}>{awayTeam.shortName}</Text>
            </View>
            <View style={[styles.statsDivider, { backgroundColor: colors.border }]} />
            {stats.map((stat, index) => (
              <DualStatBar
                key={stat.label}
                label={stat.label}
                homeValue={stat.home}
                awayValue={stat.away}
                homeColor={homeTeam.primaryColor}
                awayColor={awayTeam.primaryColor}
                suffix={stat.suffix}
                delay={index * 60}
              />
            ))}
          </View>
        )}

        {homeTeam && awayTeam && insightsQuery.data && (
          <View style={[styles.statsCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <Text style={[styles.verdictTitle, { color: colors.mutedForeground }]}>CATEGORY WINNERS</Text>
            <View style={styles.insightGrid}>
              {Object.entries(insightsQuery.data.comparison.comparison).map(([label, winner]) => {
                const winnerColor =
                  winner === homeTeam.name
                    ? homeTeam.primaryColor
                    : winner === awayTeam.name
                    ? awayTeam.primaryColor
                    : colors.mutedForeground;

                return (
                  <View key={label} style={[styles.insightItem, { backgroundColor: colors.secondary, borderColor: colors.border }]}> 
                    <Text style={[styles.insightLabel, { color: colors.mutedForeground }]}>{humanizeLabel(label)}</Text>
                    <Text style={[styles.insightValue, { color: winnerColor }]}>{winner}</Text>
                  </View>
                );
              })}
            </View>
          </View>
        )}

        {homeTeam && awayTeam && insightsQuery.data && (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="history" size={36} color={colors.border} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Historical data</Text>
            <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}>{insightsQuery.data.headToHead.message}</Text>
          </View>
        )}

        {!homeTeam || !awayTeam ? (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="soccer-field" size={52} color={colors.border} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Compare any two clubs</Text>
            <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}>Select both clubs above to see a live API-backed comparison.</Text>
          </View>
        ) : null}
      </ScrollView>

      <TeamSelectorModal
        teams={teams}
        visible={selectorFor !== null}
        onSelect={(team) => {
          if (selectorFor === "home") {
            setHomeTeamId(team.id);
          } else {
            setAwayTeamId(team.id);
          }
        }}
        onClose={() => setSelectorFor(null)}
        exclude={selectorFor === "home" ? awayTeamId ?? undefined : homeTeamId ?? undefined}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { paddingHorizontal: 16, paddingBottom: 12, borderBottomWidth: 1, gap: 6 },
  titleRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  title: { fontSize: 22, fontFamily: "Inter_700Bold" },
  scroll: { padding: 16, gap: 16 },
  selectorRow: { flexDirection: "row", alignItems: "center", gap: 12, marginBottom: 4 },
  slot: {
    flex: 1,
    borderRadius: 14,
    borderWidth: 1,
    padding: 14,
    alignItems: "center",
    gap: 6,
  },
  slotName: { fontSize: 13, fontFamily: "Inter_600SemiBold", textAlign: "center" },
  slotPts: { fontSize: 12, fontFamily: "Inter_700Bold" },
  slotEmpty: { width: 44, height: 44, borderRadius: 22, alignItems: "center", justifyContent: "center" },
  slotPlaceholder: { fontSize: 12, fontFamily: "Inter_500Medium" },
  vsCircle: { width: 36, height: 36, borderRadius: 18, alignItems: "center", justifyContent: "center" },
  vsText: { fontSize: 11, fontFamily: "Inter_700Bold" },
  verdictCard: { borderRadius: 14, borderWidth: 1, padding: 14, gap: 10 },
  verdictTitle: { fontSize: 10, fontFamily: "Inter_600SemiBold", letterSpacing: 1.2, textAlign: "center" },
  verdictBar: { height: 8, borderRadius: 4, overflow: "hidden", flexDirection: "row" },
  verdictFillHome: { height: "100%" },
  verdictFillAway: { height: "100%" },
  verdictLabels: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  verdictPct: { fontSize: 16, fontFamily: "Inter_700Bold" },
  verdictTeams: { fontSize: 11, fontFamily: "Inter_400Regular" },
  statsCard: { borderRadius: 14, borderWidth: 1, padding: 16 },
  statsTeamHeaders: { flexDirection: "row", justifyContent: "space-between", marginBottom: 8 },
  statsTeamName: { fontSize: 14, fontFamily: "Inter_700Bold", flex: 1 },
  statsDivider: { height: 1, marginBottom: 14 },
  insightGrid: { gap: 8 },
  insightItem: { borderRadius: 12, borderWidth: 1, padding: 10, gap: 4 },
  insightLabel: { fontSize: 10, fontFamily: "Inter_500Medium", textTransform: "uppercase" },
  insightValue: { fontSize: 14, fontFamily: "Inter_700Bold" },
  emptyCard: {
    borderRadius: 16,
    borderWidth: 1,
    borderStyle: "dashed",
    padding: 32,
    alignItems: "center",
    gap: 12,
  },
  emptyTitle: { fontSize: 17, fontFamily: "Inter_600SemiBold", textAlign: "center" },
  emptySubtitle: { fontSize: 13, fontFamily: "Inter_400Regular", textAlign: "center" },
  modal: { flex: 1, paddingHorizontal: 16, paddingTop: 12 },
  modalHandle: { width: 40, height: 4, borderRadius: 2, alignSelf: "center", marginBottom: 16 },
  modalTitle: { fontSize: 20, fontFamily: "Inter_700Bold", marginBottom: 12 },
  modalList: { paddingTop: 4 },
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