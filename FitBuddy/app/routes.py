from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import secrets

from .config import get_settings
from .crud import (
    get_all_users_with_plans,
    get_latest_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from .database import get_db
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .gemini_generator import generate_workout_gemini
from .schemas import FeedbackRequest, UserInput
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


def admin_required(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    settings = get_settings()
    valid_user = secrets.compare_digest(credentials.username, settings.admin_username)
    valid_password = secrets.compare_digest(credentials.password, settings.admin_password)
    if not (valid_user and valid_password):
        from fastapi.responses import Response
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"error": None},
    )


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserInput(
            user_id=user_id,
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )
        workout_plan = generate_workout_gemini(data)
        nutrition_tip = generate_nutrition_tip_with_flash(data.goal)
        save_user(db, data)
        save_plan(db, data.user_id, workout_plan, nutrition_tip)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": f"Could not generate the plan: {exc}"},
            status_code=500,
        )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": data.model_dump(),
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "plan_updated": False,
            "error": None,
        },
    )


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        request_data = FeedbackRequest(user_id=user_id, feedback=feedback)
        user = get_user(db, request_data.user_id)
        plan = get_latest_plan(db, request_data.user_id)

        if user is None or plan is None:
            raise HTTPException(status_code=404, detail="User or plan not found.")

        current_plan = plan.updated_plan or plan.original_plan
        revised_plan = update_workout_plan(
            current_plan,
            request_data.feedback,
            user.goal,
            user.intensity,
        )
        nutrition_tip = generate_nutrition_tip_with_flash(user.goal)
        update_plan(db, plan, revised_plan, request_data.feedback, nutrition_tip)

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Could not update the plan: {exc}") from exc

    user_dict = {
        "user_id": user.user_id,
        "name": user.name,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
    }
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "user": user_dict,
            "workout_plan": revised_plan,
            "nutrition_tip": nutrition_tip,
            "plan_updated": True,
            "error": None,
        },
    )


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(
    request: Request,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    records = get_all_users_with_plans(db)
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"records": records},
    )


@router.get("/api/health")
def health():
    return {"status": "ok", "service": "FitBuddy"}


@router.get("/api/users/{user_id}")
def api_user(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    plan = get_latest_plan(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return {
        "user": {
            "user_id": user.user_id,
            "name": user.name,
            "age": user.age,
            "weight": user.weight,
            "goal": user.goal,
            "intensity": user.intensity,
        },
        "plan": None if plan is None else {
            "id": plan.id,
            "original_plan": plan.original_plan,
            "updated_plan": plan.updated_plan,
            "nutrition_tip": plan.nutrition_tip,
            "feedback": plan.feedback,
        },
    }
