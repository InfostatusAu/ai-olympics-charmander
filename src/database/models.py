
from sqlalchemy import Column, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Prospect(Base):
    __tablename__ = "prospects"

    id = Column(String, primary_key=True, index=True)
    company_name = Column(String, index=True)
    research_markdown = Column(Text)
    profile_markdown = Column(Text)

    def __repr__(self):
        return f"<Prospect(id='{self.id}', company_name='{self.company_name}')>"
