from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from registration.models import users
from registration.schemas import UserCreate
from typing import List, Optional
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_cxt.hash(password)

def create_user(db: Session, user: UserCreate) -> users:
    db_user = users(first_name=user.first_name, last_name=user.last_name, email=user.email, 
                    mobile_number=user.mobile_number, encrypted_enpassword=hash_password(user.encrypted_enpassword), 
                    user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(firstname, response, db: Session, skip: int = 0, limit: int = 10):
    db_users = db.query(users).filter(users.first_name == firstname).offset(skip).limit(limit).all()
    if not db_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user is not exists')
    return db_users

def delete_users(firstname, db: Session):
    db.query(users).filter(users.first_name == firstname).delete(synchronize_session=False)
    db.commit()
    return 'User is deleted.'

def update_users(firstname, mobilenumber, db: Session):
    db_users = db.query(users).filter(users.first_name == firstname)
    if not db_users.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user is not exists for update')
    
    db_users.update({'mobile_number':mobilenumber})
    db.commit()
    return 'user is updated.'
