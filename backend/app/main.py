from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import httpx
import os
import asyncio
import base64

# FastAPIアプリケーションを作成
app = FastAPI()

# CORS設定（フロントエンドからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# モックの検索結果データ
mock_results: List[Dict[str, Any]] = [
    {
        "dockercompose": """
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
""",
        "create": "Accord33/synctimer (or created from AI)",
        "description": "Node.jsアプリとPostgreSQLデータベースを連携させる構成です。"
    },
    {
        "dockercompose": """
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
""",
        "create": "toma1128/ai2",
        "description": "PythonのFastAPIやFlaskなど、単一のバックエンドAPIを開発するためのシンプルな構成です。"
    },
    {
        "dockercompose": """
version: '3.8'
services:
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./build:/usr/share/nginx/html
""",
        "create": "toma1128/ai3",
        "description": "ReactやVueなどでビルドした静的なWebサイトをNginxで配信するための構成です。"
    },
    {
        "dockercompose": """
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
""",
        "create": "toma1128/ai4",
        "description": "DjangoやRailsアプリケーションとRedisをキャッシュとして連携させる構成です。"
    },
    {
        "dockercompose": """
version: '3.8'
services:
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    depends_on:
      - db
  db:
    image: mysql:5.7
    environment:
      MYSQL_DATABASE: wordpress
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: rootpassword
""",
        "create": "toma1128/ai5",
        "description": "WordPressとMySQLデータベースを起動するための標準的な構成です。"
    },
]

# /mock エンドポイント
@app.get("/mock")
def mock(q: Optional[str] = None):
    """
    検索クエリに基づいてモックデータを返すエンドポイント
    """
    print(f"検索クエリ '{q}' を受信しました。")

    # フロントエンドが必要とするレスポンス形式に合わせてデータを整形
    response_data = {
        "results": mock_results,
        "total": len(mock_results),
        "page": 1,
        "limit": 10,
        "query": q if q else ""
    }

    return response_data


GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_API_TOKEN")

"""
指定したリポジトリのDocker Composeファイルを取得する
"""
async def get_docker_compose(client: httpx.AsyncClient, repo_full_name: str) -> Optional[str]:
  content_url = f"{GITHUB_API_URL}/repos/{repo_full_name}/contents/docker-compose.yml"
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

@app.get("/search")
async def search(
    q: str = Query(..., min_length=1, description="検索キーワード"),
    page: int = Query(1, ge=1, description="ページ番号"),
    limit: int = Query(10, ge=1, le=100, description="1ページあたりの取得件数")
):
    search_query = f"{q} filename:docker-compose.yml"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DockDockGo-App"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    params = {
        "q": search_query,
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": limit,
    }

    async with httpx.AsyncClient() as client:
        try:
            search_response = await client.get(f"{GITHUB_API_URL}/search/repositories", params=params)
            search_response.raise_for_status()  # 2xx以外のステータスコードで例外を発生
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"サービス利用不可: GitHub APIへの接続に失敗しました。 {exc}")
        except httpx.HTTPStatusError as exc:
            # GitHubからのエラーレスポンスをそのままクライアントに返す
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

    search_data = search_response.json()
    repositories = search_data.get("items", [])

    tasks = [get_docker_compose(client, repo["full_name"]) for repo in repositories]
    docker_compose_contents = await asyncio.gather(*tasks)

    results = []
    for repo, content in zip(repositories, docker_compose_contents):
      if content:
          results.append({
            "dockercompose": content,
            "create": repo["full_name"],
            "description": repo.get("description", "no description")
          })

    return {
        "results": results,
        "total": search_data.get("total_count", 0),
        "page": page,
        "limit": limit,
        "query": q
    }

# ルートURL
@app.get("/")
def read_root():
    return {"message": "Welcome to DockDockGo Simple API"}