# API Documentation

## Response Format

Success:

```json
{
  "success": true,
  "data": {},
  "meta": {},
  "errors": []
}
```

Error:

```json
{
  "success": false,
  "data": null,
  "meta": {},
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "team_a and team_b must be different."
    }
  ]
}
```

## Team Endpoints

- `GET /api/teams/`
- `GET /api/teams/{team_id}/`
- `GET /api/teams/{team_id}/stats/`
- `GET /api/teams/{team_id}/strengths-weaknesses/`
- `GET /api/teams/{team_id}/players/`
- `GET /api/teams/{team_id}/player-impact/`

## Player Endpoints

- `GET /api/players/`
- `GET /api/players/{player_id}/`
- `GET /api/players/{player_id}/stats/`

## Comparison Endpoints

- `GET /api/compare/?team_a={id}&team_b={id}`
- `GET /api/compare/summary/?team_a={id}&team_b={id}`
- `GET /api/head-to-head/?team_a={id}&team_b={id}`

## Prediction Endpoints

- `GET /api/predict/?team_a={id}&team_b={id}`
- `GET /api/predict/probabilities/?team_a={id}&team_b={id}`
- `GET /api/predict/exact-score/?team_a={id}&team_b={id}`
- `GET /api/predict/over-under/?team_a={id}&team_b={id}&line=2.5`
- `GET /api/predict/btts/?team_a={id}&team_b={id}`
- `GET /api/predict/simulation/?team_a={id}&team_b={id}&runs=100000`
- `GET /api/predict/model-breakdown/?team_a={id}&team_b={id}`

## Ratings Endpoints

- `GET /api/ratings/elo/`
- `GET /api/ratings/elo/{team_id}/`
- `GET /api/ratings/power/`
- `GET /api/ratings/power/{team_id}/`

## Analytics Endpoints

- `GET /api/analytics/correlation/`
- `GET /api/analytics/feature-importance/`
- `GET /api/analytics/league-averages/`

## Example Prediction Request

```bash
curl "http://127.0.0.1:8000/api/predict/?team_a=1&team_b=2"
```

## Example Prediction Response

```json
{
  "success": true,
  "data": {
    "teams": {
      "team_a": {"id": 1, "name": "Arsenal"},
      "team_b": {"id": 2, "name": "Manchester City"}
    },
    "overall_prediction": {
      "team_a_win": 0.41,
      "draw": 0.24,
      "team_b_win": 0.35,
      "predicted_winner": "Arsenal",
      "confidence_score": 68.4,
      "confidence_level": "Medium"
    },
    "expected_goals": {
      "team_a": 1.63,
      "team_b": 1.29
    },
    "most_likely_scores": [
      {"score": "1-1", "probability": 0.11},
      {"score": "1-0", "probability": 0.10},
      {"score": "2-1", "probability": 0.09}
    ],
    "over_under": {
      "over_0_5": 0.93,
      "under_0_5": 0.07,
      "over_1_5": 0.71,
      "under_1_5": 0.29,
      "over_2_5": 0.49,
      "under_2_5": 0.51,
      "over_3_5": 0.28,
      "under_3_5": 0.72
    },
    "both_teams_to_score": {
      "yes": 0.56,
      "no": 0.44
    },
    "team_comparison": {
      "overall": "Arsenal",
      "attack": "Arsenal",
      "defense": "Manchester City",
      "xg": "Arsenal",
      "discipline": "Even",
      "goalkeeper": "Arsenal",
      "player_impact": "Arsenal"
    },
    "strengths": {"team_a": ["elite attack"], "team_b": ["strong defense"]},
    "weaknesses": {"team_a": [], "team_b": ["discipline risk"]},
    "risk_notes": [],
    "model_breakdown": {}
  },
  "meta": {},
  "errors": []
}
```

## Validation Rules

- `team_a` is required.
- `team_b` is required.
- `team_a` and `team_b` must be different.
- Team IDs must exist.
- `line` must be greater than 0.
- `runs` must be between 1000 and 200000.
