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

function SelectorSlot({ team, onPress, label }: { team: TeamSummary | null; onPress: () => void; label: string }) {
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
          <TeamBadge team={team} size={38} />
          <Text style={[styles.slotName, { color: colors.foreground }]} numberOfLines={1}>{team.shortName}</Text>
          <Text style={[styles.slotLeague, { color: colors.mutedForeground }]}>{team.league}</Text>
        </>
      ) : (
        <>
          <View style={[styles.slotEmpty, { backgroundColor: colors.border }]}> 
            <MaterialCommunityIcons name="shield-plus-outline" size={22} color={colors.mutedForeground} />
          </View>
          <Text style={[styles.slotPlaceholder, { color: colors.mutedForeground }]}>{label}</Text>
        </>
      )}
    </Pressable>
  );
}

function ScoreChip({ score, probability, color }: { score: string; probability: number; color: string }) {
  const colors = useColors();

  return (
    <View style={[styles.scoreChip, { backgroundColor: colors.card, borderColor: color + "44" }]}> 
      <Text style={[styles.scoreChipScore, { color }]}>{score}</Text>
      <Text style={[styles.scoreChipProb, { color: colors.mutedForeground }]}>{Math.round(probability * 100)}%</Text>
    </View>
  );
}

function InsightColumn({ title, items, color }: { title: string; items: string[]; color: string }) {
  const colors = useColors();

  return (
    <View style={styles.insightColumn}>
      <Text style={[styles.insightColumnTitle, { color }]}>{title}</Text>
      {items.length > 0 ? (
        items.map((item) => (
          <Text key={item} style={[styles.insightText, { color: colors.mutedForeground }]}>• {item}</Text>
        ))
      ) : (
        <Text style={[styles.insightText, { color: colors.mutedForeground }]}>No notes.</Text>
      )}
    </View>
  );
}

