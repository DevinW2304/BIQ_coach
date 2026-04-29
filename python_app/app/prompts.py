def build_workout_prompt(
    position: str,
    skill_level: str,
    strengths: str,
    weaknesses: str,
    available_time: int,
    primary_goal: str,
    environment: str,
) -> str:
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
- Respect the training environment. Do not suggest drills that require equipment or space the player likely does not have.
- Keep the workout actionable and easy to follow.
- Avoid dangerous, reckless, or overly advanced instructions.
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
- Keep it basketball-relevant

COOLDOWN
- List cooldown or recovery steps

COACHING POINTS
- 4 to 6 short bullet points with technique reminders

MOTIVATIONAL SUMMARY
- A short 2 to 4 sentence closing message

Keep the response clean, organized, and easy to display in a terminal or web app.
""".strip()