import os
from typing import List

class Settings:
    # CORS設定
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # GitHub API設定
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_TOKEN: str = os.getenv("GITHUB_API_TOKEN", "")
    
    # アプリケーション設定
    APP_NAME: str = "DockDockGo"
    APP_VERSION: str = "1.0.0"

settings = Settings()
