from pydantic import BaseModel

class FileBase(BaseModel):
    file_uri: str
    person_id: str

class FileCreate(FileBase):
    pass

class FileResponse(FileBase):
    id: str

    class Config:
        orm_mode = True
