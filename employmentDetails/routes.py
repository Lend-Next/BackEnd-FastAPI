from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Generator
from employmentDetails.crud import get_employer_details
from employmentDetails.schemas import EmploymentResponse

router = APIRouter()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{personId}", response_model=EmploymentResponse)
def employmentdetails(personId: str, db: Session = Depends(get_db)):  
    details = get_employer_details(personId, db)
    return details

