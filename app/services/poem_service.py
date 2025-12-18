import google.generativeai as genai
from app.config import GEMINI_API_KEY
from app.utils.logger import logger
from sqlalchemy.orm import Session
from app.db.models import Poem

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash-lite")


def generate_poem(input_text: str, style: str, db: Session) -> str:
    logger.info("Generating poem")

    prompt = f"Write a {style} poem about: {input_text}"
    response = model.generate_content(prompt)

    poem_text = response.text

    poem = Poem(
        input_text=input_text,
        style=style,
        poem=poem_text
    )

    db.add(poem)
    db.commit()
    db.refresh(poem)

    return poem_text


def list_poems(db: Session, limit: int = 10, offset: int = 0):
    total = db.query(Poem).count()

    poems = (
        db.query(Poem)
        .order_by(Poem.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, poems
