import json
import os
from typing import List, Dict, Any, Optional
from ..schemas.search import SearchResult, MockResponse

def load_mock_data(file_name: str) -> List[Dict[str, Any]]:
    """
    JSONファイルからモックデータを読み込む
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, file_name)
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found. Returning empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: JSON file parsing error: {e}")
        return []

PYTHON_MOCK_RESULTS: List[Dict[str, Any]] = [
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
        "create": "toma1128/ai4",
        "description": "DjangoやRailsアプリケーションとRedisをキャッシュとして連携させる構成です。"
    }
]

REACT_MOCK_RESULTS: List[Dict[str, Any]] = [
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
    }
]

def get_mock_data(query: Optional[str] = None) -> MockResponse:
    print(f"検索クエリ '{query}' を受信しました。")

    if not query:
        mock_results = load_mock_data('mock_results.json')
        return MockResponse(
            results=[SearchResult(**result) for result in mock_results],
            total=len(mock_results),
            page=1,
            limit=10,
            query=""
        )

    q_lower = query.lower()
    results: List[Dict[str, Any]] = []

    # AND検索のように、複数のキーワードが含まれているかをチェック
    if 'fastapi' in q_lower and 'react' in q_lower:
        results = load_mock_data('react_mock_results.json')
    elif "python" in q_lower:
        results = load_mock_data('python_mock_results.json')
    else:
        # 一致するキーワードがない場合はデフォルトのデータを返す
        results = load_mock_data('mock_results.json')

    return MockResponse(
        results=[SearchResult(**result) for result in results],
        total=len(results),
        page=1,
        limit=10,
        query=query
    )