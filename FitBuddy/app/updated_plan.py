from .ai_client import generate_text

UPDATE_INSTRUCTION = """
You revise fitness plans responsibly.
Preserve useful parts of the original plan unless the user's feedback asks
for a change. Never recommend exercising through sharp/severe pain or unsafe
extremes. Return a complete seven-day plan, not just a list of changes.
"""


def update_workout_plan(original_plan: str, feedback: str, goal: str, intensity: str) -> str:
    prompt = f"""
Original seven-day FitBuddy plan:
--- START ORIGINAL ---
{original_plan}
--- END ORIGINAL ---

User feedback:
--- START FEEDBACK ---
{feedback}
--- END FEEDBACK ---

Goal: {goal}
Preferred intensity: {intensity}

Create a revised complete seven-day plan that meaningfully incorporates the
feedback. Keep warm-up, main workout, rest guidance, and cooldown/recovery
for each day. If feedback is unsafe or contradictory, adapt it into a safer
alternative rather than following it literally.
"""
    return generate_text(prompt, system_instruction=UPDATE_INSTRUCTION, model_role="workout")
