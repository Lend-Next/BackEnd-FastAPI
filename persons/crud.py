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

    # Update fields only if the values are provided
    if person.email is not None:
        db_person.email = person.email
    if person.personName is not None:
        db_person.person_name = person.personName
    if person.firstName is not None:
        db_person.first_name = person.firstName
    if person.lastName is not None:
        db_person.last_name = person.lastName
    if person.fatherName is not None:
        db_person.father_name = person.fatherName
    if person.maritalStatus is not None:
        db_person.marital_status = person.maritalStatus
    if person.phoneNumber is not None:
        db_person.phone_number = person.phoneNumber
    if person.DOB is not None:
        db_person.date_of_birth = person.DOB
    if person.gender is not None:
        db_person.gender = person.gender
    if person.houseFlatNo is not None:
        db_person.house_flat_no = person.houseFlatNo
    if person.street is not None:
        db_person.street = person.street
    if person.city is not None:
        db_person.city = person.city
    if person.state is not None:
        db_person.state = person.state
    if person.postalCode is not None:
        db_person.postal_code = person.postalCode
    if person.country is not None:
        db_person.country = person.country
    if person.currentHouseFlatNo is not None:
        db_person.current_house_flat_no = person.currentHouseFlatNo
    if person.currentStreet is not None:
        db_person.current_street = person.currentStreet
    if person.currentCity is not None:
        db_person.current_city = person.currentCity
    if person.currentPostalCode is not None:
        db_person.current_postal_code = person.currentPostalCode
    if person.currentState is not None:
        db_person.current_state = person.currentState
    if person.currentCountry is not None:
        db_person.current_country = person.currentCountry
    if person.noOfDependents is not None:
        db_person.no_of_dependents = person.noOfDependents
    if person.timeAtCurrentAddress is not None:
        db_person.time_at_current_address = person.timeAtCurrentAddress
    if person.verifiedUser is not None:
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

def get_person_address(db: Session, personId: str):
    db_person = get_person_by_id(db, personId)
    if not db_person:
        return None
    data = {
        "houseFlatNo":db_person.house_flat_no,
        "street":db_person.street,
        "city":db_person.city,
        "postalCode":db_person.postal_code,
        "state":db_person.state,
        "country":db_person.country,
        "currentHouseFlatNo":db_person.current_house_flat_no,
        "currentStreet":db_person.current_street,
        "currentCity":db_person.current_city,
        "currentPostalCode":db_person.current_postal_code,
        "currentState":db_person.current_state,
        "currentCountry":db_person.current_country
    }
    return data