import { Platform } from "react-native";

type ApiError = {
  code?: string;
  message: string;
};

type ApiMeta = {
  count?: number;
  page?: number;
  num_pages?: number;
};

type ApiEnvelope<T> = {
  success: boolean;
  data: T;
  meta: ApiMeta;
  errors: ApiError[];
};

type ApiTeamListItem = {
  id: number;
  name: string;
  league_name: string;
  matches_overall: number;
  wins_overall: number;
  draws_overall: number;
  losses_overall: number;
  goals_for_overall: number;
  goals_against_overall: number;
  points_overall: number;
  xg_for: number;
  xg_against: number;
};

type ApiPlayerListItem = {
  id: number;
  team_id: number;
  team_name: string;
  name: string;
  goals: number | null;
  assists: number | null;
  cards: number | null;
};

type ApiTeamPlayersPayload = {
  team: {
    id: number;
    name: string;
  };
  players: ApiPlayerListItem[];
};

type ApiTeamGoalkeeper = {
  team_id: number;
  team_name: string;
  league_name: string;
  season: string;
  ga: number | null;
  save_pct: number | null;
  cs: number | null;
  psxg_net: number | null;
  saves: number | null;
};

type ApiTeamImpactPlayer = {
  id: number;
  name: string;
  team_id: number;
  attack_impact: number;
  defensive_impact: number;
  discipline_impact: number;
  goalkeeper_impact: number;
  total_player_impact: number;
};

type ApiTeamPlayerImpactPayload = {
  average_total_player_impact: number;
  average_attack_impact: number;
  average_defensive_impact: number;
  average_discipline_impact: number;
  average_goalkeeper_impact: number;
  player_count: number;
  warning?: string;
  players: ApiTeamImpactPlayer[];
};

type ApiTeamDerivedStats = {
  win_rate: number;
  draw_rate: number;
  loss_rate: number;
  goals_for_per_game: number;
  goals_against_per_game: number;
  points_per_game: number;
  xg_for_per_game: number;
  xg_against_per_game: number;
  goal_difference: number;
  goal_difference_per_game: number;
  xg_difference: number;
  xg_difference_per_game: number;
  finishing_efficiency: number;
  attacking_overperformance: number;
  defensive_overperformance: number;
};

type ApiAttackAndDefense = {
  attack_strength: number;
  defense_weakness: number;
  xg_attack_strength: number;
  xg_defense_weakness: number;
};

type ApiTeamStrength = {
  points_per_game_score: number;
  goal_difference_score: number;
  xg_difference_score: number;
  attacking_score: number;
  defensive_score: number;
  player_impact_score: number;
  overall_team_strength: number;
};

type ApiTeamStatsPayload = {
  team: {
    id: number;
    name: string;
    league_name: string;
  };
  derived_stats: ApiTeamDerivedStats;
  attack_and_defense: ApiAttackAndDefense;
  team_strength: ApiTeamStrength;
  player_impact: ApiTeamPlayerImpactPayload;
  goalkeeper: ApiTeamGoalkeeper | null;
};

type ApiStrengthsWeaknessesPayload = {
  team: {
    id: number;
    name: string;
  };
  strengths: string[];
  weaknesses: string[];
  risk_notes: string[];
};

type ApiPlayerStatsPayload = {
  player: {
    id: number;
    name: string;
    team: {
      id: number;
      name: string;
    };
  };
  raw_stats: {
    goals: number | null;
    assists: number | null;
    cards: number | null;
    shots_per_game: number | null;
    aerial_won_per_game: number | null;
    tackles: number | null;
    fouls: number | null;
    offsides: number | null;
    dribbles: number | null;
    goals_conceded: number | null;
    saves: number | null;
  };
  impact: {
    attack_impact: number;
    defensive_impact: number;
    discipline_impact: number;
    goalkeeper_impact: number;
    total_player_impact: number;
  };
};

type ApiComparisonPayload = {
  teams: {
    team_a: {
      id: number;
      name: string;
    };
    team_b: {
      id: number;
      name: string;
    };
  };
  comparison: Record<string, string>;
  metrics: {
    team_a: {
      team_strength: number;
      attack_strength: number;
      defense_weakness: number;
      xg_difference_per_game: number;
      player_impact: number;
    };
    team_b: {
      team_strength: number;
      attack_strength: number;
      defense_weakness: number;
      xg_difference_per_game: number;
      player_impact: number;
    };
  };
  profile_similarity: number | null;
};

