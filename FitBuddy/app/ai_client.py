from functools import lru_cache

from .config import get_settings


def _mock_workout(prompt: str) -> str:
    return """DAY 1 — Full Body Foundation
Warm-up: 7 minutes brisk walking and mobility.
Main workout: Bodyweight squats 3×10, incline push-ups 3×8, glute bridges 3×12, bird-dogs 3×8/side.
Rest: 60–90 seconds between sets.
Cooldown: 5 minutes easy walking and gentle stretching.

DAY 2 — Cardio + Core
Warm-up: 5 minutes easy movement.
Main workout: Brisk walk 25 minutes; dead bugs 3×8/side; plank 3×20–30 seconds.
Rest: Keep the cardio conversational and recover as needed.
Cooldown: 5 minutes easy walking.

DAY 3 — Lower Body
Warm-up: 8 minutes of mobility and easy squats.
Main workout: Reverse lunges 3×8/side, hip hinges 3×10, calf raises 3×15, glute bridges 3×12.
Rest: 60–90 seconds.
Cooldown: Gentle lower-body stretching.

DAY 4 — Recovery
Warm-up: 5 minutes gentle walking.
Main workout: Easy walk 20–30 minutes plus 10 minutes of mobility or yoga.
Rest: Keep effort easy.
Cooldown: Breathing and gentle stretching.

DAY 5 — Upper Body + Core
Warm-up: 7 minutes shoulder and upper-back mobility.
Main workout: Incline push-ups 3×8, resistance-band rows 3×12, shoulder raises 2×10, dead bugs 3×8/side.
Rest: 60–90 seconds.
Cooldown: Gentle upper-body stretching.

DAY 6 — Cardio Intervals
Warm-up: 8 minutes easy walking.
Main workout: 6 rounds of 1 minute brisk effort + 2 minutes easy effort.
Rest: Use the easy intervals for recovery.
Cooldown: 5–8 minutes easy walking.

DAY 7 — Rest + Reflection
Warm-up: Optional 5-minute easy walk.
Main workout: Rest, or gentle mobility for 10–15 minutes.
Recovery: Hydrate, sleep well, and note how the week felt.
Cooldown: Not applicable.

Safety note: Stop if you experience significant pain, dizziness, chest pain, or unusual shortness of breath and seek appropriate medical advice."""


def _mock_tip(goal: str) -> str:
    tips = {
        "weight loss": "Build meals around vegetables, a protein source, whole-food carbohydrates, and healthy fats. Drink water regularly and focus on sustainable habits rather than extreme restriction.",
        "muscle gain": "Include a protein-rich food at regular meals, such as eggs, dairy, fish, chicken, soy, beans, or lentils, and pair it with enough overall food to support training and recovery.",
        "general wellness": "Aim for balanced meals, regular hydration, adequate sleep, and a variety of minimally processed foods. Consistency matters more than perfection.",
        "flexibility": "Stay hydrated and include protein-rich, balanced meals while giving your body enough recovery time. Gentle mobility work is most useful when practiced consistently.",
    }
    return tips.get(goal, tips["general wellness"])


@lru_cache(maxsize=1)
def _client():
    settings = get_settings()
    if not settings.gemini_api_key:
        return None
    from google import genai
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str, *, system_instruction: str, model_role: str) -> str:
    settings = get_settings()

    if settings.use_mock_ai or not settings.gemini_api_key:
        return _mock_workout(prompt) if model_role == "workout" else _mock_tip(prompt)

    client = _client()
    model = settings.workout_model if model_role == "workout" else settings.nutrition_model

    from google.genai import types

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7 if model_role == "workout" else 0.5,
            max_output_tokens=5000 if model_role == "workout" else 500,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text
