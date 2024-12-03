from fastapi import APIRouter,HTTPException

from pydantic import BaseModel
import requests

from .schemas import UserEmail, CreateUser, ConfirmUser, SigninUser
from .crud import create_user, confirm_signup, resend_confirm, signin_user

router = APIRouter()

@router.post("/signup", response_model=dict)
async def signup(user: CreateUser):  
    return create_user(user=user)

@router.post("/confirm", response_model=dict)
async def confirmSignup(user: ConfirmUser):
    return confirm_signup(user=user)

@router.post("/resend_confirm", response_model=dict)
async def resendConfirm(user: UserEmail):
    return resend_confirm(user=user)

@router.post("/signin", response_model=dict)
async def signin(user: SigninUser):
    return signin_user(user=user)