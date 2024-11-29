from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import jwt
import boto3
from typing import Optional
from datetime import datetime, timedelta
from employmentverification.schemas import EmploymentResponse,EmploymentRequest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database import SessionLocal  # Importing SessionLocal from database.py
from employmentverification.crud import fetch_company_details
from employmentverification.models import employmentverification
from getaccounts.schemas import GetBankAccountResponse
from getaccounts.models import GetBankAccount
from typing import List

app = FastAPI()

#mock response for getaccounts
mock_data = {
    "results": [
        {
            "update_timestamp": "2017-02-07T17:29:24.740802Z",
            "account_id": "f1234560abf9f57287637624def390871",
            "account_type": "TRANSACTION",
            "display_name": "Club Lloyds",
            "currency": "GBP",
            "account_number": {
                "iban": "GB35LOYD12345678901234",
                "number": "12345678",
                "sort_code": "12-34-56",
                "swift_bic": "LOYDGB2L"
            },
            "provider": {
                "provider_id": "lloyds"
            }
        },
        {
            "update_timestamp": "2017-02-07T17:29:24.740802Z",
            "account_id": "f1234560abf9f57287637624def390872",
            "account_type": "SAVINGS",
            "display_name": "Club Lloyds",
            "currency": "GBP",
            "account_number": {
                "iban": "GB35LOYD12345678901235",
                "number": "12345679",
                "sort_code": "12-34-57",
                "swift_bic": "LOYDGB2L"
            },
            "provider": {
                "provider_id": "lloyds"
            }
        }
    ]
}

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

# Dependency to get the database session
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session so it can be used in endpoints
    finally:
        db.close()  # Make sure to close the session when done
    #models.Base.metadata.create_all(bind=engine)

@app.post("/employmentverification",response_model=EmploymentResponse)
def employmentdetails(request: EmploymentRequest, db: Session = Depends(get_db)):
    email = request.email

    details = fetch_company_details(email)
    record = employmentverification(
        mail=email,
        company_name=details["company_name"],
        result=details["result"],
        current_term=details["current_term"],
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    # Return the response
    return {
        "mail": email,
        "company_name": details["company_name"],
        "result": details["result"],
        "current_term": details["current_term"],
    }

@app.get("/accounts", response_model=List[GetBankAccountResponse])
def get_accounts():
    session = SessionLocal()
    try:
        for item in mock_data["results"]:
            account_number = item["account_number"]
        
            if not session.query(GetBankAccount).filter_by(account_id=item["account_id"]).first():
                account = GetBankAccount(
                    account_id = item["account_id"],
                    account_type = item["account_type"],
                    display_name=item["display_name"],
                    currency=item["currency"],
                    iban=account_number["iban"],
                    number=account_number["number"],
                    sort_code=account_number["sort_code"],
                    swift_bic=account_number["swift_bic"],
                    person_id=None,
                    agent_id=None
                )
                session.add(account)
        session.commit()
        

        accounts = session.query(GetBankAccount).all()
        return accounts
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
