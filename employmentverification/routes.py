from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Generator
from employmentverification.crud import fetch_company_details, create_employment_record
from employmentverification.schemas import EmploymentResponse, EmploymentRequest
import logging

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/employmentverification", response_model=EmploymentResponse)
def employmentdetails(request: EmploymentRequest, db: Session = Depends(get_db)):
    email = request.email

    try:
        # Check if email contains 'gmail' (return 404)
        if "gmail" in email:
            raise HTTPException(status_code=404, detail="No employment info found")

        # Fetch details if email exists in the database
        details = fetch_company_details(email, db)
        return details

    except HTTPException as e:
        if e.status_code == 404:
            # If email is not found, create a new record
            new_record = create_employment_record(email, db)
            return {
                "mail": new_record.mail,
                "company_name": new_record.company_name,
                "result": new_record.result,
                "current_term": new_record.current_term,
            }

        raise HTTPException(status_code=500, detail="Unexpected error")