type ApiHeadToHeadPayload = {
  teams: {
    team_a: {
      id: number;
      name: string;
    };
    team_b: {
      id: number;
      name: string;
    };
  };
  history_available: boolean;
  message: string;
  matches: Array<Record<string, unknown>>;
};

type ApiPredictionPayload = {
  teams: {
    team_a: {
      id: number;
      name: string;
    };
    team_b: {
      id: number;
      name: string;
    };
  };
  overall_prediction: {
    team_a_win: number;
    draw: number;
    team_b_win: number;
    predicted_winner: string;
    confidence_score: number;
    confidence_level: string;
  };
  expected_goals: {
    team_a: number;
    team_b: number;
  };
  most_likely_scores: Array<{
    score: string;
    probability: number;
  }>;
  over_under: Record<string, number | null>;
  both_teams_to_score: {
    yes: number;
    no: number;
  };
  team_comparison: Record<string, string>;
  strengths: {
    team_a: string[];
    team_b: string[];
  };
  weaknesses: {
    team_a: string[];
    team_b: string[];
  };
  risk_notes: string[];
  model_breakdown: Record<string, unknown>;
};

type TeamBranding = {
  shortName: string;
  abbr: string;
  primaryColor: string;
  secondaryColor: string;
};

export type TeamBadgeData = Pick<TeamSummary, "abbr" | "primaryColor">;

export type League = string;

export type TeamSummary = {
  id: number;
  name: string;
  shortName: string;
  league: League;
  abbr: string;
  primaryColor: string;
  secondaryColor: string;
  stats: {
    played: number;
    won: number;
    drawn: number;
    lost: number;
    goalsFor: number;
    goalsAgainst: number;
    points: number;
    xG: number;
    xGA: number;
  };
};

export type PlayerSummary = {
  id: number;
  teamId: number;
  teamName: string;
  name: string;
  goals: number;
  assists: number;
  cards: number;
  impact: number | null;
};

export type TeamImpactPlayer = {
  id: number;
  name: string;
  teamId: number;
  attackImpact: number;
  defensiveImpact: number;
  disciplineImpact: number;
  goalkeeperImpact: number;
  totalPlayerImpact: number;
};

export type TeamDerivedStats = {
  winRate: number;
  drawRate: number;
  lossRate: number;
  goalsForPerGame: number;
  goalsAgainstPerGame: number;
  pointsPerGame: number;
  xgForPerGame: number;
  xgAgainstPerGame: number;
  goalDifference: number;
  goalDifferencePerGame: number;
  xgDifference: number;
  xgDifferencePerGame: number;
  finishingEfficiency: number;
  attackingOverperformance: number;
  defensiveOverperformance: number;
};

export type TeamAttackAndDefense = {
  attackStrength: number;
  defenseWeakness: number;
  xgAttackStrength: number;
  xgDefenseWeakness: number;
};

export type TeamStrengthBreakdown = {
  pointsPerGameScore: number;
  goalDifferenceScore: number;
  xgDifferenceScore: number;
  attackingScore: number;
  defensiveScore: number;
  playerImpactScore: number;
  overallTeamStrength: number;
};

export type TeamPlayerImpactBreakdown = {
  averageTotalPlayerImpact: number;
  averageAttackImpact: number;
  averageDefensiveImpact: number;
  averageDisciplineImpact: number;
  averageGoalkeeperImpact: number;
  playerCount: number;
  warning?: string;
  players: TeamImpactPlayer[];
};

export type TeamGoalkeeperStats = {
  teamId: number;
  teamName: string;
  leagueName: string;
  season: string;
  goalsAgainst: number | null;
  savePct: number | null;
  cleanSheets: number | null;
  postShotXgNet: number | null;
  saves: number | null;
};

export type TeamDetailData = {
  team: TeamSummary;
  derivedStats: TeamDerivedStats;
  attackAndDefense: TeamAttackAndDefense;
  teamStrength: TeamStrengthBreakdown;
  playerImpact: TeamPlayerImpactBreakdown;
  goalkeeper: TeamGoalkeeperStats | null;
  strengths: string[];
  weaknesses: string[];
  riskNotes: string[];
  players: PlayerSummary[];
};

