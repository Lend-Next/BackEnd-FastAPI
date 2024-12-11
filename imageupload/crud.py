import boto3
from sqlalchemy.orm import Session
from uuid import uuid4
from models import File
from schemas import FileCreate

# S3 Configuration
AWS_ACCESS_KEY_ID = "your-access-key"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
AWS_BUCKET_NAME = "your-bucket-name"
S3_FOLDER = "id-verification"

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

def upload_file_to_s3(file, person_id: str) -> str:
    file_id = str(uuid4())
    file_extension = file.filename.split(".")[-1]
    s3_key = f"{S3_FOLDER}/{file_id}.{file_extension}"

    s3_client.upload_fileobj(
        file.file,
        AWS_BUCKET_NAME,
        s3_key,
        ExtraArgs={"ContentType": file.content_type}
    )
    return f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"

def save_file_metadata(db: Session, file_data: FileCreate) -> File:
    new_file = File(
        id=str(uuid4()),
        file_uri=file_data.file_uri,
        person_id=file_data.person_id
    )
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file