# HoopCoach AI

HoopCoach AI is a polished starter project for a Generative AI class assignment. It uses the Mistral API to generate practical basketball workouts based on a player's position, skill level, strengths, weaknesses, available time, training goal, and workout environment.

The project is intentionally small enough for a student submission, but structured cleanly so it feels like a real app and can be extended later.

## Features

- Python terminal app with a standard input/output loop
- Personalized basketball workout generation with the Mistral API
- Structured output with warm-up, drills, conditioning, cooldown, coaching points, and motivation
- Save generated workouts to text files
- `.env` support for API secrets
- Modular beginner-friendly codebase
- Matching basketball-inspired branding and theme assets

## Project Structure

```text
python_app/
├── main.py
├── .env.example
├── requirements.txt
├── README.md
├── abstract_draft.md
├── example_inputs.md
├── assets/
│   ├── hoopcoach_theme.css
│   └── landing_mockup.html
├── saved_workouts/
└── app/
    ├── __init__.py
    ├── config.py
    ├── prompts.py
    ├── mistral_client.py
    ├── workout_generator.py
    └── ui.py
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`.
4. Add your Mistral API key to `.env`:

```env
MISTRAL_API_KEY=your_real_key_here
MISTRAL_MODEL=mistral-small-latest
```

## Run

```bash
python main.py
```

## Notes on the Mistral SDK

This project uses Mistral's official Python SDK with the `mistralai` package and the `client.chat.complete(...)` pattern described in the official docs. citeturn995590view0

## Suggested Demo Flow

1. Launch the app.
2. Generate a workout for a guard, wing, or big.
3. Show how the app adapts to different skill levels and environments.
4. Save the generated workout to a text file.
5. Include the abstract draft in your submission package.

## Extension Ideas

- Export workouts as markdown or PDF
- Add a GUI with Tkinter or a web front end
- Add workout history and comparison
- Add recovery-day or game-day plan options
- Let users choose training intensity

## Theme and Style

The included CSS and mockup follow a dark, premium basketball feel with gold accents, bold display typography, and sports-dashboard energy so the project visually matches a modern basketball analytics or training brand.
