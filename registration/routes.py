from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from registration.schemas import SigninUser
from .crud import signin_user

from registration.schemas import UserEmail, CreateUser, ConfirmUser, SigninUser

from registration.crud import create_user, confirm_signup, resend_confirm, signin_user

router = APIRouter()

@router.post("/signup")
async def signup(user: CreateUser):  
    # print(create_user(user=user))
    return create_user(user=user)

@router.post("/confirm", response_model=dict)
async def confirmSignup(user: ConfirmUser):
    return confirm_signup(user=user)

@router.post("/resend_confirm", response_model=dict)
async def resendConfirm(user: UserEmail):
    return resend_confirm(user=user)

@router.post("/signin")
async def signin(user: SigninUser, db: Session = Depends(get_db)):  
    return signin_user(user, db)  # ✅ Explicitly pass `db`
