from jose import jwt
from jose.exceptions import JWTError
import requests
from fastapi import HTTPException, status

# Cognito configuration
COGNITO_REGION = "ap-south-1"  # e.g., "us-east-1"
COGNITO_USER_POOL_ID = "CMRp1sN4W"
COGNITO_CLIENT_ID = "hkibiomfmpuh9m0oorc1rknkk"

def get_cognito_public_keys():
    url = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["keys"]

def decode_cognito_token(token: str):
    public_keys = get_cognito_public_keys()
    for key in public_keys:
        try:
            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                audience=COGNITO_CLIENT_ID,
                issuer=f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{COGNITO_USER_POOL_ID}",
            )
            return payload
        except JWTError:
            continue
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_user_info(token: str):
    payload = decode_cognito_token(token)
    user_id = payload.get("sub")
    email = payload.get("email")
    username = payload.get("cognito:username")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")
    return {
        "user_id": user_id,
        "email": email,
        "username": username
    }

def get_user_id(token: str):
    payload = decode_cognito_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User ID not found in token")
    return user_id