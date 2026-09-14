import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api import events, network, simulation

app = FastAPI(title="AnnaSetu API", description="Autonomous food-rescue coordination service", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin for origin in __import__("os").getenv("CORS_ORIGINS", "http://localhost:5173").split(",")],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router, prefix="/api/events", tags=["Events"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(simulation.router, prefix="/api/simulation", tags=["Simulation"])

@app.get("/health")
def health_check():
    return {"status": "ok", "mode": __import__("os").getenv("MOCK_AWS", "true")}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
