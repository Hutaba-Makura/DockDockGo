"""
FastAPI アプリケーションのメインファイル
アプリケーションの起動、ルータ登録、CORS設定を担当
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes_search import router as search_router

# ログ設定の初期化
setup_logging()

# FastAPI アプリケーションの作成
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="DockDockGo 検索API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(search_router, prefix=settings.api_v1_prefix)

# ヘルスチェックエンドポイント
@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy", "service": settings.app_name}

# ルートエンドポイント
@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {
        "message": "DockDockGo API",
        "version": settings.app_version,
        "docs": "/docs"
    }
