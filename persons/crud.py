from sqlalchemy.orm import Session
from persons.models import Person
from persons.schemas import PersonCreate, PersonUpdate
from datetime import date
from uuid import uuid4

def get_persons(db: Session):
    return db.query(Person).all()

def get_person_by_id(db: Session, person_id: str):
    return db.query(Person).filter(Person.person_id == person_id).first()


# Function to return mock data and success message
def get_person_mock_data(db: Session):
    # Mock data
    mock_data = {
        "Name": "Jane Smith",
        "DOB": "1990-01-01",
        "ID-Document Type": "Driving License",
        "Gender": "Female",
        "Success Msg": "Id Verification is successful!"
    }
    
    # Create a new `Person` instance from the mock data
    new_person = Person(
        person_id=uuid4(),
        person_name="Jane Smith",
        applicant_id=None,
        first_name="Jane",
        middle_name=None,
        last_name="Smith",
        father_name="John Doe",
        email="janesmith@example.com",
        phone_number="1234567890",
        date_of_birth=date(1990, 1, 1),
        marital_status="Single",
        gender="Female",
        house_flat_no="123",
        street="Sample Street",
        city="London",
        postal_code="XYZ 1AB",
        state="London",
        country="UK",
        current_house_flat_no="123",
        current_street="Sample Street",
        current_city="London",
        current_postal_code="XYZ 1AB",
        current_state="London",
        current_country="UK",
        no_of_dependents=0,
        time_at_current_address=5,
        user_id=None
    )
    
    # Add and commit the new person to the database
    db.add(new_person)
    db.commit()
    
    # Return mock data
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