import os
import google.generativeai as genai  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.db.models import Poem
from app.utils.logger import logger


# -------------------
# Gemini setup
# -------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash-lite")


# -------------------
# Services
# -------------------

def generate_poem(input_text: str, db: Session) -> str:
    poetic_prompt = f"""
    You are a wise and thoughtful poet, a lyrical companion who sees beauty
     in every moment.
    Transform the following message into a beautiful, expressive poetic verse.

    Guidelines:
    - Respond with 2-4 lines of poetry
    - Use vivid imagery and metaphors
    - Create rhythm and flow in your verses
    - Make it personal and profound
    - Capture the emotion and essence of the message
    - Use poetic language but keep it accessible

    User's message: "{input_text}"

    Your poetic response:
    """

    try:
        response = model.generate_content(poetic_prompt)
        poem_text = response.text
    except Exception as exc:
        logger.exception("Gemini failed")
        raise RuntimeError("Poem generation failed") from exc

    poem = Poem(
        input_text=input_text,
        poem=poem_text,
    )

    db.add(poem)
    db.commit()
    db.refresh(poem)

    return poem_text


def list_poems(
    db: Session,
    limit: int = 10,
    offset: int = 0,
):
    total = db.query(Poem).count()

    poems = (
        db.query(Poem)
        .order_by(Poem.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return total, poems
