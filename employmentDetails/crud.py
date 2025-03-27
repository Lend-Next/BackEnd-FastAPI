
from sqlalchemy.orm import Session
from persons.models import Person
from employmentDetails.models import EmploymentVerification
from employmentDetails.schemas import EmploymentResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from datetime import date

def create_employment_record(email: str, db: Session):
    employer_name = "CloudKaptan Consultancy Services Private Limited"

    new_record = EmploymentVerification(
        email=email,
        employer_name=employer_name,
        designation="Software Engineer",
        start_date=date(2022, 9, 28),
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
    

def get_employer_details(personId: str, db: Session,):
    email = db.query(Person).filter(Person.person_id == personId).first().email
    if email is None:
        return {"No Employment Info Found."}
    else:
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