export type PlayerRawStats = {
  goals: number;
  assists: number;
  cards: number;
  shotsPerGame: number | null;
  aerialWonPerGame: number | null;
  tackles: number | null;
  fouls: number | null;
  offsides: number | null;
  dribbles: number | null;
  goalsConceded: number | null;
  saves: number | null;
};

export type PlayerImpactBreakdown = {
  attackImpact: number;
  defensiveImpact: number;
  disciplineImpact: number;
  goalkeeperImpact: number;
  totalPlayerImpact: number;
};

export type PlayerDetailData = {
  player: {
    id: number;
    name: string;
  };
  team: TeamBadgeData & {
    id: number;
    name: string;
    shortName: string;
  };
  rawStats: PlayerRawStats;
  impact: PlayerImpactBreakdown;
};

export type ComparisonMetric = {
  teamStrength: number;
  attackStrength: number;
  defenseWeakness: number;
  xgDifferencePerGame: number;
  playerImpact: number;
};

export type ComparisonData = {
  teams: {
    teamA: {
      id: number;
      name: string;
    };
    teamB: {
      id: number;
      name: string;
    };
  };
  comparison: Record<string, string>;
  metrics: {
    teamA: ComparisonMetric;
    teamB: ComparisonMetric;
  };
  profileSimilarity: number | null;
};

export type HeadToHeadData = {
  historyAvailable: boolean;
  message: string;
  matches: Array<Record<string, unknown>>;
};

export type PredictionData = {
  teams: {
    teamA: {
      id: number;
      name: string;
    };
    teamB: {
      id: number;
      name: string;
    };
  };
  overallPrediction: {
    teamAWin: number;
    draw: number;
    teamBWin: number;
    predictedWinner: string;
    confidenceScore: number;
    confidenceLevel: string;
  };
  expectedGoals: {
    teamA: number;
    teamB: number;
  };
  mostLikelyScores: Array<{
    score: string;
    probability: number;
  }>;
  overUnder: Record<string, number | null>;
  bothTeamsToScore: {
    yes: number;
    no: number;
  };
  teamComparison: Record<string, string>;
  strengths: {
    teamA: string[];
    teamB: string[];
  };
  weaknesses: {
    teamA: string[];
    teamB: string[];
  };
  riskNotes: string[];
  modelBreakdown: Record<string, unknown>;
};

export type PairInsightsData = {
  comparison: ComparisonData;
  headToHead: HeadToHeadData;
  prediction: PredictionData;
};

const TEAM_BRANDING: Record<string, TeamBranding> = {
  Arsenal: {
    shortName: "Arsenal",
    abbr: "ARS",
    primaryColor: "#EF0107",
    secondaryColor: "#FFFFFF",
  },
  "Manchester City": {
    shortName: "Man City",
    abbr: "MCI",
    primaryColor: "#6CABDD",
    secondaryColor: "#1C2C5B",
  },
  "Manchester Utd": {
    shortName: "Man Utd",
    abbr: "MUN",
    primaryColor: "#DA291C",
    secondaryColor: "#FBE122",
  },
  Liverpool: {
    shortName: "Liverpool",
    abbr: "LIV",
    primaryColor: "#C8102E",
    secondaryColor: "#F6EB61",
  },
  Everton: {
    shortName: "Everton",
    abbr: "EVE",
    primaryColor: "#003399",
    secondaryColor: "#FFFFFF",
  },
  Barcelona: {
    shortName: "Barcelona",
    abbr: "BAR",
    primaryColor: "#A50044",
    secondaryColor: "#004D98",
  },
  "Real Madrid": {
    shortName: "Real Madrid",
    abbr: "RMA",
    primaryColor: "#FEBE10",
    secondaryColor: "#FFFFFF",
  },
  Villarreal: {
    shortName: "Villarreal",
    abbr: "VIL",
    primaryColor: "#FFD700",
    secondaryColor: "#009036",
  },
  "Atl. Madrid": {
    shortName: "Atletico",
    abbr: "ATM",
    primaryColor: "#CB3524",
    secondaryColor: "#003087",
  },
  Betis: {
    shortName: "Betis",
    abbr: "BET",
    primaryColor: "#00954B",
    secondaryColor: "#FFFFFF",
  },
  Inter: {
    shortName: "Inter",
    abbr: "INT",
    primaryColor: "#00529F",
    secondaryColor: "#000000",
  },
  "AS Roma": {
    shortName: "Roma",
    abbr: "ROM",
    primaryColor: "#8E1F2F",
    secondaryColor: "#F7C948",
  },
  Como: {
    shortName: "Como",
    abbr: "COM",
    primaryColor: "#1D65A6",
    secondaryColor: "#FFFFFF",
  },
  "Bayern Munich": {
    shortName: "Bayern",
    abbr: "FCB",
    primaryColor: "#DC052D",
    secondaryColor: "#0066B2",
  },
  Dortmund: {
    shortName: "Dortmund",
    abbr: "BVB",
    primaryColor: "#FDE100",
    secondaryColor: "#000000",
  },
  "RB Leipzig": {
    shortName: "Leipzig",
    abbr: "RBL",
    primaryColor: "#D50032",
    secondaryColor: "#0D1B2A",
  },
  Stuttgart: {
    shortName: "Stuttgart",
    abbr: "VFB",
    primaryColor: "#E30613",
    secondaryColor: "#FFFFFF",
  },
  "Bayer Leverkusen": {
    shortName: "Leverkusen",
    abbr: "B04",
    primaryColor: "#D00027",
    secondaryColor: "#111111",
  },
  PSG: {
    shortName: "PSG",
    abbr: "PSG",
    primaryColor: "#004170",
    secondaryColor: "#DA291C",
  },
};

