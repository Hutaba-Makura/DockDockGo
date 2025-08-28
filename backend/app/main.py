from fastapi import FastAPI
from .core.config import settings
from .core.middleware import setup_cors_middleware
from .api.routes import search, health

# FastAPIアプリケーションを作成
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Docker Composeファイルを検索するAPI"
)

# CORSミドルウェアを設定
setup_cors_middleware(app)

# ルーターを登録
app.include_router(health.router)
app.include_router(search.router)