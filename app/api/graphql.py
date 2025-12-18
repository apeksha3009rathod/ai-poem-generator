import strawberry  # type: ignore
from strawberry.fastapi import GraphQLRouter  # type: ignore

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session  # type: ignore
from fastapi import Depends, APIRouter

from app.db.deps import get_db
from app.db.models import Poem
from app.services.poem_service import generate_poem


# -------------------
# GraphQL Types
# -------------------

@strawberry.type
class PoemType:
    id: int
    input_text: str
    poem: str
    created_at: datetime


# -------------------
# Queries (READ)
# -------------------

@strawberry.type
class Query:

    @strawberry.field
    def poems(
        self,
        info,
        limit: int = 10,
        offset: int = 0,
    ) -> List[PoemType]:
        db: Session = info.context["db"]

        return (
            db.query(Poem)
            .order_by(Poem.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )


# -------------------
# Mutations (WRITE)
# -------------------

@strawberry.type
class Mutation:

    @strawberry.mutation
    def generate_poem(
        self,
        info,
        input_text: str,
    ) -> PoemType:
        db: Session = info.context["db"]

        generate_poem(
            input_text=input_text,
            db=db,
        )

        poem = (
            db.query(Poem)
            .order_by(Poem.created_at.desc())
            .first()
        )

        return poem


# -------------------
# Schema
# -------------------

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
)


# -------------------
# Context (DB injection)
# -------------------

def get_context(db: Session = Depends(get_db)):
    return {"db": db}


# -------------------
# Router
# -------------------

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context,
)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")