function normalizeApiBaseUrl(value: string): string {
  const stripped = value.replace(/\/+$/, "");
  return stripped.endsWith("/api") ? stripped.slice(0, -4) : stripped;
}

function getConfiguredApiBaseUrl(): string | undefined {
  const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env;
  return env?.EXPO_PUBLIC_API_BASE_URL;
}

export function getApiBaseUrl(): string {
  const configured = getConfiguredApiBaseUrl()?.trim();
  if (configured) {
    return normalizeApiBaseUrl(configured);
  }

  if (Platform.OS === "android") {
    return "http://10.0.2.2:8000";
  }

  return "http://127.0.0.1:8000";
}

export function formatLeagueName(leagueName: string): string {
  if (leagueName === "LaLiga") {
    return "La Liga";
  }

  return leagueName;
}

function getTeamBranding(teamName: string): TeamBranding {
  const branding = TEAM_BRANDING[teamName];
  if (branding) {
    return branding;
  }

  const words = teamName
    .replace(/[^A-Za-z0-9 ]+/g, " ")
    .split(/\s+/)
    .filter(Boolean);

  return {
    shortName: teamName,
    abbr: words.slice(0, 3).map((word) => word[0]?.toUpperCase() ?? "").join("") || "CLB",
    primaryColor: "#2979FF",
    secondaryColor: "#FFFFFF",
  };
}

function toNumber(value: number | null | undefined): number {
  return typeof value === "number" && Number.isFinite(value) ? value : 0;
}

function toTeamSummary(team: ApiTeamListItem): TeamSummary {
  const branding = getTeamBranding(team.name);

  return {
    id: team.id,
    name: team.name,
    shortName: branding.shortName,
    league: formatLeagueName(team.league_name),
    abbr: branding.abbr,
    primaryColor: branding.primaryColor,
    secondaryColor: branding.secondaryColor,
    stats: {
      played: team.matches_overall,
      won: team.wins_overall,
      drawn: team.draws_overall,
      lost: team.losses_overall,
      goalsFor: team.goals_for_overall,
      goalsAgainst: team.goals_against_overall,
      points: team.points_overall,
      xG: team.xg_for,
      xGA: team.xg_against,
    },
  };
}

function toPlayerImpactBreakdown(payload: ApiTeamPlayerImpactPayload): TeamPlayerImpactBreakdown {
  return {
    averageTotalPlayerImpact: payload.average_total_player_impact,
    averageAttackImpact: payload.average_attack_impact,
    averageDefensiveImpact: payload.average_defensive_impact,
    averageDisciplineImpact: payload.average_discipline_impact,
    averageGoalkeeperImpact: payload.average_goalkeeper_impact,
    playerCount: payload.player_count,
    warning: payload.warning,
    players: payload.players.map((player) => ({
      id: player.id,
      name: player.name,
      teamId: player.team_id,
      attackImpact: player.attack_impact,
      defensiveImpact: player.defensive_impact,
      disciplineImpact: player.discipline_impact,
      goalkeeperImpact: player.goalkeeper_impact,
      totalPlayerImpact: player.total_player_impact,
    })),
  };
}

