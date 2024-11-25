# from fastapi import FastAPI, HTTPException, Depends, status, Response
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from typing import List, Annotated
# from registration import models
# from database import engine, SessionLocal
# from sqlalchemy.orm import Session

# from registration.crud import create_user, get_users, delete_users, update_users

# from registration.schemas import UserCreate, ResponseUser

# # Create an instance of the FastAPI class
# app = FastAPI()

# models.Base.metadata.create_all(bind=engine)

# # class groupBase(BaseModel):
# #     group_name: str
# #     description: str
# #     is_active: bool

# #     class Config:
# #         orm_mode = True

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # db_dependency = Annotated[Session, Depends(get_db)]
 


# @app.post("/users/", status_code= status.HTTP_201_CREATED)
# async def create_user_records(user: UserCreate, db: Session = Depends(get_db)):  
#     try:
#         db_user = create_user(db=db, user=user)
#         return db_user
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# @app.get("/users/", status_code= 200, response_model = List[ResponseUser])
# async def get_user_records(firstname, response: Response, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     try:
#         db_users = get_users(firstname=firstname, response=response, db=db, skip=skip, limit=limit)
#         return db_users
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")\
        
# @app.delete("/users/", status_code= status.HTTP_204_NO_CONTENT)
# async def delete_user_records(firstname, db: Session = Depends(get_db)):
#     try:
#         message = delete_users(firstname=firstname, db=db)
#         return message
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# @app.put("/users/", status_code= status.HTTP_202_ACCEPTED)
# async def update_user_records(firstname, mobilenumber, db: Session = Depends(get_db)):
#     try:
#         message = update_users(firstname=firstname, mobilenumber=mobilenumber, db=db)
#         return message
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
import boto3
from typing import Optional
from datetime import datetime, timedelta

app = FastAPI()

# Cognito User Pool Settings
CLIENT_ID = 'hkibiomfmpuh9m0oorc1rknkk'
REGION = 'ap-south-1'
JWT_SECRET= 'your-jwt-secret-key'

cognito_client = boto3.client('cognito-idp',region_name=REGION)

# OAuth2 settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    name: str
    email: str
    mobile_number: Optional[str]= None
    password: str
    confirmation_code: Optional[str]= None

class Token(BaseModel):
    access_token: str
    token_type: str

def create_jwt_token(name: str):
    payload ={
        "sub": name,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token= jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def decode_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithm=["HS256"])
        return payload
    except jwt.ExpireSignatureError:
        raise HTTPException(status_code=401, detail="token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="invalid token")

@app.post("/Signup", response_model=dict)
async def signup(user: User):  
    try:
        response= cognito_client.sign_up(
            ClientId = CLIENT_ID,
            Username = user.email,
            Password = user.password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': user.email
                },
                {
                    'Name': 'name',
                    'Value': user.name
                },
                {
                    'Name': 'phone_number',
                    'Value': user.mobile_number
                }
            ]
        )
        return response
    except cognito_client.exceptions.UsernameExistsException:
        raise HTTPException(status_code=400, detail="User nameexists")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/Confirm", response_model=dict)
async def confirm_signup(user: User):  
    try:
        response= cognito_client.confirm_sign_up(
            ClientId = CLIENT_ID,
            Username = user.email,
            ConfirmationCode = user.confirmation_code
            
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/Signin", response_model=Token)
async def signin(user: User):  
    try:
        response= cognito_client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': user.email,
                'PASSWORD': user.password
            },
            ClientId = CLIENT_ID
        )
        token= create_jwt_token(user.email)
        return {'access_token': token, 'token_type': 'bearer'}
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))