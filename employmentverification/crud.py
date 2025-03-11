from sqlalchemy.orm import Session
from fastapi import HTTPException
from employmentverification.models import EmploymentVerification
from random import randint
import re
from sqlalchemy.exc import IntegrityError

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def fetch_company_details(email: str, db: Session):
    if not is_valid_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    if "gmail" in email:
        raise HTTPException(status_code=404, detail="No employment info found")

    record = db.query(EmploymentVerification).filter_by(mail=email).first()
    if not record:
        raise HTTPException(status_code=404, detail="Email not found")

    return {
        "mail": record.mail,  # ✅ Ensure 'mail' is returned
        "company_name": record.company_name,
        "result": record.result,
        "current_term": record.current_term
    }

def create_employment_record(email: str, db: Session):
    if "gmail" in email:
        raise HTTPException(status_code=404, detail="No employment info found")

    # Safe domain extraction
    try:
        domain = email.split("@")[1].split(".")[0]
    except IndexError:
        raise HTTPException(status_code=400, detail="Invalid email structure")

    company_name = f"{domain.capitalize()} Pvt. Ltd"  # Capitalize domain name
    current_term = randint(6, 120)  # Ensure it's within a valid range

    new_record = EmploymentVerification(
        mail=email,
        company_name=company_name,
        result="Success",
        current_term=current_term
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
