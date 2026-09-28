from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Plan, User


def get_user(db: Session, user_id: str) -> User | None:
    return db.scalar(select(User).where(User.user_id == user_id))


def save_user(db: Session, data) -> User:
    user = get_user(db, data.user_id)
    if user is None:
        user = User(
            user_id=data.user_id,
            name=data.name,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
        )
        db.add(user)
    else:
        user.name = data.name
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity
    db.commit()
    db.refresh(user)
    return user


def save_plan(db: Session, user_id: str, original_plan: str, nutrition_tip: str) -> Plan:
    plan = Plan(
        user_id=user_id,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_plan(db: Session, user_id: str) -> Plan | None:
    return db.scalar(
        select(Plan)
        .where(Plan.user_id == user_id)
        .order_by(Plan.created_at.desc(), Plan.id.desc())
        .limit(1)
    )


def update_plan(db: Session, plan: Plan, updated_plan: str, feedback: str, nutrition_tip: str | None = None) -> Plan:
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    if nutrition_tip:
        plan.nutrition_tip = nutrition_tip
    db.commit()
    db.refresh(plan)
    return plan


def get_all_users_with_plans(db: Session) -> list[tuple[User, Plan | None]]:
    users = db.scalars(select(User).order_by(User.created_at.desc())).all()
    return [(user, get_latest_plan(db, user.user_id)) for user in users]
