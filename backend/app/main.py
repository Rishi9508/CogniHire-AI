"""Main FastAPI application entrypoint."""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import create_tables
from app.ai.embeddings import EmbeddingEngine
from app.ai.ner import NERExtractor
from app.services.job_service import JobService
from app.services.candidate_service import CandidateService
from app.services.ranking_service import RankingService
from app.services.export_service import ExportService
from app.routers.jobs import router as jobs_router
from app.routers.candidates import router as candidates_router
from app.routers.rankings import router as rankings_router
from app.routers.export import router as export_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("semantihire")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for database initialization and model loading."""
    logger.info("Initializing database and tables...")
    await create_tables()

    # Ensure upload and export directories exist
    logger.info("Creating upload and export directories...")
    Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    Path(settings.EXPORT_DIR).mkdir(parents=True, exist_ok=True)

    # Initialize AI models and engines (loaded once at startup)
    logger.info("Loading SentenceTransformer model (all-MiniLM-L6-v2)...")
    embedding_engine = EmbeddingEngine(model_name=settings.MODEL_NAME)
    
    logger.info("Loading spaCy NLP model and skill patterns...")
    ner_extractor = NERExtractor()

    # Initialize and attach services to app state
    logger.info("Initializing application services...")
    app.state.embedding_engine = embedding_engine
    app.state.ner_extractor = ner_extractor
    
    app.state.job_service = JobService(
        embedding_engine=embedding_engine,
        ner_extractor=ner_extractor,
    )
    app.state.candidate_service = CandidateService(
        embedding_engine=embedding_engine,
        ner_extractor=ner_extractor,
    )
    app.state.ranking_service = RankingService(
        embedding_engine=embedding_engine,
        ner_extractor=ner_extractor,
    )
    app.state.export_service = ExportService()

    logger.info("SemantiHire AI backend is fully initialized.")
    yield
    logger.info("Shutting down SemantiHire AI backend...")


app = FastAPI(
    title="SemantiHire AI API",
    description="Semantic hiring platform backend with hybrid scoring and explainable AI.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS setup
origins = settings.cors_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(jobs_router)
app.include_router(candidates_router)
app.include_router(rankings_router)
app.include_router(export_router)


@app.get("/api/health", tags=["System"])
async def health_check():
    """Simple API health check endpoint."""
    return {"status": "healthy", "service": "SemantiHire AI API"}
