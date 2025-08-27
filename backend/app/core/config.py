"""
設定管理モジュール
pydantic-settingsを使用して環境変数から設定を読み込み
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # アプリケーション設定
    app_name: str = "DockDockGo API"
    app_version: str = "1.0.0"
    
    # CORS設定
    backend_cors_origins: List[str] = ["http://localhost:3000"]
    
    # ログ設定
    log_level: str = "INFO"
    
    # API設定
    api_v1_prefix: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
