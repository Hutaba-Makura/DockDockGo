import httpx
import base64
import asyncio
import logging
from typing import Optional, List
from fastapi import HTTPException
from ..core.config import settings
from ..schemas.search import SearchResult, SearchResponse
from asyncio import Semaphore

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
    limit: int = 10
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

    results = []
    current_page = page
    total_count = 0

    sem = Semaphore(5)

    async def fetch_with_semaphore(repo_full_name: str, client: httpx.AsyncClient):
        async with sem:
            # 0.2秒の軽い待機を入れるとさらに安定性が増す
            await asyncio.sleep(0.2)
            return await get_docker_compose(client, repo_full_name)

    async with httpx.AsyncClient(headers=headers) as client:
        while len(results) < limit:
            params = {
                "q": search_query,
                "sort": "stars",
                "order": "desc",
                "page": current_page,
                "per_page": limit,
            }
            try:
                search_response = await client.get(
                    f"{settings.GITHUB_API_URL}/search/repositories",
                    params=params
                )
                search_response.raise_for_status()
            except Exception as e:
                logger.error(f"検索APIでエラー: {e}")
                break
            search_data = search_response.json()
            repositories = search_data.get("items", [])
            if current_page == page:
                total_count = search_data.get("total_count", 0)
            if not repositories:
                break

            logger.info(f"{total_count}件のリポジトリが見つかりました。各リポジトリのdocker-compose.ymlを探します。")

            tasks = [get_docker_compose(client, repo["full_name"]) for repo in repositories]
            contents = await asyncio.gather(*tasks, return_exceptions=True)

            for repo_info, content in zip(repositories, contents):
                if content and not isinstance(content, Exception):
                    results.append(SearchResult(
                        dockercompose=content,
                        create=repo_info.get("full_name", "N/A"),
                        description=repo_info.get("description", "説明がありません。")
                    ))
                    if len(results) >= limit:
                        break

            if len(results) >= limit:
                break

            current_page += 1

    logger.info(f"最終的に{len(results)}件のdocker-compose.ymlを持つリポジトリを返します。")
    return SearchResponse(
        results=results,
        total=total_count, # totalはあくまでキーワードにヒットしたリポジトリの総数
        page=page,
        limit=limit,
        query=query
    )
