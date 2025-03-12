from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Generator
from employmentverification.crud import fetch_company_details
from employmentverification.schemas import EmploymentResponse

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{email}", response_model=EmploymentResponse)
def employmentdetails(email: str, db: Session = Depends(get_db)):  
    if "gmail" in email:
        raise HTTPException(status_code=404, detail="No employment info found")

    details = fetch_company_details(email, db)
    return details

