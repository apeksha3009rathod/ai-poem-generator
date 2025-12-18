from dotenv import load_dotenv
import os
# Purpose:
# ✔ Load secrets safely
# ✔ Needed for deployment later

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
