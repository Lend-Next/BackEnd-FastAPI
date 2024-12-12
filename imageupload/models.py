from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid

class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    file_uri = Column(String, nullable=False)
    person_id = Column(UUID(as_uuid=True), ForeignKey("persons.person_id"), nullable=False)
    document_category = Column(String, nullable=True)