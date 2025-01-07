from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.logging import logger
from routers import document, user

app = FastAPI(
    title="GraphMind",
    description="API for automatic knowledge graph creation and management",
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document.router)
app.include_router(user.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"detail": "Internal server error occurred."}
    )


@app.get("/")
async def root():
    """Root endpoint to check if the API is running"""
    logger.info("Root endpoint accessed")
    return {"status": "ok", "message": "Knowledge Graph Agent API is running"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    logger.debug("Health check endpoint accessed")
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Knowledge Graph Agent API")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
