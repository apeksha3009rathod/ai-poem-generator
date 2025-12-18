from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.api.rest import router as rest_router
from app.api.graphql import router as graphql_router
from app.db.database import engine
from app.db.models import Base


# This function controls startup & shutdown of app
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)
    print("Done.")

    yield  # app runs here

    print("Shutting down app...")


app = FastAPI(
    title="AI Poem Generator",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router)
app.include_router(graphql_router)


@app.get("/")
def health():
    return {"status": "ok"}
