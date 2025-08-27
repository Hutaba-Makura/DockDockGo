"""
ログ設定モジュール
アプリケーション全体のログ設定を管理
"""
import logging
from app.core.config import settings


def setup_logging():
    """
    ログ設定を初期化
    """
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ]
    )
    
    # 外部ライブラリのログレベルを調整
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
