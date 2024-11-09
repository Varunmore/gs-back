from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import games

app = FastAPI()

# Configure CORS (Adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include game-related routes
app.include_router(games.router, prefix="/api", tags=["games"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the GameShow API!"}