export default function PredictionScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const { data: teams = [], isLoading, error } = useTeamsQuery();
  const [teamAId, setTeamAId] = useState<number | null>(null);
  const [teamBId, setTeamBId] = useState<number | null>(null);
  const [selectorFor, setSelectorFor] = useState<"teamA" | "teamB" | null>(null);
  const insightsQuery = usePairInsightsQuery(teamAId, teamBId);

  const headerTop = Platform.OS === "web" ? 67 : insets.top;
  const teamA = useMemo(() => teams.find((team) => team.id === teamAId) ?? null, [teamAId, teams]);
  const teamB = useMemo(() => teams.find((team) => team.id === teamBId) ?? null, [teamBId, teams]);

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
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Unable to load predictions</Text>
        <Text style={[styles.stateText, { color: colors.mutedForeground }]}>{error instanceof Error ? error.message : "The API is not reachable."}</Text>
      </View>
    );
  }

  const prediction = insightsQuery.data?.prediction;
  const headToHeadMessage = insightsQuery.data?.headToHead.message ?? "Historical data is currently unavailable.";
  const overTwoFive = prediction?.overUnder.over_2_5 ?? null;
  const underTwoFive = prediction?.overUnder.under_2_5 ?? null;

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}> 
      <View style={[styles.header, { paddingTop: headerTop + 10, backgroundColor: colors.background, borderBottomColor: colors.border }]}> 
        <View style={styles.titleRow}>
          <MaterialCommunityIcons name="chart-timeline-variant" size={22} color={colors.primary} />
          <Text style={[styles.title, { color: colors.foreground }]}>Prediction Center</Text>
        </View>
      </View>

      <ScrollView contentContainerStyle={[styles.scroll, { paddingBottom: insets.bottom + 100 }]} showsVerticalScrollIndicator={false}>
        <View style={styles.selectorRow}>
          <SelectorSlot team={teamA} onPress={() => setSelectorFor("teamA")} label="Select home side" />
          <View style={[styles.vsCircle, { backgroundColor: colors.primary }]}> 
            <Text style={[styles.vsText, { color: colors.primaryForeground }]}>VS</Text>
          </View>
          <SelectorSlot team={teamB} onPress={() => setSelectorFor("teamB")} label="Select away side" />
        </View>

        {!teamA || !teamB ? (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="robot-happy-outline" size={48} color={colors.border} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Generate a live prediction</Text>
            <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}>Choose two clubs to replace the old mock results feed with real API predictions.</Text>
          </View>
        ) : null}

        {teamA && teamB && insightsQuery.isLoading && (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="progress-clock" size={48} color={colors.primary} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Running models</Text>
          </View>
        )}

        {teamA && teamB && insightsQuery.error && (
          <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <MaterialCommunityIcons name="alert-circle-outline" size={48} color={colors.statRed} />
            <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Prediction unavailable</Text>
            <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}>{insightsQuery.error instanceof Error ? insightsQuery.error.message : "The selected teams could not be scored."}</Text>
          </View>
        )}

        {teamA && teamB && prediction && (
          <>
            <View style={[styles.card, { backgroundColor: colors.card, borderColor: colors.border }]}> 
              <Text style={[styles.cardTitle, { color: colors.mutedForeground }]}>WIN PROBABILITIES</Text>
              <View style={styles.probabilityBar}>
                <View style={[styles.probabilitySegment, { width: `${prediction.overallPrediction.teamAWin * 100}%`, backgroundColor: teamA.primaryColor }]} />
                <View style={[styles.probabilitySegment, { width: `${prediction.overallPrediction.draw * 100}%`, backgroundColor: colors.statOrange }]} />
                <View style={[styles.probabilitySegment, { width: `${prediction.overallPrediction.teamBWin * 100}%`, backgroundColor: teamB.primaryColor }]} />
              </View>
              <View style={styles.probabilityLabels}>
                <Text style={[styles.probabilityText, { color: teamA.primaryColor }]}>{teamA.shortName} {Math.round(prediction.overallPrediction.teamAWin * 100)}%</Text>
                <Text style={[styles.probabilityText, { color: colors.statOrange }]}>Draw {Math.round(prediction.overallPrediction.draw * 100)}%</Text>
                <Text style={[styles.probabilityText, { color: teamB.primaryColor }]}>{teamB.shortName} {Math.round(prediction.overallPrediction.teamBWin * 100)}%</Text>
              </View>
              <Text style={[styles.summaryText, { color: colors.foreground }]}>Predicted winner: {prediction.overallPrediction.predictedWinner}</Text>
              <Text style={[styles.summarySubtext, { color: colors.mutedForeground }]}>Confidence: {prediction.overallPrediction.confidenceLevel} ({prediction.overallPrediction.confidenceScore.toFixed(1)})</Text>
            </View>

            <View style={[styles.card, { backgroundColor: colors.card, borderColor: colors.border }]}> 
              <Text style={[styles.cardTitle, { color: colors.mutedForeground }]}>EXPECTED GOALS</Text>
              <View style={styles.expectedGoalsRow}>
                <View style={styles.expectedGoalItem}>
                  <Text style={[styles.expectedGoalLabel, { color: colors.mutedForeground }]}>{teamA.shortName}</Text>
                  <Text style={[styles.expectedGoalValue, { color: teamA.primaryColor }]}>{prediction.expectedGoals.teamA.toFixed(2)}</Text>
                </View>
                <View style={styles.expectedGoalItem}>
                  <Text style={[styles.expectedGoalLabel, { color: colors.mutedForeground }]}>{teamB.shortName}</Text>
                  <Text style={[styles.expectedGoalValue, { color: teamB.primaryColor }]}>{prediction.expectedGoals.teamB.toFixed(2)}</Text>
                </View>
              </View>
            </View>

            <View style={[styles.card, { backgroundColor: colors.card, borderColor: colors.border }]}> 
              <Text style={[styles.cardTitle, { color: colors.mutedForeground }]}>MOST LIKELY SCORES</Text>
              <View style={styles.scoreChipRow}>
                {prediction.mostLikelyScores.slice(0, 3).map((scoreline) => (
                  <ScoreChip key={scoreline.score} score={scoreline.score} probability={scoreline.probability} color={colors.primary} />
                ))}
              </View>
            </View>

            <View style={[styles.card, { backgroundColor: colors.card, borderColor: colors.border }]}> 
              <Text style={[styles.cardTitle, { color: colors.mutedForeground }]}>MARKET SNAPSHOT</Text>
              <View style={styles.marketRow}>
                <View style={[styles.marketTile, { backgroundColor: colors.secondary }]}> 
                  <Text style={[styles.marketLabel, { color: colors.mutedForeground }]}>BTTS Yes</Text>
                  <Text style={[styles.marketValue, { color: colors.primary }]}>{Math.round(prediction.bothTeamsToScore.yes * 100)}%</Text>
                </View>
                <View style={[styles.marketTile, { backgroundColor: colors.secondary }]}> 
                  <Text style={[styles.marketLabel, { color: colors.mutedForeground }]}>Over 2.5</Text>
                  <Text style={[styles.marketValue, { color: colors.statOrange }]}>{overTwoFive === null ? "--" : `${Math.round(overTwoFive * 100)}%`}</Text>
                </View>
                <View style={[styles.marketTile, { backgroundColor: colors.secondary }]}> 
                  <Text style={[styles.marketLabel, { color: colors.mutedForeground }]}>Under 2.5</Text>
                  <Text style={[styles.marketValue, { color: colors.statBlue }]}>{underTwoFive === null ? "--" : `${Math.round(underTwoFive * 100)}%`}</Text>
                </View>
              </View>
            </View>

            <View style={[styles.card, { backgroundColor: colors.card, borderColor: colors.border }]}> 
              <Text style={[styles.cardTitle, { color: colors.mutedForeground }]}>TEAM NOTES</Text>
              <View style={styles.insightRow}>
                <InsightColumn title={teamA.shortName} items={prediction.strengths.teamA.concat(prediction.weaknesses.teamA)} color={teamA.primaryColor} />
                <InsightColumn title={teamB.shortName} items={prediction.strengths.teamB.concat(prediction.weaknesses.teamB)} color={teamB.primaryColor} />
              </View>
              {prediction.riskNotes.length > 0 && (
                <View style={[styles.riskBox, { backgroundColor: colors.secondary }]}> 
                  <Text style={[styles.marketLabel, { color: colors.mutedForeground }]}>Risk Notes</Text>
                  {prediction.riskNotes.map((note) => (
                    <Text key={note} style={[styles.insightText, { color: colors.mutedForeground }]}>• {note}</Text>
                  ))}
                </View>
              )}
            </View>

            <View style={[styles.emptyCard, { backgroundColor: colors.card, borderColor: colors.border }]}> 
              <MaterialCommunityIcons name="history" size={36} color={colors.border} />
              <Text style={[styles.emptyTitle, { color: colors.foreground }]}>Historical fixtures</Text>
              <Text style={[styles.emptySubtitle, { color: colors.mutedForeground }]}>{headToHeadMessage}</Text>
            </View>
          </>
        )}
      </ScrollView>

      <TeamSelectorModal
        teams={teams}
        visible={selectorFor !== null}
        onSelect={(team) => {
          if (selectorFor === "teamA") {
            setTeamAId(team.id);
          } else {
            setTeamBId(team.id);
          }
        }}
        onClose={() => setSelectorFor(null)}
        exclude={selectorFor === "teamA" ? teamBId ?? undefined : teamAId ?? undefined}
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
  slotLeague: { fontSize: 11, fontFamily: "Inter_400Regular", textAlign: "center" },
  slotEmpty: { width: 44, height: 44, borderRadius: 22, alignItems: "center", justifyContent: "center" },
  slotPlaceholder: { fontSize: 12, fontFamily: "Inter_500Medium" },
  vsCircle: { width: 36, height: 36, borderRadius: 18, alignItems: "center", justifyContent: "center" },
  vsText: { fontSize: 11, fontFamily: "Inter_700Bold" },
  card: { borderRadius: 14, borderWidth: 1, padding: 16, gap: 12 },
  cardTitle: { fontSize: 10, fontFamily: "Inter_600SemiBold", letterSpacing: 1.2 },
  probabilityBar: { height: 10, borderRadius: 5, overflow: "hidden", flexDirection: "row" },
  probabilitySegment: { height: "100%" },
  probabilityLabels: { flexDirection: "row", justifyContent: "space-between", gap: 8 },
  probabilityText: { fontSize: 12, fontFamily: "Inter_600SemiBold" },
  summaryText: { fontSize: 16, fontFamily: "Inter_700Bold" },
  summarySubtext: { fontSize: 12, fontFamily: "Inter_400Regular" },
  expectedGoalsRow: { flexDirection: "row", gap: 12 },
  expectedGoalItem: { flex: 1, gap: 4 },
  expectedGoalLabel: { fontSize: 11, fontFamily: "Inter_500Medium" },
  expectedGoalValue: { fontSize: 28, fontFamily: "Inter_700Bold" },
  scoreChipRow: { flexDirection: "row", gap: 10, flexWrap: "wrap" },
  scoreChip: { borderRadius: 12, borderWidth: 1, paddingHorizontal: 14, paddingVertical: 12, minWidth: 88, alignItems: "center", gap: 4 },
  scoreChipScore: { fontSize: 20, fontFamily: "Inter_700Bold" },
  scoreChipProb: { fontSize: 11, fontFamily: "Inter_500Medium" },
  marketRow: { flexDirection: "row", gap: 10 },
  marketTile: { flex: 1, borderRadius: 12, padding: 12, gap: 6 },
  marketLabel: { fontSize: 10, fontFamily: "Inter_500Medium", textTransform: "uppercase" },
  marketValue: { fontSize: 20, fontFamily: "Inter_700Bold" },
  insightRow: { flexDirection: "row", gap: 12 },
  insightColumn: { flex: 1, gap: 6 },
  insightColumnTitle: { fontSize: 13, fontFamily: "Inter_700Bold" },
  insightText: { fontSize: 12, fontFamily: "Inter_400Regular", lineHeight: 18 },
  riskBox: { borderRadius: 12, padding: 12, gap: 4 },
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