import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.config import settings

# ─── Sentry ──────────────────────────────────────────────────────────────────
if settings.sentry_dsn:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)

# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url=None,
)

# ─── Middleware ───────────────────────────────────────────────────────────────
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers (registered in Phase 3+) ────────────────────────────────────────
# from app.routers import auth, locations, posts, feed, votes, comments
# from app.routers import dashboard, search, profile, notifications
# app.include_router(auth.router, prefix=settings.api_prefix)
# app.include_router(locations.router, prefix=settings.api_prefix)
# ... (uncomment as each phase is built)


# ─── Health ───────────────────────────────────────────────────────────────────
@app.get("/health", tags=["health"])
async def health():
    from datetime import datetime, timezone

    from app.core.cache import ping_redis
    from app.database import engine

    db_ok = False
    redis_ok = False

    try:
        async with engine.connect() as conn:
            await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        db_ok = True
    except Exception:
        pass

    try:
        redis_ok = await ping_redis()
    except Exception:
        pass

    return {
        "status": "healthy" if db_ok and redis_ok else "degraded",
        "db": db_ok,
        "redis": redis_ok,
        "env": settings.app_env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
