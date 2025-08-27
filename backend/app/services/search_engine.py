"""
検索エンジンサービス
実際の検索処理を担当（現在はモック実装）
"""
import logging
from typing import List, Tuple
from app.schemas.search import SearchResult
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)


class SearchEngine:
    """検索エンジンクラス"""
    
    def __init__(self):
        # モックデータ（実際の実装では外部APIやデータベースを使用）
        self.mock_data = [
            {
                "id": "1",
                "title": "React の使い方 - 初心者向けガイド",
                "description": "React の基本的な使い方から応用まで、初心者でも分かりやすく解説します。",
                "url": "https://example.com/react-guide",
                "score": 0.95,
                "published_at": datetime.now() - timedelta(days=1)
            },
            {
                "id": "2", 
                "title": "TypeScript 入門 - 型安全な開発",
                "description": "TypeScript の基本概念から実践的な使い方まで詳しく説明します。",
                "url": "https://example.com/typescript-intro",
                "score": 0.88,
                "published_at": datetime.now() - timedelta(days=3)
            },
            {
                "id": "3",
                "title": "FastAPI で Web API を構築する",
                "description": "Python FastAPI を使用した高速な Web API の構築方法を紹介します。",
                "url": "https://example.com/fastapi-tutorial",
                "score": 0.82,
                "published_at": datetime.now() - timedelta(days=5)
            },
            {
                "id": "4",
                "title": "Docker コンテナ化のベストプラクティス",
                "description": "Docker を使用したアプリケーションのコンテナ化について解説します。",
                "url": "https://example.com/docker-best-practices",
                "score": 0.78,
                "published_at": datetime.now() - timedelta(days=7)
            },
            {
                "id": "5",
                "title": "Mantine UI ライブラリの活用方法",
                "description": "React 用の UI ライブラリ Mantine の使い方とカスタマイズ方法。",
                "url": "https://example.com/mantine-usage",
                "score": 0.75,
                "published_at": datetime.now() - timedelta(days=10)
            }
        ]
    
    async def search(self, query: str, page: int = 1, limit: int = 10) -> Tuple[List[SearchResult], int]:
        """
        検索を実行
        
        Args:
            query: 検索クエリ
            page: ページ番号
            limit: 1ページあたりの結果数
            
        Returns:
            (検索結果リスト, 総件数) のタプル
        """
        logger.info(f"検索実行: query='{query}', page={page}, limit={limit}")
        
        # モック実装: クエリに基づいてフィルタリング
        filtered_results = []
        for item in self.mock_data:
            if (query.lower() in item["title"].lower() or 
                query.lower() in item["description"].lower()):
                filtered_results.append(item)
        
        # スコアでソート
        filtered_results.sort(key=lambda x: x["score"], reverse=True)
        
        # ページネーション
        total = len(filtered_results)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        page_results = filtered_results[start_idx:end_idx]
        
        # SearchResult オブジェクトに変換
        results = [
            SearchResult(
                id=item["id"],
                title=item["title"],
                description=item["description"],
                url=item["url"],
                score=item["score"],
                published_at=item["published_at"]
            )
            for item in page_results
        ]
        
        logger.info(f"検索完了: {len(results)}件の結果を返却")
        return results, total


# シングルトンインスタンス
search_engine = SearchEngine()
