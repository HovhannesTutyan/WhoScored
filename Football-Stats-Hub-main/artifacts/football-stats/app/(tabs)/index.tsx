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

import { TeamCard } from "@/components/TeamCard";
import { useColors } from "@/hooks/useColors";
import { useTeamsQuery } from "@/hooks/useFootballData";
import type { League } from "@/lib/football-data";

type FilterLeague = "All" | League;

export default function TeamsScreen() {
  const colors = useColors();
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const { data: teams = [], isLoading, error } = useTeamsQuery();
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<FilterLeague>("All");

  const headerTop = Platform.OS === "web" ? 67 : insets.top;
  const leagues = useMemo(
    () => ["All", ...Array.from(new Set(teams.map((team) => team.league))).sort()] as FilterLeague[],
    [teams],
  );

  const filtered = useMemo(() => {
    return teams
      .filter((team) => {
        const matchesLeague = filter === "All" || team.league === filter;
        const matchesSearch =
          search.length === 0 ||
          team.name.toLowerCase().includes(search.toLowerCase()) ||
          team.abbr.toLowerCase().includes(search.toLowerCase());

        return matchesLeague && matchesSearch;
      })
      .sort((teamA, teamB) => teamB.stats.points - teamA.stats.points);
  }, [filter, search, teams]);

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
        <Text style={[styles.stateTitle, { color: colors.foreground }]}>Unable to load clubs</Text>
        <Text style={[styles.stateText, { color: colors.mutedForeground }]}> 
          {error instanceof Error ? error.message : "The API is not reachable."}
        </Text>
      </View>
    );
  }

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}> 
      <View
        style={[
          styles.header,
          {
            paddingTop: headerTop + 10,
            backgroundColor: colors.background,
            borderBottomColor: colors.border,
          },
        ]}
      >
        <View style={styles.titleRow}>
          <MaterialCommunityIcons name="soccer" size={22} color={colors.primary} />
          <Text style={[styles.title, { color: colors.foreground }]}>Clubs</Text>
          <View style={styles.countBadge}>
            <Text style={[styles.countText, { color: colors.primary }]}>{filtered.length}</Text>
          </View>
        </View>
        <View style={[styles.searchBox, { backgroundColor: colors.card, borderColor: colors.border }]}> 
          <Ionicons name="search" size={16} color={colors.mutedForeground} />
          <TextInput
            placeholder="Search clubs..."
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
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filterRow}>
          {leagues.map((league) => (
            <Pressable
              key={league}
              onPress={() => setFilter(league)}
              style={[
                styles.filterBtn,
                {
                  backgroundColor: filter === league ? colors.primary : colors.card,
                  borderColor: filter === league ? colors.primary : colors.border,
                },
              ]}
            >
              <Text
                style={[
                  styles.filterText,
                  { color: filter === league ? colors.primaryForeground : colors.mutedForeground },
                ]}
              >
                {league}
              </Text>
            </Pressable>
          ))}
        </ScrollView>
      </View>

      <FlatList
        data={filtered}
        keyExtractor={(item) => String(item.id)}
        contentContainerStyle={[styles.list, { paddingBottom: insets.bottom + 90, paddingTop: 8 }]}
        showsVerticalScrollIndicator={false}
        renderItem={({ item, index }) => (
          <View style={styles.itemWrapper}>
            <View style={styles.rankBadge}>
              <Text style={[styles.rankText, { color: index === 0 ? colors.gold : colors.mutedForeground }]}>{index + 1}</Text>
            </View>
            <View style={{ flex: 1 }}>
              <TeamCard team={item} onPress={() => router.push(`/team/${item.id}`)} />
            </View>
          </View>
        )}
        ListEmptyComponent={
          <View style={styles.empty}>
            <MaterialCommunityIcons name="shield-off" size={40} color={colors.mutedForeground} />
            <Text style={[styles.emptyText, { color: colors.mutedForeground }]}>No clubs found</Text>
          </View>
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  header: {
    paddingHorizontal: 16,
    paddingBottom: 12,
    borderBottomWidth: 1,
    gap: 10,
  },
  titleRow: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  title: {
    fontSize: 22,
    fontFamily: "Inter_700Bold",
    flex: 1,
  },
  countBadge: { paddingHorizontal: 8, paddingVertical: 2 },
  countText: { fontSize: 13, fontFamily: "Inter_700Bold" },
  searchBox: {
    flexDirection: "row",
    alignItems: "center",
    borderRadius: 10,
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 8,
    gap: 8,
  },
  searchInput: { flex: 1, fontSize: 14, fontFamily: "Inter_400Regular" },
  filterRow: { gap: 8 },
  filterBtn: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
    borderWidth: 1,
  },
  filterText: { fontSize: 12, fontFamily: "Inter_500Medium" },
  list: { paddingHorizontal: 16 },
  itemWrapper: { flexDirection: "row", alignItems: "center", gap: 6 },
  rankBadge: { width: 20, alignItems: "center" },
  rankText: { fontSize: 12, fontFamily: "Inter_600SemiBold" },
  empty: { alignItems: "center", marginTop: 60, gap: 12 },
  emptyText: { fontSize: 15, fontFamily: "Inter_500Medium" },
  state: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
    gap: 10,
  },
  stateTitle: {
    fontSize: 18,
    fontFamily: "Inter_700Bold",
  },
  stateText: {
    fontSize: 13,
    fontFamily: "Inter_400Regular",
    textAlign: "center",
  },
});