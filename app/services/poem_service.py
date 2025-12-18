import os
from google import genai  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from app.db.models import Poem
from app.utils.logger import logger


# -------------------
# Gemini setup
# -------------------


API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

client = genai.Client(api_key=API_KEY)


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
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=poetic_prompt,
        )
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
