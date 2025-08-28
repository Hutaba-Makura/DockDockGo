import os
from typing import List
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class Settings:
    # CORS設定
    CORS_ORIGINS: List[str] = ["*"]

    # GitHub API設定
    GITHUB_API_URL: str = "https://api.github.com"
    GITHUB_TOKEN: str = os.getenv("GITHUB_API_TOKEN", "")

    # アプリケーション設定
    APP_NAME: str = "DockDockGo"
    APP_VERSION: str = "1.0.0"

settings = Settings()

if settings.GITHUB_TOKEN:
    print("✅ GITHUB_API_TOKENが正常に読み込まれました。")
else:
    print("⚠️ GITHUB_API_TOKENが読み込めていません。.envファイルの場所と内容を確認してください。")