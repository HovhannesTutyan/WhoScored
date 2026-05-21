# Football Prediction API

A modular Django REST Framework project for football statistics, team comparison, ratings, analytics, and pure statistics-based match prediction.

## Project Layout

- `config/`: Django settings and root URL wiring
- `apps/common/`: shared responses, exceptions, pagination, validators, constants, and import command
- `apps/math_utils/`: pure statistical and mathematical utilities
- `apps/teams/`: team models and team API endpoints
- `apps/players/`: player models and player API endpoints
- `apps/statistics/`: derived metrics, team strength, player impact, and strengths/weaknesses services
- `apps/comparison/`: team-vs-team comparison API
- `apps/prediction/`: prediction orchestration, ensemble logic, and confidence scoring
- `apps/ratings/`: Elo fallback handling and power ratings
- `apps/simulation/`: Monte Carlo simulation services
- `apps/analytics/`: correlations, feature importance, and league averages
- `tests/`: shared test factories and math utility tests

## Setup

1. Create or activate a virtual environment.
2. Install dependencies:

```bash
pip install -r football_prediction/requirements.txt
```

3. Run migrations:

```bash
cd football_prediction
python manage.py migrate
```

4. Import the scraped data from the existing SQLite database in the workspace root:

```bash
python manage.py import_scraped_data --clear
```

5. Start the server:

```bash
python manage.py runserver
```

## Running Tests

```bash
cd football_prediction
python manage.py test
```

## Example Requests

```bash
GET /api/teams/
GET /api/teams/1/stats/
GET /api/compare/?team_a=1&team_b=2
GET /api/predict/?team_a=1&team_b=2
GET /api/predict/simulation/?team_a=1&team_b=2&runs=100000
GET /api/analytics/league-averages/
```

## Data Import Notes

This project keeps its own Django database (`football_prediction/db.sqlite3`) and imports the current scraped dataset from the workspace root `team_recent_form.db`.

## Limitations

- There is no full historical match model yet, so Elo and head-to-head endpoints return a clear not-enough-data response.
- Player dribbles, individual goalkeeper saves, and individual goals conceded are not currently present in the scraper DB for every player, so those inputs are treated safely as missing values.
- Predictions are statistics-based only and do not include injuries, lineups, schedule congestion, or bookmaker prices.
