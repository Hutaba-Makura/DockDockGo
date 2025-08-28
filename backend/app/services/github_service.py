import httpx
import base64
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import HTTPException
from ..core.config import settings
from ..schemas.search import SearchResult, SearchResponse

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
            # contentはBase64でエンコードされているためデコードする
            decoded_content = base64.b64decode(data["content"]).decode('utf-8')
            return decoded_content
    except httpx.HTTPError as e:
        if e.response.status_code == 404:
            return None
        return e.response.status_code
    except Exception as e:
        return None

async def search_github_repositories(
    query: str,
    page: int = 1,
    limit: int = 10
) -> SearchResponse:
    """
    GitHub APIを使用してDocker Composeファイルを含むリポジトリを検索する
    """
    search_query = f"{query} filename:docker-compose.yml"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DockDockGo-App"
    }
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"

    params = {
        "q": search_query,
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": limit,
    }

    async with httpx.AsyncClient() as client:
        try:
            search_response = await client.get(
                f"{settings.GITHUB_API_URL}/search/repositories", 
                params=params,
                headers=headers
            )
            search_response.raise_for_status()
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503, 
                detail=f"サービス利用不可: GitHub APIへの接続に失敗しました。 {exc}"
            )
        except httpx.HTTPStatusError as exc:
            # GitHubからのエラーレスポンスをそのままクライアントに返す
            raise HTTPException(
                status_code=exc.response.status_code, 
                detail=exc.response.json()
            )

    search_data = search_response.json()
    repositories = search_data.get("items", [])

    # 並行してDocker Composeファイルを取得
    tasks = [get_docker_compose(client, repo["full_name"]) for repo in repositories]
    docker_compose_contents = await asyncio.gather(*tasks)

    # 結果を整形
    results = []
    for repo, content in zip(repositories, docker_compose_contents):
        if content:
            results.append(SearchResult(
                dockercompose=content,
                create=repo["full_name"],
                description=repo.get("description", "no description")
            ))

    return SearchResponse(
        results=results,
        total=search_data.get("total_count", 0),
        page=page,
        limit=limit,
        query=query
    )
