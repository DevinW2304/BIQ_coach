from datetime import datetime
from pathlib import Path

from app.workout_generator import generate_workout_plan


def _prompt_non_empty(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Please enter a value.")


def _prompt_time() -> int:
    while True:
        raw = input("Available workout time (minutes): ").strip()
        try:
            minutes = int(raw)
            if 10 <= minutes <= 180:
                return minutes
            print("Enter a number between 10 and 180.")
        except ValueError:
            print("Please enter a valid whole number.")


def _prompt_environment() -> str:
    valid = {"home", "gym", "court"}
    while True:
        value = input("Environment (home / gym / court) [default: court]: ").strip().lower()
        if not value:
            return "court"
        if value in valid:
            return value
        print("Choose home, gym, or court.")


def save_workout_to_file(workout: str) -> Path:
    folder = Path("saved_workouts")
    folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = folder / f"workout_{timestamp}.txt"
    filepath.write_text(workout, encoding="utf-8")
    return filepath


def generate_workout_interactive() -> str:
    print("\nEnter player details:\n")
    position = _prompt_non_empty("Position")
    skill_level = _prompt_non_empty("Skill level")
    strengths = _prompt_non_empty("Strengths")
    weaknesses = _prompt_non_empty("Weaknesses")
    available_time = _prompt_time()
    primary_goal = _prompt_non_empty("Primary training goal")
    environment = _prompt_environment()

    print("\nGenerating workout...\n")

    workout = generate_workout_plan(
        position=position,
        skill_level=skill_level,
        strengths=strengths,
        weaknesses=weaknesses,
        available_time=available_time,
        primary_goal=primary_goal,
        environment=environment,
    )
    return workout


def run_cli() -> None:
    current_workout = ""

    while True:
        print("\n" + "=" * 56)
        print("HOOPCOACH".center(56))
        print("=" * 56)
        print("1. Generate new workout")
        print("2. Save last workout to text file")
        print("3. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            try:
                current_workout = generate_workout_interactive()
                print("\n" + "=" * 56)
                print(current_workout)
                print("=" * 56)
            except Exception as exc:
                print(f"\nError: {exc}")

        elif choice == "2":
            if not current_workout:
                print("\nNo workout has been generated yet.")
                continue
            filepath = save_workout_to_file(current_workout)
            print(f"\nWorkout saved to: {filepath}")

        elif choice == "3":
            print("\nGood luck with your training.")
            break

        else:
            print("\nInvalid option. Choose 1, 2, or 3.")