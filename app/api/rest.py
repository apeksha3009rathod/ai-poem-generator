from fastapi import APIRouter, Depends
from app.schemas.poem import PoemRequest, PoemResponse
from app.services.poem_service import generate_poem

from app.schemas.poem import PoemListResponse
from app.services.poem_service import list_poems

from app.db.deps import get_db

from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/v1", tags=["Poem"])

# POST /api/v1/poem

@router.post("/poem", response_model=PoemResponse)
def create_poem(request: PoemRequest):
    poem = generate_poem(
        input_text=request.input_text,
        style=request.style
    )
    return {"poem": poem}


@router.get("/poems", response_model=PoemListResponse)
def get_poems(
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    total, poems = list_poems(db, limit=limit, offset=offset)
    return {
        "total": total,
        "items": poems
    }
