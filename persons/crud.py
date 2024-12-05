from tkinter import N
from sqlalchemy import true
from sqlalchemy.orm import Session
from persons.models import Person
from persons.schemas import PersonCreate, PersonUpdate
from datetime import date


def get_persons(db: Session):
    return db.query(Person).all()

def get_person_by_id(db: Session, person_id: str):
    return db.query(Person).filter(Person.person_id == person_id).first()


# Function to return mock data and success message
def get_person_verification_data(db: Session, person_id: str):
    data = db.query(Person).filter(Person.person_id == person_id).first()
    if not data:
        return {"error": "Person not found."}

    mock_data = {
        "person_name": data.person_name,
        "email": data.email,
        "phone_number": data.phone_number,
        "first_name":data.first_name,
        "middle_name":data.middle_name,
        "last_name": data.last_name,
        "user_id":data.user_id,
        "father_name":"John Doe",
        "date_of_birth":date(1990, 1, 1),
        "marital_status":"Single",
        "gender":"Female",
        "house_flat_no":"123",
        "street":"Sample Street",
        "city":"London",
        "postal_code":"XYZ 1AB",
        "state":"London",
        "country":"UK",
        "current_house_flat_no":"123",
        "current_street":"Sample Street",
        "current_city":"London",
        "current_postal_code":"XYZ 1AB",
        "current_state":"London",
        "current_country":"UK",
        "no_of_dependents":"0",
        "time_at_current_address":"5",
        "verified_user": "true"
    }
    return mock_data

def create_person(db: Session, person: PersonCreate):
    db_person = Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: str, person: PersonUpdate):
    db_person = get_person_by_id(db, person_id)
    if not db_person:
        return None
    for key, value in person.dict(exclude_unset=True).items():
        setattr(db_person, key, value)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: str):
    db_person = get_person_by_id(db, person_id)
    if not db_person:
        return None
    db.delete(db_person)
    db.commit()
    return db_person