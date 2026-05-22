import React, { useMemo, useState } from "react";
import {
  FlatList,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from "react-native";
import { useRouter } from "expo-router";
import { Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { useSafeAreaInsets } from "react-native-safe-area-context";

import { PlayerCard } from "@/components/PlayerCard";
import { useColors } from "@/hooks/useColors";
import { usePlayerDirectoryQuery } from "@/hooks/useFootballData";
import type { League } from "@/lib/football-data";

type SortKey = "impact" | "goals" | "assists" | "cards";

const SORT_OPTIONS: { key: SortKey; label: string }[] = [
  { key: "impact", label: "Impact" },
  { key: "goals", label: "Goals" },
  { key: "assists", label: "Assists" },
  { key: "cards", label: "Cards" },
];

export default function PlayersScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { data, isLoading, error } = usePlayerDirectoryQuery();
  const [search, setSearch] = useState("");
  const [leagueFilter, setLeagueFilter] = useState<"All" | League>("All");
  const [sortKey, setSortKey] = useState<SortKey>("impact");

  const headerTop = Platform.OS === "web" ? 67 : insets.top;
  const teams = data?.teams ?? [];
  const players = data?.players ?? [];
  const teamMap = useMemo(() => new Map(teams.map((team) => [team.id, team])), [teams]);
  const leagues = useMemo(
    () => ["All", ...Array.from(new Set(teams.map((team) => team.league))).sort()] as Array<"All" | League>,
    [teams],
  );

  const filtered = useMemo(() => {
    return players
      .filter((player) => {
        const team = teamMap.get(player.teamId);
        if (!team) {
          return false;
        }

        const matchesLeague = leagueFilter === "All" || team.league === leagueFilter;
        const matchesSearch =
          search.length === 0 ||
          player.name.toLowerCase().includes(search.toLowerCase()) ||
          team.shortName.toLowerCase().includes(search.toLowerCase());

        return matchesLeague && matchesSearch;
      })
      .sort((playerA, playerB) => {
        if (sortKey === "impact") {
          return (playerB.impact ?? Number.NEGATIVE_INFINITY) - (playerA.impact ?? Number.NEGATIVE_INFINITY);
        }

        if (sortKey === "goals") {
          return playerB.goals - playerA.goals;
        }

        if (sortKey === "assists") {
          return playerB.assists - playerA.assists;
        }

        return playerB.cards - playerA.cards;
      });
  }, [leagueFilter, players, search, sortKey, teamMap]);

  if (isLoading) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="progress-clock" size={36} color={colors.primary} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Loading players</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={[styles.state, { backgroundColor: colors.background }]}> 
        <MaterialCommunityIcons name="server-network-off" size={36} color={colors.statRed} />
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Unable to load players</Text>
        <Text style={[styles.stateText, { color: colors.mutedForeground }]}> 
          {error instanceof Error ? error.message : "The API is not reachable."}
        </Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}> 
      <View style={[styles.header, { paddingTop: headerTop + 10, backgroundColor: colors.background, borderBottomColor: colors.border }]}> 
        <View style={styles.titleRow}>
          <MaterialCommunityIcons name="account-multiple" size={22} color={colors.primary} />
          <Text style={[styles.title, { color: colors.foreground }]}>Players</Text>
          <View style={[styles.badge, { backgroundColor: colors.card, borderColor: colors.border }]}> 
            <Text style={[styles.badgeText, { color: colors.primary }]}>{filtered.length}</Text>
          </View>
        </View>
        <View style={[styles.searchBox, { backgroundColor: colors.card, borderColor: colors.border }]}> 
          <Ionicons name="search" size={16} color={colors.mutedForeground} />
          <TextInput
            placeholder="Search players or clubs..."
            placeholderTextColor={colors.mutedForeground}
            value={search}
            onChangeText={setSearch}
            style={[styles.searchInput, { color: colors.foreground }]}
          />
          {search.length > 0 && (
            <Pressable onPress={() => setSearch("")}> 
              <Ionicons name="close-circle" size={16} color={colors.mutedForeground} />
            </Pressable>
          )}
        </View>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.leagueRow}>
          {leagues.map((league) => (
            <Pressable
              key={league}
              onPress={() => setLeagueFilter(league)}
              style={[
                styles.chip,
                {
                  backgroundColor: leagueFilter === league ? colors.primary : colors.card,
                  borderColor: leagueFilter === league ? colors.primary : colors.border,
                },
              ]}
            >
              <Text
                style={[
                  styles.chipText,
                  { color: leagueFilter === league ? colors.primaryForeground : colors.mutedForeground },
                ]}
              >
                {league}
              </Text>
            </Pressable>
          ))}
        </ScrollView>
        <View style={styles.sortRow}>
          <Text style={[styles.sortLabel, { color: colors.mutedForeground }]}>Sort:</Text>
          {SORT_OPTIONS.map((option) => (
            <Pressable
              key={option.key}
              onPress={() => setSortKey(option.key)}
              style={[
                styles.sortBtn,
                { backgroundColor: sortKey === option.key ? colors.accent + "22" : "transparent" },
              ]}
            >
              <Text style={[styles.sortText, { color: sortKey === option.key ? colors.accent : colors.mutedForeground }]}>
                {option.label}
              </Text>
            </Pressable>
          ))}
        </View>
      </View>

      <FlatList
        data={filtered}
        keyExtractor={(player) => String(player.id)}
        contentContainerStyle={[styles.list, { paddingBottom: insets.bottom + 90 }]}
        showsVerticalScrollIndicator={false}
        renderItem={({ item }) => {
          const team = teamMap.get(item.teamId);
          if (!team) {
            return null;
          }

          return <PlayerCard player={item} team={team} onPress={() => router.push(`/player/${item.id}`)} />;
        }}
        ListEmptyComponent={
          <View style={styles.empty}>
            <MaterialCommunityIcons name="account-off" size={40} color={colors.mutedForeground} />
            <Text style={[styles.emptyText, { color: colors.mutedForeground }]}>No players found</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: { paddingHorizontal: 16, paddingBottom: 10, borderBottomWidth: 1, gap: 10 },
  titleRow: { flexDirection: "row", alignItems: "center", gap: 8 },
  title: { fontSize: 22, fontFamily: "Inter_700Bold", flex: 1 },
  badge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, borderWidth: 1 },
  badgeText: { fontSize: 12, fontFamily: "Inter_700Bold" },
  searchBox: { flexDirection: "row", alignItems: "center", borderRadius: 10, borderWidth: 1, paddingHorizontal: 10, paddingVertical: 8, gap: 8 },
  searchInput: { flex: 1, fontSize: 14, fontFamily: "Inter_400Regular" },
  leagueRow: { gap: 8, paddingVertical: 2 },
  chip: { paddingHorizontal: 14, paddingVertical: 6, borderRadius: 20, borderWidth: 1 },
  chipText: { fontSize: 12, fontFamily: "Inter_600SemiBold" },
  sortRow: { flexDirection: "row", alignItems: "center", gap: 4 },
  sortLabel: { fontSize: 12, fontFamily: "Inter_500Medium", marginRight: 4 },
  sortBtn: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 8 },
  sortText: { fontSize: 12, fontFamily: "Inter_600SemiBold" },
  list: { padding: 16 },
  empty: { alignItems: "center", marginTop: 60, gap: 12 },
  emptyText: { fontSize: 15, fontFamily: "Inter_500Medium" },
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