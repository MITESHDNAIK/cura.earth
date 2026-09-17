from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.api.v1.router import api_router
from app.rag.ingestion import ingestion_pipeline


app = FastAPI(
    title="Cura.Earth",
    description="AI Environmental Scientist and Ecological Reasoning Engine",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# API ROUTES
# ---------------------------------------------------------

app.include_router(
    api_router,
    prefix="/api/v1",
)


# ---------------------------------------------------------
# STARTUP
# ---------------------------------------------------------

@app.on_event("startup")
async def startup_event():
    """
    Automatically ingest environmental knowledge documents
    when the backend starts.
    """

    try:
        documents_dir = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "documents"
        )

        if not documents_dir.exists():
            print(
                f"Knowledge directory not found: {documents_dir}"
            )
            return

        count = ingestion_pipeline.ingest_directory(
            documents_dir
        )

        print(
            f"Cura.Earth Knowledge Base initialized: "
            f"{count} chunks indexed."
        )

    except Exception as exc:
        print(
            f"Warning: Could not auto-ingest documents: {exc}"
        )


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
async def root():
    return {
        "name": "Cura.Earth",
        "status": "online",
        "message": "AI Environmental Scientist is running.",
    }


# ---------------------------------------------------------
# HEALTH
# ---------------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "cura.earth",
    }