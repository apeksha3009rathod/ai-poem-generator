from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app.schemas.poem import PoemRequest, PoemResponse, PoemListResponse
from app.services.poem_service import generate_poem, list_poems
from app.db.deps import get_db

router = APIRouter(prefix="/api/v1", tags=["Poem"])


# POST /api/v1/poem
@router.post("/poem", response_model=PoemResponse)
def create_poem(
    request: PoemRequest,
    db: Session = Depends(get_db),   # DB injected here
):
    poem = generate_poem(
        input_text=request.input_text,
        db=db,                       # DB passed explicitly
    )
    return {"poem": poem}


# GET /api/v1/poems
@router.get("/poems", response_model=PoemListResponse)
def get_poems(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    total, poems = list_poems(db, limit=limit, offset=offset)
    return {
        "total": total,
        "items": poems,
    }
