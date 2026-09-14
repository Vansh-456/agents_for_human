import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api import events, network, simulation

app = FastAPI(title="AnnaSetu API", description="Autonomous food-rescue coordination service", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["Simulation"])

from backend.api import judge_endpoints
app.include_router(judge_endpoints.router, prefix="/api", tags=["Judge Spec Endpoints"])

@app.get("/health")
def health_check():
    return {"status": "ok", "mode": __import__("os").getenv("MOCK_AWS", "true")}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {repr(exc)}"},
        headers={"Access-Control-Allow-Origin": "*"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
