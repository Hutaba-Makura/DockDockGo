# DockDockGo

React + TypeScript + Mantine のフロントエンドと FastAPI のバックエンドで構成された検索サイトのプロトタイプです。

## 技術スタック

### フロントエンド
- React 18
- TypeScript
- Mantine UI
- Vite
- Docker

### バックエンド
- Python 3.11+
- FastAPI
- Pydantic
- Docker

## プロジェクト構成

```
DockDockGo/
├─ docker-compose.yml        # frontend / backend をまとめて起動
├─ .env                      # 共通環境変数
├─ README.md
├─ frontend/                 # React + TS + Mantine
└─ backend/                  # FastAPI
```

### フロントエンド構成 (frontend/)

```
frontend/
├─ Dockerfile               # フロントエンド用Docker設定
├─ .dockerignore           # Docker除外ファイル
├─ .env                    # VITE_PUBLIC_API_BASE など
├─ index.html              # HTMLエントリポイント
├─ package.json            # 依存関係管理
├─ tsconfig.json           # TypeScript設定
├─ vite.config.ts          # Vite設定
└─ src/
   ├─ main.tsx             # エントリポイント（MantineProvider 設定）
   ├─ App.tsx              # 単一ページ構成のルート
   ├─ pages/
   │  └─ SearchPage.tsx    # 検索フォーム + 結果一覧
   ├─ components/
   │  ├─ SearchForm.tsx    # クエリ入力、submit ボタン
   │  ├─ ResultList.tsx    # 結果一覧
   │  └─ ResultItem.tsx    # 結果1件（タイトル/概要/リンクなど）
   ├─ hooks/
   │  └─ useSearch.ts      # フロント側の検索ロジック（API 呼び出し）
   ├─ services/
   │  └─ apiClient.ts      # fetch ラッパ（baseURL, エラーハンドリング）
   ├─ types/
   │  └─ search.ts         # API 入出力の型（Query, SearchResult など）
   ├─ styles/
   │  └─ theme.ts          # Mantine テーマ拡張（色/フォント等）
   └─ assets/              # 画像やアイコン
```

### バックエンド構成 (backend/)

```
backend/
├─ Dockerfile              # バックエンド用Docker設定
├─ .dockerignore          # Docker除外ファイル
├─ requirements.txt        # Python依存関係
├─ .env                   # BACKEND_CORS_ORIGINS, LOG_LEVEL など
└─ app/
   ├─ main.py             # FastAPI 起動、ルータ登録、CORS
   ├─ api/
   │  ├─ __init__.py
   │  └─ routes_search.py # /search エンドポイント
   ├─ core/
   │  ├─ config.py        # 設定読込（pydantic-settings 等）
   │  └─ logging.py       # ロガー設定
   ├─ schemas/
   │  └─ search.py        # Pydantic モデル（Request/Response）
   └─ services/
      └─ search_engine.py # 実検索の呼び出し
```

## 起動方法

1. プロジェクトのルートディレクトリで以下を実行:
```bash
docker-compose up --build
```

2. ブラウザで以下にアクセス:
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000

## 開発

### フロントエンド開発
- 検索フォームと結果表示のUI
- APIとの通信処理
- エラーハンドリング

### バックエンド開発
- 検索APIエンドポイント
- 検索エンジンとの連携
- レスポンス形式の定義