function toPlayerSummary(
  player: ApiPlayerListItem,
  impactByPlayerId: ReadonlyMap<number, number>,
): PlayerSummary {
  return {
    id: player.id,
    teamId: player.team_id,
    teamName: player.team_name,
    name: player.name,
    goals: toNumber(player.goals),
    assists: toNumber(player.assists),
    cards: toNumber(player.cards),
    impact: impactByPlayerId.get(player.id) ?? null,
  };
}

function toDerivedStats(stats: ApiTeamDerivedStats): TeamDerivedStats {
  return {
    winRate: stats.win_rate,
    drawRate: stats.draw_rate,
    lossRate: stats.loss_rate,
    goalsForPerGame: stats.goals_for_per_game,
    goalsAgainstPerGame: stats.goals_against_per_game,
    pointsPerGame: stats.points_per_game,
    xgForPerGame: stats.xg_for_per_game,
    xgAgainstPerGame: stats.xg_against_per_game,
    goalDifference: stats.goal_difference,
    goalDifferencePerGame: stats.goal_difference_per_game,
    xgDifference: stats.xg_difference,
    xgDifferencePerGame: stats.xg_difference_per_game,
    finishingEfficiency: stats.finishing_efficiency,
    attackingOverperformance: stats.attacking_overperformance,
    defensiveOverperformance: stats.defensive_overperformance,
  };
}

function toAttackAndDefense(stats: ApiAttackAndDefense): TeamAttackAndDefense {
  return {
    attackStrength: stats.attack_strength,
    defenseWeakness: stats.defense_weakness,
    xgAttackStrength: stats.xg_attack_strength,
    xgDefenseWeakness: stats.xg_defense_weakness,
  };
}

function toTeamStrength(stats: ApiTeamStrength): TeamStrengthBreakdown {
  return {
    pointsPerGameScore: stats.points_per_game_score,
    goalDifferenceScore: stats.goal_difference_score,
    xgDifferenceScore: stats.xg_difference_score,
    attackingScore: stats.attacking_score,
    defensiveScore: stats.defensive_score,
    playerImpactScore: stats.player_impact_score,
    overallTeamStrength: stats.overall_team_strength,
  };
}

function toGoalkeeperStats(goalkeeper: ApiTeamGoalkeeper | null): TeamGoalkeeperStats | null {
  if (!goalkeeper) {
    return null;
  }

  return {
    teamId: goalkeeper.team_id,
    teamName: goalkeeper.team_name,
    leagueName: formatLeagueName(goalkeeper.league_name),
    season: goalkeeper.season,
    goalsAgainst: goalkeeper.ga,
    savePct: goalkeeper.save_pct,
    cleanSheets: goalkeeper.cs,
    postShotXgNet: goalkeeper.psxg_net,
    saves: goalkeeper.saves,
  };
}

function toPlayerDetailData(payload: ApiPlayerStatsPayload): PlayerDetailData {
  const branding = getTeamBranding(payload.player.team.name);

  return {
    player: {
      id: payload.player.id,
      name: payload.player.name,
    },
    team: {
      id: payload.player.team.id,
      name: payload.player.team.name,
      shortName: branding.shortName,
      abbr: branding.abbr,
      primaryColor: branding.primaryColor,
    },
    rawStats: {
      goals: toNumber(payload.raw_stats.goals),
      assists: toNumber(payload.raw_stats.assists),
      cards: toNumber(payload.raw_stats.cards),
      shotsPerGame: payload.raw_stats.shots_per_game,
      aerialWonPerGame: payload.raw_stats.aerial_won_per_game,
      tackles: payload.raw_stats.tackles,
      fouls: payload.raw_stats.fouls,
      offsides: payload.raw_stats.offsides,
      dribbles: payload.raw_stats.dribbles,
      goalsConceded: payload.raw_stats.goals_conceded,
      saves: payload.raw_stats.saves,
    },
    impact: {
      attackImpact: payload.impact.attack_impact,
      defensiveImpact: payload.impact.defensive_impact,
      disciplineImpact: payload.impact.discipline_impact,
      goalkeeperImpact: payload.impact.goalkeeper_impact,
      totalPlayerImpact: payload.impact.total_player_impact,
    },
  };
}

