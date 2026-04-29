import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from mistralai import Mistral
from pydantic import BaseModel, Field

load_dotenv()

# ── Config ────────────────────────────────────────────────────────
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()
MISTRAL_MODEL   = os.getenv("MISTRAL_MODEL", "mistral-small-latest").strip()

SYSTEM_PROMPT = (
    "You are an experienced basketball skills trainer and player development coach. "
    "You create safe, structured, basketball-specific workouts based on a player's role, "
    "skill level, strengths, weaknesses, available time, and training environment. "
    "Your workouts should feel realistic, practical, and useful for actual improvement."
)

FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"

# ── Prompt builder ────────────────────────────────────────────────
def build_prompt(position, skill_level, strengths, weaknesses, available_time, primary_goal, environment):
    return f"""
Create a practical basketball workout plan for one player.

Player profile:
- Position: {position}
- Skill level: {skill_level}
- Strengths: {strengths}
- Weaknesses: {weaknesses}
- Available time: {available_time} minutes
- Primary training goal: {primary_goal}
- Training environment: {environment}

Instructions:
- Make the workout basketball-specific, realistic, and safe.
- Fit the full plan into approximately {available_time} minutes.
- Tailor the drills to the player's position, skill level, strengths, weaknesses, and goal.
- Respect the training environment.
- Keep the workout actionable and easy to follow.
- Use a confident but supportive coaching tone.

Return the workout in this exact section structure:

WORKOUT TITLE
A short title for the session

TOTAL TIME
Estimated total time in minutes

WARM-UP
- List drills with time or reps

SKILL DRILLS
- List drills with time or reps
- Explain what each drill improves

CONDITIONING
- List conditioning work with time or reps

COOLDOWN
- List cooldown or recovery steps

COACHING POINTS
- 4 to 6 short bullet points with technique reminders

MOTIVATIONAL SUMMARY
- A short 2 to 4 sentence closing message
""".strip()


# ── Mistral call ──────────────────────────────────────────────────
def generate_text(prompt: str) -> str:
    if not MISTRAL_API_KEY:
        raise ValueError("Missing MISTRAL_API_KEY environment variable.")
    client = Mistral(api_key=MISTRAL_API_KEY)
    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("Mistral returned an empty response.")
    return content.strip()


# ── FastAPI app ───────────────────────────────────────────────────
app = FastAPI(title="HoopCoach AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkoutRequest(BaseModel):
    position:       str = Field(..., min_length=2, max_length=40)
    skill_level:    str = Field(..., min_length=2, max_length=40)
    strengths:      str = Field(..., min_length=2, max_length=300)
    weaknesses:     str = Field(..., min_length=2, max_length=300)
    available_time: int = Field(..., ge=10, le=180)
    primary_goal:   str = Field(..., min_length=2, max_length=120)
    environment:    Optional[str] = "court"


class WorkoutResponse(BaseModel):
    workout: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-workout", response_model=WorkoutResponse)
def generate_workout(payload: WorkoutRequest):
    try:
        prompt  = build_prompt(
            payload.position, payload.skill_level, payload.strengths,
            payload.weaknesses, payload.available_time, payload.primary_goal,
            payload.environment or "court",
        )
        workout = generate_text(prompt)
        return WorkoutResponse(workout=workout)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/")
@app.get("/app")
def serve_frontend():
    return HTMLResponse(content=FRONTEND.read_text(encoding="utf-8"))