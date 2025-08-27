"""
検索関連のPydanticモデル
APIのリクエスト/レスポンスの型定義
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class SearchRequest(BaseModel):
    """検索リクエストのモデル"""
    query: str = Field(..., description="検索クエリ", min_length=1, max_length=500)
    page: int = Field(1, description="ページ番号", ge=1)
    limit: int = Field(10, description="1ページあたりの結果数", ge=1, le=100)


class SearchResult(BaseModel):
    """検索結果1件のモデル"""
    id: str = Field(..., description="結果の一意識別子")
    title: str = Field(..., description="タイトル", max_length=200)
    description: str = Field(..., description="説明文", max_length=1000)
    url: str = Field(..., description="URL")
    score: float = Field(..., description="関連度スコア", ge=0.0, le=1.0)
    published_at: Optional[datetime] = Field(None, description="公開日時")


class SearchResponse(BaseModel):
    """検索レスポンスのモデル"""
    results: List[SearchResult] = Field(..., description="検索結果一覧")
    total: int = Field(..., description="総結果数", ge=0)
    page: int = Field(..., description="現在のページ番号", ge=1)
    limit: int = Field(..., description="1ページあたりの結果数", ge=1)
    query: str = Field(..., description="検索クエリ")


class ErrorResponse(BaseModel):
    """エラーレスポンスのモデル"""
    error: str = Field(..., description="エラー種別")
    message: str = Field(..., description="エラーメッセージ")
    status: int = Field(..., description="HTTPステータスコード")
