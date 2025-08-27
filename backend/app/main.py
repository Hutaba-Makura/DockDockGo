from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional

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
def search(q: Optional[str] = None):
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

# ルートURL
@app.get("/")
def read_root():
    return {"message": "Welcome to DockDockGo Simple API"}