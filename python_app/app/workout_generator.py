from app.mistral_client import generate_text
from app.prompts import build_workout_prompt


def generate_workout_plan(
    position: str,
    skill_level: str,
    strengths: str,
    weaknesses: str,
    available_time: int,
    primary_goal: str,
    environment: str = "court",
) -> str:
    prompt = build_workout_prompt(
        position=position,
        skill_level=skill_level,
        strengths=strengths,
        weaknesses=weaknesses,
        available_time=available_time,
        primary_goal=primary_goal,
        environment=environment,
    )
    return generate_text(prompt)