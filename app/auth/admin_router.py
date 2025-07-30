# app/auth/admin_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import engine
from app.auth.models import User
from app.auth.dependencies import get_current_admin
from app.auth.schemas import UserAdminRead, UserAdminUpdate

router = APIRouter(
    prefix="/users",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)]
)

@router.get("/", response_model=list[UserAdminRead])
def list_users(skip: int = 0, limit: int = 100):
    with Session(engine) as sess:
        return sess.exec(select(User).offset(skip).limit(limit)).all()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    with Session(engine) as sess:
        user = sess.get(User, user_id)
        if not user:
            raise HTTPException(404, "User not found")
        sess.delete(user)
        sess.commit()


@router.patch("/{user_id}/promote", response_model=UserAdminRead, summary="Grant admin rights to a user")
def promote_user(user_id: int):
    with Session(engine) as sess:
        user = sess.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_admin:
            raise HTTPException(status_code=400, detail="User is already an admin")
        user.is_admin = True
        sess.add(user)
        sess.commit()
        sess.refresh(user)
        return user

@router.patch("/{user_id}/demote", response_model=UserAdminRead, summary="Revoke admin rights from a user")
def demote_user(user_id: int):
    with Session(engine) as sess:
        user = sess.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not user.is_admin:
            raise HTTPException(status_code=400, detail="User is not an admin")
        user.is_admin = False
        sess.add(user)
        sess.commit()
        sess.refresh(user)
        return user
