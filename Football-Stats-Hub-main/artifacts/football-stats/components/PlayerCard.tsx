import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import * as Haptics from "expo-haptics";
import { MaterialCommunityIcons } from "@expo/vector-icons";

import { TeamBadge } from "@/components/TeamCard";
import { useColors } from "@/hooks/useColors";
import type { PlayerSummary, TeamSummary } from "@/lib/football-data";

interface PlayerCardProps {
  player: PlayerSummary;
  team: TeamSummary;
  onPress: () => void;
}

function ImpactCircle({ value }: { value: number | null }) {
  const colors = useColors();
  const impactValue = value ?? 0;
  const color =
    impactValue >= 10
      ? colors.gold
      : impactValue >= 5
      ? colors.primary
      : impactValue > 0
      ? colors.statBlue
      : colors.mutedForeground;
  const label =
    value === null
      ? "N/A"
      : impactValue >= 10
      ? "Elite"
      : impactValue >= 5
      ? "High"
      : impactValue > 0
      ? "Live"
      : "Low";

  return (
    <View style={[styles.impactCircle, { borderColor: color }]}> 
      <Text style={[styles.impactValue, { color }]}>{value === null ? "--" : value.toFixed(1)}</Text>
      <Text style={[styles.impactLabel, { color: colors.mutedForeground }]}>{label}</Text>
    </View>
  );
}

export function PlayerCard({ player, team, onPress }: PlayerCardProps) {
  const colors = useColors();

  return (
    <Pressable
      onPress={() => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        onPress();
      }}
      style={({ pressed }) => [
        styles.card,
        {
          backgroundColor: colors.card,
          borderColor: colors.border,
          opacity: pressed ? 0.85 : 1,
        },
      ]}
    >
      <View style={styles.top}>
        <View style={styles.left}>
          <TeamBadge team={team} size={40} />
          <View style={styles.info}>
            <Text style={[styles.name, { color: colors.foreground }]} numberOfLines={1}>
              {player.name}
            </Text>
            <Text style={[styles.teamName, { color: team.primaryColor }]}>{team.shortName}</Text>
            <Text style={[styles.meta, { color: colors.mutedForeground }]}>Goals {player.goals} · Assists {player.assists} · Cards {player.cards}</Text>
          </View>
        </View>
        <ImpactCircle value={player.impact} />
      </View>
      <View style={[styles.divider, { backgroundColor: colors.border }]} />
      <View style={styles.statsRow}>
        <StatPill icon="soccer" label="Goals" value={player.goals} color={colors.statGreen} />
        <StatPill icon="handshake" label="Assists" value={player.assists} color={colors.statBlue} />
        <StatPill icon="alert-circle-outline" label="Cards" value={player.cards} color={colors.statOrange} />
      </View>
    </Pressable>
  );
}

function StatPill({ icon, label, value, color }: { icon: string; label: string; value: string | number; color: string }) {
  const colors = useColors();

  return (
    <View style={styles.pill}>
      <MaterialCommunityIcons name={icon as never} size={14} color={color} />
      <Text style={[styles.pillValue, { color: colors.foreground }]}>{value}</Text>
      <Text style={[styles.pillLabel, { color: colors.mutedForeground }]}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 14,
    padding: 14,
    borderWidth: 1,
    marginBottom: 10,
  },
  top: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 12,
  },
  left: {
    flexDirection: "row",
    alignItems: "center",
    gap: 10,
    flex: 1,
  },
  info: {
    flex: 1,
    gap: 3,
  },
  name: {
    fontSize: 14,
    fontFamily: "Inter_600SemiBold",
  },
  teamName: {
    fontSize: 11,
    fontFamily: "Inter_500Medium",
  },
  meta: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
  },
  impactCircle: {
    width: 58,
    height: 58,
    borderRadius: 29,
    borderWidth: 2,
    alignItems: "center",
    justifyContent: "center",
  },
  impactValue: {
    fontSize: 15,
    fontFamily: "Inter_700Bold",
  },
  impactLabel: {
    fontSize: 8,
    fontFamily: "Inter_500Medium",
  },
  divider: {
    height: 1,
    marginVertical: 10,
  },
  statsRow: {
    flexDirection: "row",
    justifyContent: "space-around",
  },
  pill: {
    alignItems: "center",
    gap: 2,
  },
  pillValue: {
    fontSize: 13,
    fontFamily: "Inter_700Bold",
  },
  pillLabel: {
    fontSize: 9,
    fontFamily: "Inter_400Regular",
  },
});