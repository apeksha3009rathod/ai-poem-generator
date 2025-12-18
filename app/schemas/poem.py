from pydantic import BaseModel

from datetime import datetime


class PoemRequest(BaseModel):
    input_text: str
    style: str | None = "free verse"


class PoemResponse(BaseModel):
    poem: str


class PoemItem(BaseModel):
    id: int
    input_text: str
    style: str
    poem: str
    created_at: datetime

    class Config:
        from_attributes = True


class PoemListResponse(BaseModel):
    total: int
    items: list[PoemItem]
