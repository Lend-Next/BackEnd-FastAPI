from sqlalchemy.orm import Session
from persons.models import Person
from persons.schemas import PersonCreate, PersonBase
from datetime import date


def get_persons(db: Session):
    return db.query(Person).all()

def get_person_by_id(db: Session, personId: str):
    return db.query(Person).filter(Person.person_id == personId).first()


# Function to return mock data and success message
def get_person_verification_data(db: Session, personId: str):
    data = db.query(Person).filter(Person.person_id == personId).first()
    if not data:
        return {"error": "Person not found."}

    mock_data = {
        "personName": data.first_name + " " + data.last_name,
        "email": data.email,
        "phoneNumber": data.phone_number,
        "firstName":data.first_name,
        "lastName": data.last_name,
        "userId":data.user_id,
        "fatherName":"John Doe",
        "DOB":date(1990, 1, 1),
        "maritalStatus":"Single",
        "gender":"Female",
        "houseFlatNo":"123",
        "street":"Sample Street",
        "city":"London",
        "postalCode":"XYZ 1AB",
        "state":"London",
        "country":"UK",
        "currentHouseFlatNo":"123",
        "currentStreet":"Sample Street",
        "currentCity":"London",
        "currentPostalCode":"XYZ 1AB",
        "currentState":"London",
        "currentCountry":"UK",
        "noOfDependents": 0,
        "timeAtCurrentAddress": 5,
        "verifiedUser": True
    }
    return mock_data

def create_person(db: Session, person: PersonCreate):
    db_person = Person(first_name=person.firstName, last_name=person.lastName, email=person.email, user_id=person.userId)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return {
        'personId' : db_person.person_id
    }

def update_person(db: Session, personId: str, person: PersonBase):
    # Fetch the person by ID
    db_person = get_person_by_id(db, personId)
    if not db_person:
        return None  # Return None if the person is not found

    db_person.email = person.email
    db_person.person_name = person.personName
    db_person.first_name = person.firstName
    db_person.last_name = person.lastName
    db_person.father_name = person.fatherName
    db_person.email = person.email
    db_person.marital_status = person.maritalStatus
    db_person.phone_number = person.phoneNumber
    db_person.date_of_birth = person.DOB
    db_person.gender = person.gender
    db_person.house_flat_no = person.houseFlatNo
    db_person.street = person.street
    db_person.city = person.city
    db_person.state = person.state
    db_person.postal_code = person.postalCode
    db_person.country = person.country
    db_person.current_house_flat_no = person.currentHouseFlatNo
    db_person.current_street = person.currentStreet
    db_person.current_city = person.currentCity
    db_person.current_postal_code = person.currentPostalCode
    db_person.current_state = person.currentState
    db_person.current_country = person.currentCountry
    db_person.no_of_dependents = person.noOfDependents
    db_person.time_at_current_address = person.timeAtCurrentAddress
    db_person.verified_user = person.verifiedUser

    # Commit changes and refresh the object
    db.commit()
    db.refresh(db_person)
    return db_person


def delete_person(db: Session, personId: str):
    db_person = get_person_by_id(db, personId)
    if not db_person:
        return None
    db.delete(db_person)
    db.commit()
    return db_person