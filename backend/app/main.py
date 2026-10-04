"""RakshaScan Backend Application Entrypoint."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes.analysis import router as analysis_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Evidence-based financial scam and trust verification platform API. "
        "Provides safe multi-input analysis, SSRF protection, Trust Chain verification, "
        "Scam Journey reconstruction, Safe Response, and recovery guidance."
    ),
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)


# Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
        return response


app.add_middleware(SecurityHeadersMiddleware)

# Production-safe CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Register API routes under /api/v1
app.include_router(analysis_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check probe compliant with Production Hardening specification."""
    return {
        "status": "ok",
    }


@app.get("/", tags=["Root"])
async def root():
    """API Root summary."""
    return {
        "message": "Welcome to RakshaScan Analysis Engine API",
        "version": settings.VERSION,
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "Disabled in production",
        "phase": "Phase 11 — Production Hardened",
    }

