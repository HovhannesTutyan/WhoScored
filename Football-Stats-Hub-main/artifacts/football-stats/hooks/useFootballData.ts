import { useQuery } from "@tanstack/react-query";

import {
  getPairInsights,
  getPlayerDetail,
  getPlayerDirectory,
  getTeamDetail,
  getTeams,
} from "@/lib/football-data";

const STALE_TIME_MS = 60_000;

export function useTeamsQuery() {
  return useQuery({
    queryKey: ["football", "teams"],
    queryFn: getTeams,
    staleTime: STALE_TIME_MS,
  });
}

export function useTeamDetailQuery(teamId: number | null) {
  return useQuery({
    queryKey: ["football", "team", teamId],
    queryFn: () => getTeamDetail(teamId as number),
    enabled: typeof teamId === "number" && Number.isFinite(teamId),
    staleTime: STALE_TIME_MS,
  });
}

export function usePlayerDirectoryQuery() {
  return useQuery({
    queryKey: ["football", "players", "directory"],
    queryFn: getPlayerDirectory,
    staleTime: STALE_TIME_MS,
  });
}

export function usePlayerDetailQuery(playerId: number | null) {
  return useQuery({
    queryKey: ["football", "player", playerId],
    queryFn: () => getPlayerDetail(playerId as number),
    enabled: typeof playerId === "number" && Number.isFinite(playerId),
    staleTime: STALE_TIME_MS,
  });
}

export function usePairInsightsQuery(teamAId: number | null, teamBId: number | null) {
  return useQuery({
    queryKey: ["football", "pair-insights", teamAId, teamBId],
    queryFn: () => getPairInsights(teamAId as number, teamBId as number),
    enabled:
      typeof teamAId === "number" &&
      Number.isFinite(teamAId) &&
      typeof teamBId === "number" &&
      Number.isFinite(teamBId),
    staleTime: STALE_TIME_MS,
  });
}