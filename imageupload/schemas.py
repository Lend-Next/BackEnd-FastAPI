from pydantic import BaseModel
from typing import Optional

class FileBase(BaseModel):
    file_uri: str
    person_id: str
    document_category: Optional[str]

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: str

    class Config:
        orm_mode = True
