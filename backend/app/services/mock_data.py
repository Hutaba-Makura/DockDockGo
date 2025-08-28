import json
import os
from typing import List, Dict, Any, Optional
from ..schemas.search import SearchResult, MockResponse

def load_mock_results() -> List[Dict[str, Any]]:
    """
    JSONファイルからモックデータを読み込む
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, 'mock_results.json')
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file_path} not found. Returning empty list.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: JSON file parsing error: {e}")
        return []

def get_mock_data(query: Optional[str] = None) -> MockResponse:
    """
    検索クエリに基づいてモックデータを返す
    """
    print(f"検索クエリ '{query}' を受信しました。")

    # JSONファイルからモックデータを読み込み
    mock_results = load_mock_results()

    # フロントエンドが必要とするレスポンス形式に合わせてデータを整形
    return MockResponse(
        results=[SearchResult(**result) for result in mock_results],
        total=len(mock_results),
        page=1,
        limit=10,
        query=query if query else ""
    )
