from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Generator
from employmentverification.crud import fetch_company_details
from employmentverification.models import employmentverification
from employmentverification.schemas import EmploymentResponse,EmploymentRequest
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/employmentverification",response_model=EmploymentResponse)
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