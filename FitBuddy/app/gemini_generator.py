from .ai_client import generate_text
from .schemas import UserInput

SYSTEM_INSTRUCTION = """
You are FitBuddy, a responsible fitness-planning assistant.
Create practical, beginner-friendly-to-intermediate workout plans.
Do not diagnose medical conditions, prescribe medication, recommend dangerous
extreme dieting, or encourage exercising through significant pain.
Use conservative progression, include warm-up and cooldown/recovery guidance,
and mention that people with relevant medical conditions, injuries, pregnancy,
or significant symptoms should consult a qualified healthcare professional.
Return plain text with exactly seven clearly labeled days.
"""


def generate_workout_gemini(user: UserInput) -> str:
    prompt = f"""
Create a personalized 7-day workout plan for:
Name: {user.name}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Preferred intensity: {user.intensity}

For each day include:
- Day and focus
- Warm-up (5–10 minutes)
- Main workout with exercise names and sets/reps or duration
- Rest guidance
- Cooldown/recovery

Balance training and recovery across the week. Do not assume access to a gym.
Keep the plan actionable and avoid unsupported medical claims.
"""
    return generate_text(prompt, system_instruction=SYSTEM_INSTRUCTION, model_role="workout")
