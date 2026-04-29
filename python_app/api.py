from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from app.workout_generator import generate_workout_plan

app = FastAPI(title="HoopCoach AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://biq-coach.vercel.app",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Absolute path so Vercel can find the file regardless of working directory
FRONTEND_DIR = Path(__file__).parent / "frontend"


class WorkoutRequest(BaseModel):
    position: str = Field(..., min_length=2, max_length=40)
    skill_level: str = Field(..., min_length=2, max_length=40)
    strengths: str = Field(..., min_length=2, max_length=300)
    weaknesses: str = Field(..., min_length=2, max_length=300)
    available_time: int = Field(..., ge=10, le=180)
    primary_goal: str = Field(..., min_length=2, max_length=120)
    environment: Optional[str] = "court"


class WorkoutResponse(BaseModel):
    workout: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate-workout", response_model=WorkoutResponse)
def generate_workout(payload: WorkoutRequest) -> WorkoutResponse:
    try:
        workout = generate_workout_plan(
            position=payload.position,
            skill_level=payload.skill_level,
            strengths=payload.strengths,
            weaknesses=payload.weaknesses,
            available_time=payload.available_time,
            primary_goal=payload.primary_goal,
            environment=payload.environment or "court",
        )
        return WorkoutResponse(workout=workout)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/")
@app.get("/app")
def serve_frontend() -> HTMLResponse:
    html_file = FRONTEND_DIR / "index.html"
    return HTMLResponse(content=html_file.read_text(encoding="utf-8"))