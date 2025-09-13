from datetime import datetime
import uuid
from enum import Enum as PythonEnum
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProspectStatus(PythonEnum):
    IN_PROGRESS = "in_progress"
    RESEARCHED = "researched"

class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, nullable=False)
    status = Column(Enum(ProspectStatus), default=ProspectStatus.IN_PROGRESS, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Prospect(id='{self.id}', company_name='{self.company_name}', domain='{self.domain}')>"