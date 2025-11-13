"""
FastAPI application for crypto trading system.

This is the main application file that sets up the FastAPI app and includes routers.
"""

from fastapi import FastAPI

from api.routers import orders

app = FastAPI(
    title="Crypto Trading System API",
    description="API for placing risk-managed market orders with automatic stop loss",
    version="1.0.0",
)

# Include routers
app.include_router(orders.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Crypto Trading System API"
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