function toComparisonData(payload: ApiComparisonPayload): ComparisonData {
  return {
    teams: {
      teamA: payload.teams.team_a,
      teamB: payload.teams.team_b,
    },
    comparison: payload.comparison,
    metrics: {
      teamA: {
        teamStrength: payload.metrics.team_a.team_strength,
        attackStrength: payload.metrics.team_a.attack_strength,
        defenseWeakness: payload.metrics.team_a.defense_weakness,
        xgDifferencePerGame: payload.metrics.team_a.xg_difference_per_game,
        playerImpact: payload.metrics.team_a.player_impact,
      },
      teamB: {
        teamStrength: payload.metrics.team_b.team_strength,
        attackStrength: payload.metrics.team_b.attack_strength,
        defenseWeakness: payload.metrics.team_b.defense_weakness,
        xgDifferencePerGame: payload.metrics.team_b.xg_difference_per_game,
        playerImpact: payload.metrics.team_b.player_impact,
      },
    },
    profileSimilarity: payload.profile_similarity,
  };
}

function toHeadToHeadData(payload: ApiHeadToHeadPayload): HeadToHeadData {
  return {
    historyAvailable: payload.history_available,
    message: payload.message,
    matches: payload.matches,
  };
}

function toPredictionData(payload: ApiPredictionPayload): PredictionData {
  return {
    teams: {
      teamA: payload.teams.team_a,
      teamB: payload.teams.team_b,
    },
    overallPrediction: {
      teamAWin: payload.overall_prediction.team_a_win,
      draw: payload.overall_prediction.draw,
      teamBWin: payload.overall_prediction.team_b_win,
      predictedWinner: payload.overall_prediction.predicted_winner,
      confidenceScore: payload.overall_prediction.confidence_score,
      confidenceLevel: payload.overall_prediction.confidence_level,
    },
    expectedGoals: {
      teamA: payload.expected_goals.team_a,
      teamB: payload.expected_goals.team_b,
    },
    mostLikelyScores: payload.most_likely_scores,
    overUnder: payload.over_under,
    bothTeamsToScore: payload.both_teams_to_score,
    teamComparison: payload.team_comparison,
    strengths: {
      teamA: payload.strengths.team_a,
      teamB: payload.strengths.team_b,
    },
    weaknesses: {
      teamA: payload.weaknesses.team_a,
      teamB: payload.weaknesses.team_b,
    },
    riskNotes: payload.risk_notes,
    modelBreakdown: payload.model_breakdown,
  };
}

function buildUrl(path: string, params?: Record<string, string | number | undefined>): string {
  const query = new URLSearchParams();

  for (const [key, value] of Object.entries(params ?? {})) {
    if (value !== undefined) {
      query.set(key, String(value));
    }
  }

  const baseUrl = `${getApiBaseUrl()}${path}`;
  const queryString = query.toString();
  return queryString.length > 0 ? `${baseUrl}?${queryString}` : baseUrl;
}

async function requestEnvelope<T>(
  path: string,
  params?: Record<string, string | number | undefined>,
): Promise<ApiEnvelope<T>> {
  const response = await fetch(buildUrl(path, params), {
    headers: {
      Accept: "application/json",
    },
  });

  let payload: ApiEnvelope<T> | null = null;

  try {
    payload = (await response.json()) as ApiEnvelope<T>;
  } catch {
    payload = null;
  }

  if (!response.ok || !payload?.success) {
    const message = payload?.errors?.map((error) => error.message).join(" ") || `Request failed with status ${response.status}.`;
    throw new Error(message);
  }

  return payload;
}

async function requestAllPages<T>(path: string): Promise<T[]> {
  const collected: T[] = [];
  let page = 1;

  while (true) {
    const payload = await requestEnvelope<T[]>(path, { page });
    collected.push(...payload.data);

    if (!payload.meta.num_pages || page >= payload.meta.num_pages) {
      return collected;
    }

    page += 1;
  }
}

