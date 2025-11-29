"""FastAPI application for YouTube Trends Analysis"""

import time
from typing import List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from .models import (
    QueryRequest,
    QueryResponse,
    SystemInfoResponse,
    HealthResponse,
    ExampleQuery
)
from ..main import YouTubeTrendsApp
from ..config.settings import get_settings


# Global app instance
app_instance = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    global app_instance
    
    logger.info("Starting YouTube Trends API...")
    try:
        app_instance = YouTubeTrendsApp()
        logger.info("Application initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    
    yield
    
    logger.info("Shutting down YouTube Trends API...")


# Create FastAPI app
app = FastAPI(
    title="YouTube Trends Analysis API",
    description="Multi-Agent AI system for analyzing YouTube trending videos",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "YouTube Trends Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        info = app_instance.get_system_info()
        agents = list(info.get('agents', {}).keys())
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            agents_available=agents,
            database_connected=True
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            agents_available=[],
            database_connected=False
        )


@app.post("/query", response_model=QueryResponse, tags=["Query"])
async def process_query(request: QueryRequest):
    """
    Process a natural language query about YouTube trends.
    
    The system will automatically route your query to the appropriate agent(s):
    - SQL Agent: For analytical queries (stats, counts, aggregations)
    - Vector Agent: For semantic search (content similarity)
    - Hybrid: For queries requiring both capabilities
    """
    if not app_instance:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not initialized"
        )
    
    try:
        start_time = time.time()
        
        logger.info(f"Processing query: {request.query}")
        response = app_instance.query(request.query)
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            query=request.query,
            answer=response.get('answer', 'No answer generated'),
            success=response.get('success', True),
            metadata=response.get('metadata'),
            results=response.get('results'),
            error=response.get('error'),
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query processing failed: {str(e)}"
        )


@app.get("/system/info", response_model=SystemInfoResponse, tags=["System"])
async def get_system_info():
    """Get information about the system and available agents"""
    if not app_instance:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not initialized"
        )
    
    try:
        info = app_instance.get_system_info()
        
        return SystemInfoResponse(
            orchestrator=info.get('orchestrator', 'Unknown'),
            agents=info.get('agents', {}),
            configuration={
                'llm_model': settings.llm_model,
                'sql_database': settings.sql_db_path,
                'vector_db': f"Qdrant ({settings.qdrant_host}:{settings.qdrant_port})",
                'embedding_model': settings.local_embedding_model
            }
        )
    
    except Exception as e:
        logger.error(f"Failed to get system info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system info: {str(e)}"
        )


@app.get("/examples", response_model=List[ExampleQuery], tags=["Examples"])
async def get_example_queries():
    """Get example queries to help users understand the system capabilities"""
    return [
        ExampleQuery(
            category="SQL/Analytical",
            query="Which category has the most trending videos?",
            description="Get statistics about video categories"
        ),
        ExampleQuery(
            category="SQL/Analytical",
            query="Top 10 channels by total views",
            description="Aggregate data across channels"
        ),
        ExampleQuery(
            category="SQL/Analytical",
            query="Average likes for Gaming category",
            description="Calculate metrics for specific categories"
        ),
        ExampleQuery(
            category="Vector/Semantic",
            query="Find videos about cooking tutorials",
            description="Semantic search based on content"
        ),
        ExampleQuery(
            category="Vector/Semantic",
            query="Videos similar to tech reviews",
            description="Find similar content using embeddings"
        ),
        ExampleQuery(
            category="Vector/Semantic",
            query="Content related to fitness and wellness",
            description="Discover videos by topic"
        ),
        ExampleQuery(
            category="Hybrid",
            query="Most popular gaming videos about Minecraft",
            description="Combine semantic search with analytics"
        ),
        ExampleQuery(
            category="Hybrid",
            query="Top educational content about programming",
            description="Filter by category and search by content"
        ),
        ExampleQuery(
            category="Hybrid",
            query="Find trending cooking videos with high engagement",
            description="Semantic search with performance metrics"
        )
    ]


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
