from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.rest import router as rest_router
from app.api.graphql import router as graphql_router
from app.db.database import engine
from app.db.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔹 Startup logic
    print("Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

    yield  # ⬅️ app runs here

    # 🔹 Shutdown logic (optional)
    print("Shutting down app...")


app = FastAPI(
    title="AI Poem Generator",
    lifespan=lifespan
)

app.include_router(rest_router)
app.include_router(graphql_router)


@app.get("/")
def health():
    return {"status": "ok"}
