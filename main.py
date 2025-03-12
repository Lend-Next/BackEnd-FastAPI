from fastapi import FastAPI
from persons.routes import router as persons_router
from bankaccount.routes import router as bankaccount_router
from database import engine
from persons.models import Base  # Import the Base from your models
from fastapi.middleware.cors import CORSMiddleware
from registration.routes import router as registration_router
from scorecard.routes import router as scorecard_router
from application.routes import router as application_router
from imageupload.routes import router as image_router
from employmentverification.routes import router as employment_verification_router
from employmentDetails.routes import router as employment_details_router


app = FastAPI(title="CK-LendNext API")

# Create the database tables
Base.metadata.create_all(bind=engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include feature-specific routers
app.include_router(registration_router, prefix="/registration", tags=["Registration"])
app.include_router(persons_router, prefix="/persons", tags=["Persons"])
app.include_router(image_router, prefix="/uploadimage", tags=["S3 Image Upload"])
app.include_router(bankaccount_router, prefix="/bankaccount", tags=["BankAccount"])

app.include_router(scorecard_router,prefix="/scorecard", tags=["Scorecard"])
app.include_router(application_router, prefix="/application", tags=["Application"])
app.include_router(employment_verification_router, prefix="/employmentverification", tags=["Employment Verification"])
app.include_router(employment_details_router, prefix="/employmentdetails", tags=["Employment Details"])


@app.get("/")
def read_root():
    return {"message": "Welcome to CK-LendNext!"}
