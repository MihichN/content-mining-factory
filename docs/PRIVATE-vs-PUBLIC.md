# Public showcase vs private codebase

This repository is a **portfolio showcase**, not the production application.

## Public (this repo)

| Included | Purpose |
|----------|---------|
| README, architecture docs | Explain what was built and how |
| Pipeline diagrams | Show system design skills |
| `examples/scoring_demo.py` | Runnable **illustration** of highlight scoring |
| Screenshots | Visual proof of the UI |
| MIT license on showcase materials | Standard open-source portfolio practice |

## Private (not in this repo)

| Excluded | Why |
|----------|-----|
| `api/` — 1300+ lines FastAPI | Core product API |
| `content_factory/workers/` | Download, Whisper, FFmpeg, publish pipeline |
| `dashboard/` | Full React admin UI |
| `docker-compose*.yml`, `DEPLOY.md` | One-command deployment |
| Ingest, feed groups, registry | Business logic for channel automation |
| Publisher OAuth (YouTube, Instagram) | Integration secrets & flows |
| Planner, campaigns, accounts | Content ops product features |
| Tests against real pipeline | Tied to private modules |
