from datetime import datetime, UTC
import uuid
from enum import Enum as PythonEnum
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ProspectStatus(PythonEnum):
    NEW = "new"
    RESEARCHED = "researched"
    PROFILED = "profiled"
    ERROR = "error"

class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(String(36), primary_key=True)  # UUID as string for SQLite compatibility
    company_name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, nullable=False)
    status = Column(Enum(ProspectStatus), default=ProspectStatus.NEW, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Prospect(id='{self.id}', company_name='{self.company_name}', domain='{self.domain}')>"