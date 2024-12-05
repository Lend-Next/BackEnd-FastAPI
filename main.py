from fastapi import FastAPI
from persons.routes import router as persons_router
from database import engine
from persons.models import Base  # Import the Base from your models
from fastapi.middleware.cors import CORSMiddleware
from registration.routes import router as registration_router
# from imageupload.routes import router as image_router


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
# app.include_router(user_info_router, prefix="/current-user", tags=["User Info"])
# app.include_router(image_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CK-LendNext!"}
