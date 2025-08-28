# DockDockGo Backend

Docker Composeファイルを検索するFastAPIベースのバックエンドAPI

## 📁 プロジェクト構造

```
backend/
├── app/
│   ├── main.py                    # アプリケーションのエントリーポイント
│   ├── api/                       # API関連
│   │   ├── __init__.py
│   │   └── routes/               # APIルート定義
│   │       ├── __init__.py
│   │       ├── health.py         # ヘルスチェックエンドポイント
│   │       └── search.py         # 検索関連エンドポイント
│   ├── core/                     # コア設定
│   │   ├── __init__.py
│   │   ├── config.py            # アプリケーション設定
│   │   └── middleware.py        # ミドルウェア設定
│   ├── schemas/                  # データモデル
│   │   ├── __init__.py
│   │   └── search.py            # 検索関連のPydanticスキーマ
│   └── services/                # ビジネスロジック
│       ├── __init__.py
│       ├── github_service.py    # GitHub API通信
│       └── mock_data.py         # モックデータ管理
├── Dockerfile                   # 本番用Dockerfile
├── Dockerfile.dev              # 開発用Dockerfile
├── Dockerfile.prod             # 本番用Dockerfile
├── requirements.txt            # Python依存関係
└── README.md                   # このファイル
```

## 🏗️ アーキテクチャ

### 1. **main.py** - アプリケーションエントリーポイント
- FastAPIアプリケーションの作成と設定
- ミドルウェアの設定
- ルーターの登録

### 2. **api/routes/** - APIルート層
- **health.py**: ヘルスチェックエンドポイント (`/`)
- **search.py**: 検索関連エンドポイント
  - `/api/mock`: モックデータ取得
  - `/api/search`: GitHub API検索

### 3. **core/** - 設定とミドルウェア
- **config.py**: アプリケーション設定
  - CORS設定
  - GitHub API設定
  - 環境変数管理
- **middleware.py**: ミドルウェア設定
  - CORS設定

### 4. **schemas/** - データモデル層
- **search.py**: Pydanticスキーマ定義
  - `SearchResult`: 検索結果モデル
  - `SearchResponse`: 検索レスポンスモデル
  - `MockResponse`: モックレスポンスモデル

### 5. **services/** - ビジネスロジック層
- **github_service.py**: GitHub API通信
  - リポジトリ検索
  - Docker Composeファイル取得
- **mock_data.py**: モックデータ管理
  - 開発・テスト用のサンプルデータ

## 🚀 起動方法

### 開発環境
```bash
# 依存関係のインストール
pip install -r requirements.txt

# 開発サーバーの起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker環境
```bash
# 開発用
docker-compose -f docker-compose.dev.yml up

# 本番用
docker-compose up
```

## 📡 API エンドポイント

### ヘルスチェック
- `GET /`: アプリケーションの状態確認

### 検索API
- `GET /api/mock?q={query}`: モックデータ取得
- `GET /api/search?q={query}&page={page}&limit={limit}`: GitHub API検索

## 🔧 設定

### 環境変数
- `GITHUB_API_TOKEN`: GitHub APIトークン（オプション）

### CORS設定
- デフォルト: `http://localhost:3000`
- `core/config.py`で設定可能

## 🧪 テスト

```bash
# テストの実行
pytest

# カバレッジ付きテスト
pytest --cov=app
```

## 📝 開発ガイドライン

### 新しい機能の追加
1. **APIルート**: `api/routes/`に新しいファイルを作成
2. **サービス**: `services/`にビジネスロジックを追加
3. **スキーマ**: `schemas/`にデータモデルを定義
4. **設定**: `core/config.py`に設定を追加

### コード規約
- 型ヒントを使用
- docstringを記述
- Pydanticスキーマでデータ検証
- エラーハンドリングを適切に実装

## 🔍 デバッグ

### ログ確認
```bash
# アプリケーションログ
docker-compose logs backend

# リアルタイムログ
docker-compose logs -f backend
```

### API ドキュメント
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
