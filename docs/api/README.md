# API

Start: `uvicorn iot_pm.api.app:app --reload`. Swagger UI: `http://localhost:8000/docs`.

`GET /health`: process readiness only.
`GET /models`: currently available rule-based inference method.
`POST /alerts/score`: validates one sensor payload then returns severity and threshold reasons.

Example:
```bash
curl -X POST http://localhost:8000/alerts/score -H 'Content-Type: application/json' -d '{"machine_id":"motor-001","timestamp":"2026-01-01T10:00:00Z","temperature_c":95,"vibration_mm_s":7.2,"pressure_bar":7.4,"rpm":1730,"operating_hours":550}'
```
No authentication, rate limiting or durable alert history is supplied by this research demonstration; add those before deployment.
