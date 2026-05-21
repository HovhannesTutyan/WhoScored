from __future__ import annotations

import sqlite3
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.players.models import Player
from apps.teams.models import GoalkeeperStat, Team


class Command(BaseCommand):
    help = "Import teams, players, and goalkeeper stats from the scraper SQLite database."

    def add_arguments(self, parser):
        parser.add_argument("--database-path", default=None, help="Path to the scraper SQLite database.")
        parser.add_argument("--clear", action="store_true", help="Clear existing imported data before importing.")

    def handle(self, *args, **options):
        database_path = Path(options["database_path"] or settings.EXTERNAL_SCRAPER_DB_PATH)
        if not database_path.exists():
            raise CommandError(f"Scraper database not found: {database_path}")

        with sqlite3.connect(database_path) as source_conn, transaction.atomic():
            if options["clear"]:
                GoalkeeperStat.objects.all().delete()
                Player.objects.all().delete()
                Team.objects.all().delete()

            teams_by_source_id = self._import_teams(source_conn)
            players_count = self._import_players(source_conn, teams_by_source_id)
            goalkeeper_count = self._import_goalkeepers(source_conn, teams_by_source_id)

        self.stdout.write(self.style.SUCCESS(
            f"Imported {len(teams_by_source_id)} teams, {players_count} players, and {goalkeeper_count} goalkeeper rows."
        ))

    def _import_teams(self, source_conn: sqlite3.Connection) -> dict[int, Team]:
        teams_by_source_id: dict[int, Team] = {}
        rows = source_conn.execute(
            """
            SELECT t.id, COALESCE(l.league_name, ''), t.team_name, t.matches_overall,
                   t.wins_overall, t.draws_overall, t.losses_overall,
                   t.goals_for_overall, t.goals_against_overall, t.points_overall,
                   t.xg_for, t.xg_against
            FROM teams t
            LEFT JOIN leagues l ON l.id = t.league_id
            ORDER BY t.id
            """
        ).fetchall()
        for row in rows:
            team, _ = Team.objects.update_or_create(
                source_team_id=row[0],
                defaults={
                    "league_name": row[1] or "",
                    "name": row[2],
                    "matches_overall": row[3] or 0,
                    "wins_overall": row[4] or 0,
                    "draws_overall": row[5] or 0,
                    "losses_overall": row[6] or 0,
                    "goals_for_overall": row[7] or 0,
                    "goals_against_overall": row[8] or 0,
                    "points_overall": row[9] or 0,
                    "xg_for": row[10],
                    "xg_against": row[11],
                },
            )
            teams_by_source_id[row[0]] = team
        return teams_by_source_id

    def _import_players(self, source_conn: sqlite3.Connection, teams_by_source_id: dict[int, Team]) -> int:
        rows = source_conn.execute(
            """
            SELECT id, team_id, name, goals, assists, yellow_cards, red_cards,
                   shots_per_game, aerial_won_per_game, tackles, fouls, offsides
            FROM players
            ORDER BY id
            """
        ).fetchall()
        imported = 0
        for row in rows:
            team = teams_by_source_id.get(row[1])
            if team is None:
                continue
            Player.objects.update_or_create(
                source_player_id=row[0],
                defaults={
                    "team": team,
                    "name": row[2],
                    "goals": row[3],
                    "assists": row[4],
                    "cards": float((row[5] or 0) + (row[6] or 0)),
                    "shots_per_game": row[7],
                    "aerial_won_per_game": row[8],
                    "tackles": row[9],
                    "fouls": row[10],
                    "offsides": row[11],
                    "dribbles": None,
                    "goals_conceded": None,
                    "saves": None,
                },
            )
            imported += 1
        return imported

    def _import_goalkeepers(self, source_conn: sqlite3.Connection, teams_by_source_id: dict[int, Team]) -> int:
        rows = source_conn.execute(
            """
            SELECT id, team_id, team_name, league_name, season, games, minutes_90s,
                   ga, ga90, sota, saves, save_pct, cs, cs_pct,
                   pens_att, pens_allowed, pens_saved, pens_missed, pens_save_pct,
                   psxg, psxg_per_sot, psxg_net, psxg_net_per90
            FROM goalkeeper_stats
            ORDER BY id
            """
        ).fetchall()
        imported = 0
        for row in rows:
            team = teams_by_source_id.get(row[1])
            if team is None:
                team = Team.objects.filter(name=row[2]).first()
            if team is None:
                continue
            GoalkeeperStat.objects.update_or_create(
                source_goalkeeper_id=row[0],
                defaults={
                    "team": team,
                    "team_name": row[2],
                    "league_name": row[3],
                    "season": row[4],
                    "games": row[5],
                    "minutes_90s": row[6],
                    "ga": row[7],
                    "ga90": row[8],
                    "sota": row[9],
                    "saves": row[10],
                    "save_pct": row[11],
                    "cs": row[12],
                    "cs_pct": row[13],
                    "pens_att": row[14],
                    "pens_allowed": row[15],
                    "pens_saved": row[16],
                    "pens_missed": row[17],
                    "pens_save_pct": row[18],
                    "psxg": row[19],
                    "psxg_per_sot": row[20],
                    "psxg_net": row[21],
                    "psxg_net_per90": row[22],
                },
            )
            imported += 1
        return imported
