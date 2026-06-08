# JanBaat — "Ab Public Bolegi"

India's first neutral, district-level public opinion platform.

## Repos

| Repo | Stack | Status |
|---|---|---|
| `janbaat-backend/` | FastAPI + SQLAlchemy + Celery | Phase 0 ✅ |
| `janbaat-app/` | React Native (Expo SDK52) | Phase 0 ✅ |

## Quick Start (after adding credentials)

### Backend
```bash
cd janbaat-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in your credentials
alembic upgrade head
python scripts/seed_locations.py
uvicorn app.main:app --reload
```

### Frontend
```bash
cd janbaat-app
npm install
cp .env.example .env   # fill in your credentials
npx expo start
```

## Build Phases
- **Phase 0** — Scaffolding ✅
- **Phase 1** — Database schema + migrations
- **Phase 2** — Backend foundation (auth middleware, health check)
- **Phase 3** — Auth + Location APIs
- **Phase 4** — Posts + Feed + Votes APIs
- **Phase 5** — Comments + Search + Notifications APIs
- **Phase 6** — Celery workers + AI pipeline
- **Phase 7** — Mobile foundation (auth flow on device)
- **Phase 8** — Mobile core screens (feed, create, vote)
- **Phase 9** — Mobile secondary screens (dashboard, search, profile)
- **Phase 10** — Testing
- **Phase 11** — Deploy (Railway + EAS)
