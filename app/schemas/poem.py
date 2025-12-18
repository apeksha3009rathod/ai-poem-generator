from pydantic import BaseModel
from datetime import datetime
from typing import List


class PoemRequest(BaseModel):
    input_text: str


class PoemResponse(BaseModel):
    poem: str


class PoemItem(BaseModel):
    id: int
    input_text: str
    poem: str
    created_at: datetime

    class Config:
        from_attributes = True


class PoemListResponse(BaseModel):
    total: int
    items: List[PoemItem]
