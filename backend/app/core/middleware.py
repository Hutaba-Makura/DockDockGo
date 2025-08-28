from fastapi.middleware.cors import CORSMiddleware
from .config import settings

def setup_cors_middleware(app):
    """CORSミドルウェアを設定する"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
