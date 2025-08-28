from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["health"])

class HealthResponse(BaseModel):
    message: str
    status: str = "healthy"

@router.get("/", response_model=HealthResponse)
def read_root():
    """
    ルートURL - アプリケーションのヘルスチェック
    """
    return HealthResponse(message="Welcome to DockDockGo Simple API")
