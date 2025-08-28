from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import httpx
import os

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
        "id": "1",
        "title": "FastAPI ドキュメント",
        "description": "FastAPI の公式ドキュメントです。使い方やチュートリアルが豊富にあります。",
        "url": "https://fastapi.tiangolo.com/",
        "score": 0.98,
        "publishedAt": "2023-10-26T12:00:00Z"
    },
    {
        "id": "2",
        "title": "Mantine UI - Reactコンポーネントライブラリ",
        "description": "本プロジェクトのフロントエンドで使用しているUIライブラリです。",
        "url": "https://mantine.dev/",
        "score": 0.95,
        "publishedAt": "2023-10-25T12:00:00Z"
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


GITHUB_API_URL = "https://api.github.com/search/repositories"
GITHUB_TOKEN = os.getenv("GITHUB_API_TOKEN")
@app.get("/search")
async def search(
    q: str = Query(..., min_length=1, description="検索キーワード"),
    page: int = Query(1, ge=1, description="ページ番号"),
    limit: int = Query(10, ge=1, le=100, description="1ページあたりの取得件数")
):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "DockDockGo-App"
    }
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    params = {
        "q": q,
        "sort": "stars",
        "order": "desc",
        "page": page,
        "per_page": limit,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(GITHUB_API_URL, params=params, headers=headers)
            response.raise_for_status()  # 2xx以外のステータスコードで例外を発生
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"サービス利用不可: GitHub APIへの接続に失敗しました。 {exc}")
        except httpx.HTTPStatusError as exc:
            # GitHubからのエラーレスポンスをそのままクライアントに返す
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.json())

    data = response.json()

    results = [
        {
            "id": str(item["id"]),
            "title": item["full_name"],
            "description": item.get("description"), # descriptionがない場合もある
            "url": item["html_url"],
            "score": item.get("stargazers_count", 0),
            "publishedAt": item.get("pushed_at"),
        }
        for item in data.get("items", [])
    ]

    return {
        "results": results,
        "total": data.get("total_count", 0),
        "page": page,
        "limit": limit,
        "query": q,
    }

# ルートURL
@app.get("/")
def read_root():
    return {"message": "Welcome to DockDockGo Simple API"}