from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserInfoResponse, UserIdResponse
from .crud import get_user_info, get_user_id

JWT_SECRET= 'your-jwt-secret-key'

router = APIRouter()

# Helper function to extract the token from the Authorization header

def get_token_from_header(authorization: str):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    return authorization.split(" ")[1]

# Route to get user info
@router.get("/user-info", response_model=UserInfoResponse)
def fetch_user_info(authorization: str = Depends(get_token_from_header)):
    token = get_token_from_header(authorization)
    return get_user_info(token)

# Route to get user ID
@router.get("/user-id", response_model=UserIdResponse)
def fetch_user_id(authorization: str = Depends(get_token_from_header)):
    token = get_token_from_header(authorization)
    return get_user_id(token)
