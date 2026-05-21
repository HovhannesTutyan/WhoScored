# Statistical Methods

## Derived Team Metrics

Formulas:

- `win_rate = wins / matches`
- `draw_rate = draws / matches`
- `loss_rate = losses / matches`
- `goals_for_per_game = goals_for / matches`
- `goals_against_per_game = goals_against / matches`
- `points_per_game = points / matches`
- `xg_for_per_game = xg_for / matches`
- `xg_against_per_game = xg_against / matches`
- `goal_difference = goals_for - goals_against`
- `goal_difference_per_game = goal_difference / matches`
- `xg_difference = xg_for - xg_against`
- `xg_difference_per_game = xg_difference / matches`
- `finishing_efficiency = goals_for / xg_for`
- `attacking_overperformance = goals_for - xg_for`
- `defensive_overperformance = xg_against - goals_against`

All divisions use safe division helpers so missing values or zero denominators return `null` instead of crashing.

## Player Impact

Attack impact:

- `goals * 0.45`
- `assists * 0.30`
- `shots_per_game * 0.10`
- `dribbles * 0.10`
- `aerial_won_per_game * 0.05`

Defensive impact:

- `tackles * 0.35`
- `aerial_won_per_game * 0.20`
- `fouls * -0.15`
- `cards * -0.15`

Goalkeeper impact:

- `saves * 0.40`
- `goals_conceded * -0.40`

Discipline impact:

- `cards * -0.50`
- `fouls * -0.30`
- `offsides * -0.20`

Team player impact uses all available players and normalizes by player count because starting lineup data is not available.

## Normalization

Implemented in `apps/math_utils/normalization.py`:

- Min-max normalization
- Reverse normalization for negative stats
- Z-score normalization
- Percentile rank

## Team Strength Index

Component weights from `apps/common/constants.py`:

- points per game: `0.20`
- goal difference: `0.20`
- xG difference: `0.25`
- attacking score: `0.15`
- defensive score: `0.15`
- player impact: `0.05`

The final score is scaled to `0-100`.

## Attack and Defense Strength

- `attack_strength = team_goals_for_per_game / league_average_goals_for_per_game`
- `defense_weakness = team_goals_against_per_game / league_average_goals_against_per_game`
- `xg_attack_strength = team_xg_for_per_game / league_average_xg_for_per_game`
- `xg_defense_weakness = team_xg_against_per_game / league_average_xg_against_per_game`

## Poisson Model

Implemented in `apps/math_utils/poisson.py`.

- `P(X = k) = (lambda^k * e^-lambda) / k!`

Goal-based lambdas:

- `lambda_A = league_avg_goals_per_team * teamA_attack_strength * teamB_defense_weakness`
- `lambda_B = league_avg_goals_per_team * teamB_attack_strength * teamA_defense_weakness`

The score matrix is used to derive:

- win/draw/loss probabilities
- most likely scorelines
- over/under lines
- BTTS
- clean sheet probabilities

## xG Poisson Model

Implemented in `apps/math_utils/xg_poisson.py`.

- `lambda_A = teamA_xg_for_per_game * teamB_xg_against_per_game / league_avg_xg_per_team`
- `lambda_B = teamB_xg_for_per_game * teamA_xg_against_per_game / league_avg_xg_per_team`

## Blended Poisson Model

Implemented in `apps/math_utils/blended_poisson.py`.

- `lambda_A = goals_based_lambda_A * 0.45 + xg_based_lambda_A * 0.55`
- `lambda_B = goals_based_lambda_B * 0.45 + xg_based_lambda_B * 0.55`

## Monte Carlo Simulation

Implemented in `apps/math_utils/monte_carlo.py` and `apps/simulation/services.py`.

- Poisson sampling uses the selected model lambdas.
- Safety limits: minimum `1000`, maximum `200000` runs.

## Elo Rating

A full Elo update path requires historical match results and is intentionally marked unavailable until a proper historical match model exists.

## Power Rating

Weights:

- Elo: `0.30`
- xG rating: `0.30`
- goal difference rating: `0.20`
- player rating: `0.10`
- defensive rating: `0.10`

When Elo is unavailable, its weight is redistributed equally to xG and goal difference.

## Regression to Mean

Rule-based notes are generated when:

- goals exceed xG by a meaningful margin
- goals lag xG by a meaningful margin
- goals against is much lower than xG against
- goals against is much higher than xG against

## Ensemble Prediction

Weights from `apps/common/constants.py`:

- poisson: `0.20`
- xg_poisson: `0.25`
- blended_poisson: `0.25`
- team_strength: `0.15`
- player_impact: `0.10`
- power_rating: `0.05`

Unavailable models are removed and the remaining weights are redistributed proportionally.

## Confidence Score

The confidence model combines:

- data completeness
- difference between teams
- model agreement
- sample size
- xG consistency
- player data completeness

Output:

- `confidence_score` from `0` to `100`
- `confidence_level`: `Low`, `Medium`, `High`
- `confidence_explanation`

## Current Limitations

- No historical match table yet, so Elo and true head-to-head history are not available.
- Some player-level attacking and goalkeeper fields are still partially missing in the imported scraper dataset.
- This system is deterministic and data-driven; it does not yet incorporate injuries, suspensions, odds, or squad rotation.
