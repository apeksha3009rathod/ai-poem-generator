import strawberry
from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter
from app.services.poem_service import generate_poem

# /graphql

@strawberry.type
class Query:
    @strawberry.field
    def generate_poem(self, input_text: str, style: str = "free verse") -> str:
        return generate_poem(input_text, style)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")


import strawberry
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends
from strawberry.fastapi import GraphQLRouter
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.db.models import Poem
from app.services.poem_service import generate_poem


@strawberry.type
class PoemType:
    id: int
    input_text: str
    style: str
    poem: str
    created_at: datetime


@strawberry.type
class Query:

    @strawberry.field
    def poems(
        self,
        info,
        limit: int = 10,
        offset: int = 0
    ) -> List[PoemType]:
        db: Session = info.context["db"]

        poems = (
            db.query(Poem)
            .order_by(Poem.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return poems


@strawberry.type
class Mutation:

    @strawberry.mutation
    def generate_poem(
        self,
        info,
        input_text: str,
        style: str = "free verse"
    ) -> PoemType:
        db: Session = info.context["db"]

        poem_text = generate_poem(
            input_text=input_text,
            style=style,
            db=db
        )

        poem = (
            db.query(Poem)
            .order_by(Poem.created_at.desc())
            .first()
        )

        return poem


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)


def get_context(db: Session = Depends(get_db)):
    return {"db": db}


graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

router = APIRouter()
router.include_router(graphql_app, prefix="/graphql")
