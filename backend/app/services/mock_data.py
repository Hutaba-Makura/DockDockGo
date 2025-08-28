from typing import List, Dict, Any, Optional
from ..schemas.search import SearchResult, MockResponse

# モックの検索結果データ
MOCK_RESULTS: List[Dict[str, Any]] = [
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

def get_mock_data(query: Optional[str] = None) -> MockResponse:
    """
    検索クエリに基づいてモックデータを返す
    """
    print(f"検索クエリ '{query}' を受信しました。")

    # フロントエンドが必要とするレスポンス形式に合わせてデータを整形
    return MockResponse(
        results=[SearchResult(**result) for result in MOCK_RESULTS],
        total=len(MOCK_RESULTS),
        page=1,
        limit=10,
        query=query if query else ""
    )
