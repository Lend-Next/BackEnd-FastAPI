from sqlalchemy.orm import Session
from fastapi import HTTPException
from employmentverification.models import EmploymentVerification
from sqlalchemy.exc import IntegrityError
from datetime import date
from employmentverification.schemas import EmploymentResponse

def is_valid_email(email: str) -> bool:
    return '.' in email and '@' in email

def create_employment_record(email: str, db: Session):
    try:
        domain = email.split("@")[1].split(".")[0]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid Email-Id.")

    employer_name = f"{domain.capitalize()} Private Limited"

    new_record = EmploymentVerification(
        email=email,
        employer_name=employer_name,
        designation="Software Engineer",
        start_date=date(2022, 9, 28),  # Explicitly setting default values
        employer_address="Kolkata, India"
    )

    db.add(new_record)
    try:
        db.commit()
        db.refresh(new_record)
        return new_record
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists in records")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def fetch_company_details(email: str, db: Session):
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    record = db.query(EmploymentVerification).filter_by(email=email).first()  # Fixed filter_by column

    if not record:
        record = create_employment_record(email, db)

    return EmploymentResponse(
        employeeId=record.employee_id,
        email=record.email,
        employerName=record.employer_name,
        designation=record.designation,
        startDate=record.start_date,
        employerAddress=record.employer_address
    )
