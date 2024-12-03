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


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all folder variables
from registration.routes import router as registration_router
# from registration.schemas import UserEmail, CreateUser, ConfirmUser, SigninUser
# from registration.crud import create_user, confirm_signup, signin_user

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





# class Token(BaseModel):
#     access_token: str
#     token_type: str



# def decode_jwt_token(token: str):
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithm=["HS256"])
#         return payload
#     except jwt.ExpireSignatureError:
#         raise HTTPException(status_code=401, detail="token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="invalid token")

# @app.post("/signup", response_model=dict)
# async def signup(user: CreateUser):  
#     return create_user(user=user)

# @app.post("/confirm", response_model=dict)
# async def confirmSignup(user: ConfirmUser):
#     return confirm_signup(user=user)

# @app.post("/resend_confirm", response_model=dict)
# async def resendConfirm(user: UserEmail):
#     return resend_confirm(user=user)

# @app.post("/signin", response_model=dict)
# async def signin(user: SigninUser):
#     return signin_user(user=user)
    
app.include_router(registration_router, prefix="/registration", tags=["Registration"])