# Content Mining Factory

> **Portfolio showcase** — architecture documentation and illustrative samples.  
> This is **not** the full production codebase. See [docs/PRIVATE-vs-PUBLIC.md](./docs/PRIVATE-vs-PUBLIC.md).

Automated pipeline concept: long videos and YouTube compilations → vertical Shorts/Reels with multi-signal highlight detection, transcription, and content ops UI.

🇷🇺 Полное описание на русском: [README.ru.md](./README.ru.md)

---

## What this repo is

| ✅ Included | ❌ Not included (private) |
|-------------|---------------------------|
| Architecture & pipeline docs | Full FastAPI backend |
| System diagrams | Celery workers (download/analyze/render) |
| Scoring demo (`examples/`) | React dashboard source |
| Screenshots (add yours) | Docker deploy stack |
| Feature overview | Ingest, publishing, planner |

**You cannot clone this repo and run the full service 1:1.** That is intentional.

---

## The product (what was built)

**Content Mining Factory** is a private full-stack system I designed and implemented:

- Ingest YouTube channel groups on a schedule
- Download → transcribe (Whisper) → analyze audio/video/text signals
- Score and cluster highlight moments by content category
- Render 1080×1920 clips with optional facecam layout and branding
- Publish to YouTube Shorts / Instagram Reels with a planner UI

```mermaid
flowchart LR
  YT[YouTube sources] --> DL[Download]
  DL --> AN[Analyze]
  AN --> HL[Highlights]
  HL --> ED[Render]
  ED --> PUB[Publish]
```

---

## Tech stack

**Backend:** Python, FastAPI, Celery, PostgreSQL, Redis, MinIO, yt-dlp, faster-whisper, OpenCV, FFmpeg

**Frontend:** React, TypeScript, Vite, TanStack Query, Tailwind

**Infra:** Docker Compose, separate download/process worker queues, Celery Beat

---

## Try the scoring demo

The only runnable code in this repo — a simplified highlight scoring illustration:

```bash
python examples/scoring_demo.py
```

Example output:

```
Content Mining Factory — scoring demo

Profile: streamer_clip  |  peaks: 6  |  highlights: 2

  #1   90.0s –  97.0s   score=  82.5
  #2   12.0s –  19.0s   score=  58.2
```

---

## Documentation

| Doc | Content |
|-----|---------|
| [ARCHITECTURE.md](./docs/ARCHITECTURE.md) | System design, queues, pipeline stages |
| [PRIVATE-vs-PUBLIC.md](./docs/PRIVATE-vs-PUBLIC.md) | What's open vs closed |
| [README.ru.md](./README.ru.md) | Full project description (RU) |

---

## Key design decisions

1. **Re-Clip over raw VOD** — process 3–15 min compilations instead of 4-hour streams
2. **Split worker queues** — download (I/O) vs process (CPU/Whisper) for throughput
3. **Resume from stage** — transcript in S3 before continuing analysis after crashes
4. **Category profiles** — 22 categories × RU/EN with different scoring weights and clip lengths
5. **Adaptive highlight cap** — limit clips by video duration + quality floor, not fixed top-N
6. **Registry + watchdog** — dedupe ingest, recover stuck jobs, cleanup orphan records

---

## Screenshots

Add captures to `docs/screenshots/`:

- Dashboard overview
- Job pipeline with progress
- Feed group + video registry
- Rendered clips list

---

## License

MIT — applies to **this showcase repository** (docs + examples).  
The private production codebase is proprietary.

---

## Author

Portfolio project — replace with your links:

- GitHub: `@yourusername`
- LinkedIn: `your-profile`
