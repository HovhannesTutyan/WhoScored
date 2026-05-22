import React from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import * as Haptics from "expo-haptics";

import { useColors } from "@/hooks/useColors";
import type { TeamBadgeData, TeamSummary } from "@/lib/football-data";

interface TeamCardProps {
  team: TeamSummary;
  onPress: () => void;
  compact?: boolean;
  selected?: boolean;
}

function getLeagueColor(league: string, colors: ReturnType<typeof useColors>) {
  switch (league) {
    case "Premier League":
      return colors.premierLeague;
    case "La Liga":
      return colors.laLiga;
    case "Bundesliga":
      return colors.statOrange;
    case "Serie A":
      return colors.statBlue;
    case "Ligue 1":
      return colors.accent;
    default:
      return colors.primary;
  }
}

function TeamBadge({ team, size = 48 }: { team: TeamBadgeData; size?: number }) {
  return (
    <View
      style={[
        styles.badge,
        {
          width: size,
          height: size,
          borderRadius: size * 0.2,
          backgroundColor: team.primaryColor + "22",
          borderColor: team.primaryColor + "44",
        },
      ]}
    >
      <Text style={[styles.badgeText, { color: team.primaryColor, fontSize: size * 0.35 }]}>
        {team.abbr}
      </Text>
    </View>
  );
}

export function TeamCard({ team, onPress, compact = false, selected = false }: TeamCardProps) {
  const colors = useColors();
  const gd = team.stats.goalsFor - team.stats.goalsAgainst;
  const leagueColor = getLeagueColor(team.league, colors);

  return (
    <Pressable
      onPress={() => {
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        onPress();
      }}
      style={({ pressed }) => [
        styles.card,
        {
          backgroundColor: selected ? team.primaryColor + "22" : colors.card,
          borderColor: selected ? team.primaryColor : colors.border,
          opacity: pressed ? 0.85 : 1,
        },
      ]}
    >
      <View style={styles.left}>
        <TeamBadge team={team} size={compact ? 40 : 50} />
        <View style={styles.info}>
          <Text style={[styles.name, { color: colors.foreground }]} numberOfLines={1}>
            {team.shortName}
          </Text>
          <View style={styles.leagueRow}>
            <View style={[styles.leagueDot, { backgroundColor: leagueColor }]} />
            <Text style={[styles.league, { color: colors.mutedForeground }]}>{team.league}</Text>
          </View>
          {!compact && (
            <Text style={[styles.meta, { color: colors.mutedForeground }]}>
              {team.stats.goalsFor} GF · {team.stats.goalsAgainst} GA · {team.stats.xG.toFixed(1)} xG
            </Text>
          )}
        </View>
      </View>
      <View style={styles.right}>
        <View style={styles.statGroup}>
          <Text style={[styles.statValue, { color: team.primaryColor }]}>{team.stats.points}</Text>
          <Text style={[styles.statLabel, { color: colors.mutedForeground }]}>PTS</Text>
        </View>
        {!compact && (
          <>
            <View style={styles.statGroup}>
              <Text style={[styles.statValue, { color: colors.foreground }]}>
                {team.stats.won}-{team.stats.drawn}-{team.stats.lost}
              </Text>
              <Text style={[styles.statLabel, { color: colors.mutedForeground }]}>W-D-L</Text>
            </View>
            <View style={styles.statGroup}>
              <Text style={[styles.statValue, { color: gd >= 0 ? colors.statGreen : colors.statRed }]}>
                {gd > 0 ? "+" : ""}
                {gd}
              </Text>
              <Text style={[styles.statLabel, { color: colors.mutedForeground }]}>GD</Text>
            </View>
          </>
        )}
      </View>
    </Pressable>
  );
}

export { TeamBadge };

const styles = StyleSheet.create({
  card: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    borderRadius: 14,
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderWidth: 1,
    marginBottom: 10,
  },
  left: {
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    flex: 1,
  },
  badge: {
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
  },
  badgeText: {
    fontFamily: "Inter_700Bold",
    letterSpacing: 0.5,
  },
  info: {
    flex: 1,
    gap: 3,
  },
  name: {
    fontSize: 15,
    fontFamily: "Inter_600SemiBold",
  },
  leagueRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 5,
  },
  leagueDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
  },
  league: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
  },
  meta: {
    fontSize: 11,
    fontFamily: "Inter_400Regular",
  },
  right: {
    flexDirection: "row",
    gap: 12,
    alignItems: "center",
  },
  statGroup: {
    alignItems: "center",
    minWidth: 40,
  },
  statValue: {
    fontSize: 14,
    fontFamily: "Inter_700Bold",
  },
  statLabel: {
    fontSize: 9,
    fontFamily: "Inter_500Medium",
    marginTop: 1,
  },
});