async function getImpactByPlayerId(teams: TeamSummary[]): Promise<Map<number, number>> {
  const impactByPlayerId = new Map<number, number>();
  const responses = await Promise.allSettled(
    teams.map((team) => requestEnvelope<ApiTeamPlayerImpactPayload>(`/api/teams/${team.id}/player-impact/`)),
  );

  for (const response of responses) {
    if (response.status !== "fulfilled") {
      continue;
    }

    for (const player of response.value.data.players) {
      impactByPlayerId.set(player.id, player.total_player_impact);
    }
  }

  return impactByPlayerId;
}

export async function getTeams(): Promise<TeamSummary[]> {
  const teams = await requestAllPages<ApiTeamListItem>("/api/teams/");
  return teams.map(toTeamSummary);
}

export async function getTeamDetail(teamId: number): Promise<TeamDetailData> {
  const [teamResponse, statsResponse, playersResponse, strengthsResponse] = await Promise.all([
    requestEnvelope<ApiTeamListItem>(`/api/teams/${teamId}/`),
    requestEnvelope<ApiTeamStatsPayload>(`/api/teams/${teamId}/stats/`),
    requestEnvelope<ApiTeamPlayersPayload>(`/api/teams/${teamId}/players/`),
    requestEnvelope<ApiStrengthsWeaknessesPayload>(`/api/teams/${teamId}/strengths-weaknesses/`),
  ]);

  const team = toTeamSummary(teamResponse.data);
  const playerImpact = toPlayerImpactBreakdown(statsResponse.data.player_impact);
  const impactByPlayerId = new Map(playerImpact.players.map((player) => [player.id, player.totalPlayerImpact]));
  const players = playersResponse.data.players
    .map((player) => toPlayerSummary(player, impactByPlayerId))
    .sort((teamA, teamB) => {
      const impactDifference = (teamB.impact ?? Number.NEGATIVE_INFINITY) - (teamA.impact ?? Number.NEGATIVE_INFINITY);
      if (impactDifference !== 0) {
        return impactDifference;
      }

      const goalDifference = teamB.goals - teamA.goals;
      if (goalDifference !== 0) {
        return goalDifference;
      }

      return teamB.assists - teamA.assists;
    })
    .slice(0, 6);

  return {
    team,
    derivedStats: toDerivedStats(statsResponse.data.derived_stats),
    attackAndDefense: toAttackAndDefense(statsResponse.data.attack_and_defense),
    teamStrength: toTeamStrength(statsResponse.data.team_strength),
    playerImpact,
    goalkeeper: toGoalkeeperStats(statsResponse.data.goalkeeper),
    strengths: strengthsResponse.data.strengths,
    weaknesses: strengthsResponse.data.weaknesses,
    riskNotes: strengthsResponse.data.risk_notes,
    players,
  };
}

export async function getPlayerDirectory(): Promise<{
  teams: TeamSummary[];
  players: PlayerSummary[];
}> {
  const teams = await getTeams();
  const [players, impactByPlayerId] = await Promise.all([
    requestAllPages<ApiPlayerListItem>("/api/players/"),
    getImpactByPlayerId(teams),
  ]);

  return {
    teams,
    players: players.map((player) => toPlayerSummary(player, impactByPlayerId)),
  };
}

export async function getPlayerDetail(playerId: number): Promise<PlayerDetailData> {
  const payload = await requestEnvelope<ApiPlayerStatsPayload>(`/api/players/${playerId}/stats/`);
  return toPlayerDetailData(payload.data);
}

export async function getPairInsights(teamAId: number, teamBId: number): Promise<PairInsightsData> {
  const [comparisonResponse, headToHeadResponse, predictionResponse] = await Promise.all([
    requestEnvelope<ApiComparisonPayload>("/api/compare/", {
      team_a: teamAId,
      team_b: teamBId,
    }),
    requestEnvelope<ApiHeadToHeadPayload>("/api/head-to-head/", {
      team_a: teamAId,
      team_b: teamBId,
    }),
    requestEnvelope<ApiPredictionPayload>("/api/predict/", {
      team_a: teamAId,
      team_b: teamBId,
    }),
  ]);

  return {
    comparison: toComparisonData(comparisonResponse.data),
    headToHead: toHeadToHeadData(headToHeadResponse.data),
    prediction: toPredictionData(predictionResponse.data),
  };
}