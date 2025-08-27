"""
検索APIルーター
/search エンドポイントの実装
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.schemas.search import SearchResponse, ErrorResponse
from app.services.search_engine import search_engine

router = APIRouter()


@router.get(
    "/search",
    response_model=SearchResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="検索API",
    description="キーワードによる検索を実行し、結果を返却します"
)
async def search(
    q: str = Query(..., description="検索クエリ", min_length=1, max_length=500),
    page: int = Query(1, description="ページ番号", ge=1),
    limit: int = Query(10, description="1ページあたりの結果数", ge=1, le=100)
):
    """
    検索を実行するエンドポイント
    
    - **q**: 検索クエリ（必須）
    - **page**: ページ番号（デフォルト: 1）
    - **limit**: 1ページあたりの結果数（デフォルト: 10、最大: 100）
    """
    try:
        # 検索エンジンで検索実行
        results, total = await search_engine.search(query=q, page=page, limit=limit)
        
        # レスポンス作成
        response = SearchResponse(
            results=results,
            total=total,
            page=page,
            limit=limit,
            query=q
        )
        
        return response
        
    except Exception as e:
        # エラーハンドリング
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal Server Error",
                "message": "検索処理中にエラーが発生しました",
                "status": 500
            }
        )
