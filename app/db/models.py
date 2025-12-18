from sqlalchemy import Column, Integer, Text, DateTime  # type: ignore
from sqlalchemy.sql import func   # type: ignore
from app.db.database import Base


class Poem(Base):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    poem = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
