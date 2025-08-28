import httpx
import base64
import asyncio
import logging
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from ..core.config import settings
from ..schemas.search import SearchResult, SearchResponse

logger = logging.getLogger(__name__)

async def get_docker_compose(client: httpx.AsyncClient, repo_full_name: str) -> Optional[str]:
    """
    指定したリポジトリのDocker Composeファイルを取得する
    """
    content_url = f"{settings.GITHUB_API_URL}/repos/{repo_full_name}/contents/docker-compose.yml"
    try:
        response = await client.get(content_url)
        response.raise_for_status()
        data = response.json()
        if "content" in data:
            return base64.b64decode(data["content"]).decode('utf-8')
    except httpx.HTTPError as e:
        if e.response.status_code == 404:
            logger.info(f"ファイルが見つかりません: {repo_full_name}/docker-compose.yml")
        else:
            logger.error(f"ファイル取得中にHTTPエラー: {e.response.status_code}, Repo: {repo_full_name}")
    except Exception as e:
        logger.error(f"ファイル取得中に予期せぬエラー: {e}, Repo: {repo_full_name}")
    return None

async def search_github_repositories(
    query: str,
    page: int = 1,
    limit: int = 5
) -> SearchResponse:
    """
    GitHub APIを使用してDocker Composeファイルを含むリポジトリを検索する
    """
    search_query = f"{query} in:name,readme"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": settings.APP_NAME
    }
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    result = []
    current_page = page
    total_count = 0

    async with httpx.AsyncClient(headers=headers) as client:
        while len(result) < limit:
            params = {
                "q": search_query,
                "sort": "stars",
                "order": "desc",
                "page": page,
                "per_page": limit,
            }
            try:
                search_response = await client.get(
                    f"{settings.GITHUB_API_URL}/search/repositories",
                    params=params
                )
                search_response.raise_for_status()
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=503,
                    detail=f"サービス利用不可: GitHub APIへの接続に失敗しました。 {exc}"
                )
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 403:
                    logger.warning("GitHub APIのレート制限に達したか、認証情報が無効です。")
                    raise HTTPException(status_code=403, detail="GitHub APIのレート制限に達したか、認証情報が無効です。")
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=exc.response.json()
                )
            search_data = search_response.json()
            repositories = search_data.get("items", [])
            total_count = search_data.get("total_count", 0)

            if not repositories:
                return SearchResponse(results=[], total=0, page=page, limit=limit, query=query)

            logger.info(f"{total_count}件のリポジトリが見つかりました。各リポジトリのdocker-compose.ymlを探します。")


            tasks = [get_docker_compose(client, repo["full_name"]) for repo in repositories]
            docker_compose_contents = await asyncio.gather(*tasks)

            results = []
            for repo_info in repositories:

                content = await get_docker_compose(client, repo_info["full_name"])

                if content:
                    results.append(SearchResult(
                        dockercompose=content,
                        create=repo_info.get("full_name", "N/A"),
                        description=repo_info.get("description", "説明がありません。")
                    ))
                await asyncio.sleep(0.5)

    logger.info(f"最終的に{len(results)}件のdocker-compose.ymlを持つリポジトリを返します。")
    return SearchResponse(
        results=results,
        total=total_count, # totalはあくまでキーワードにヒットしたリポジトリの総数
        page=page,
        limit=limit,
        query=query
    )
