from .ai_client import generate_text

NUTRITION_INSTRUCTION = """
You are FitBuddy's nutrition and recovery assistant.
Give concise, general wellness guidance that complements exercise.
Do not prescribe a medical diet, diagnose conditions, or provide dangerous
calorie restrictions. Keep the advice practical and culturally flexible.
"""


def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"""
Give one concise nutrition or recovery tip for someone whose fitness goal is:
{goal}

The answer should be 2–4 sentences, actionable, and focused on sustainable
habits such as hydration, balanced meals, protein-rich foods, sleep, or recovery.
"""
    return generate_text(prompt, system_instruction=NUTRITION_INSTRUCTION, model_role="nutrition")
