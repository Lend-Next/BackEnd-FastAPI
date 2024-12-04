from fastapi import HTTPException, status
import jwt
from datetime import datetime, timedelta

# Import all folder variables
from .__init__ import USER_POOL_ID, CLIENT_ID, JWT_SECRET, cognito_client
from registration.schemas import UserEmail, CreateUser, ConfirmUser, SigninUser

# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash_password(password: str) -> str:
#     return pwd_cxt.hash(password)

# def create_user(db: Session, user: UserCreate) -> users:
#     db_user = users(first_name=user.first_name, last_name=user.last_name, email=user.email, 
#                     mobile_number=user.mobile_number, encrypted_enpassword=hash_password(user.encrypted_enpassword), 
#                     user_type=user.user_type)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def get_users(firstname, response, db: Session, skip: int = 0, limit: int = 10):
#     db_users = db.query(users).filter(users.first_name == firstname).offset(skip).limit(limit).all()
#     if not db_users:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user is not exists')
#     return db_users

# def delete_users(firstname, db: Session):
#     db.query(users).filter(users.first_name == firstname).delete(synchronize_session=False)
#     db.commit()
#     return 'User is deleted.'

# def update_users(firstname, mobilenumber, db: Session):
#     db_users = db.query(users).filter(users.first_name == firstname)
#     if not db_users.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user is not exists for update')
    
#     db_users.update({'mobile_number':mobilenumber})
#     db.commit()
#     return 'user is updated.'

def create_user(user: CreateUser):
    try:
        print('hey-1')
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
                    'Value': user.firstName + ' ' + user.lastName
                },
                # {
                #     'Name': 'phone_number',
                #     'Value': user.mobile_number
                # }
            ]
        )
        print('hey0')
        return response
    except cognito_client.exceptions.UsernameExistsException:
        print('hey2')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User nameexists")
    except Exception as e:
        print('hey1')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def confirm_signup(user: ConfirmUser):
    try:
        response= cognito_client.confirm_sign_up(
            ClientId = CLIENT_ID,
            Username = user.email,
            ConfirmationCode = user.confirmationCode
            
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def resend_confirm(user: UserEmail):
    try:
        response = cognito_client.resend_confirmation_code(
            ClientId=CLIENT_ID,
            Username=user.email
        )
        return {"message": "Confirmation code has been resent to the user."}
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")
    except cognito_client.exceptions.LimitExceededException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Too many requests, please try again later.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def create_jwt_token(name: str):
    payload ={
        "sub": name,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token= jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

def signin_user(user: SigninUser):
    try:
        cognito_client.initiate_auth(
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))