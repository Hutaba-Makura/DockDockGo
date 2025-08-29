from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Union
from ...services.github_service import search_github_repositories
from ...services.mock_data import get_mock_data
from ...schemas.search import SearchResponse, MockResponse

router = APIRouter(tags=["search"])

@router.get("/mock", response_model=Union[SearchResponse, MockResponse])
async def mock(q: Optional[str] = None):
    """
    検索クエリに基づいてモックデータを返すエンドポイント
    """
    mock_response = get_mock_data(q)

    if not mock_response.results and q:
        print(f"モックデータが見つからなかったため、GitHub検索を実行します: q='{q}'")
        # モックで見つからなければ、本番のGitHub検索を実行
        return await search_github_repositories(query=q, page=1, limit=5)

    return mock_response

@router.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, description="検索キーワード"),
    page: int = Query(1, ge=1, description="ページ番号"),
    limit: int = Query(5, ge=1, le=100, description="1ページあたりの取得件数")
):
    """
    GitHub APIを使用してDocker Composeファイルを含むリポジトリを検索するエンドポイント
    """
    return await search_github_repositories(q, page, limit)
