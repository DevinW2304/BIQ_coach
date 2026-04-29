from mistralai.client import Mistral

from app.config import settings


SYSTEM_PROMPT = (
    "You are an experienced basketball skills trainer and player development coach. "
    "You create safe, structured, basketball-specific workouts based on a player's role, "
    "skill level, strengths, weaknesses, available time, and training environment. "
    "Your workouts should feel realistic, practical, and useful for actual improvement."
)


def generate_text(prompt: str) -> str:
    if not settings.mistral_api_key:
        raise ValueError(
            "Missing MISTRAL_API_KEY. Add it to  .env"
        )

    with Mistral(api_key=settings.mistral_api_key) as client:
        response = client.chat.complete(
            model=settings.mistral_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

    content = response.choices[0].message.content
    if not content:
        raise ValueError("Mistral returned an empty response.")

    return content.strip()