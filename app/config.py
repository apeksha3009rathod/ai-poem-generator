from dotenv import load_dotenv  # type: ignore
import os


# Load secrets safely
# for local development

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
