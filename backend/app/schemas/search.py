from pydantic import BaseModel
from typing import List, Optional

class SearchResult(BaseModel):
    dockercompose: str
    create: str
    description: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    page: int
    limit: int
    query: str

class MockResponse(BaseModel):
    results: List[SearchResult]
    total: int
    page: int
    limit: int
    query: str
