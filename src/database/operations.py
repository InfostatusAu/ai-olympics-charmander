import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Prospect, ProspectStatus

DATABASE_URL = "sqlite+aiosqlite:///data/database/prospects.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_prospect(prospect_id: uuid.UUID) -> Optional[Prospect]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Prospect).filter(Prospect.id == prospect_id))
        return result.scalars().first()

async def get_prospect_by_domain(domain: str) -> Optional[Prospect]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Prospect).filter(Prospect.domain == domain))
        return result.scalars().first()

async def create_prospect(company_name: str, domain: str) -> Prospect:
    async with AsyncSessionLocal() as session:
        prospect = Prospect(company_name=company_name, domain=domain)
        session.add(prospect)
        await session.commit()
        await session.refresh(prospect)
        return prospect

async def update_prospect_status(prospect_id: uuid.UUID, status: ProspectStatus) -> Optional[Prospect]:
    async with AsyncSessionLocal() as session:
        prospect = await get_prospect(prospect_id)
        if prospect:
            prospect.status = status
            await session.commit()
            await session.refresh(prospect)
        return prospect

async def delete_prospect(prospect_id: uuid.UUID) -> bool:
    async with AsyncSessionLocal() as session:
        prospect = await get_prospect(prospect_id)
        if prospect:
            await session.delete(prospect)
            await session.commit()
            return True
        return False

async def list_prospects(skip: int = 0, limit: int = 100) -> List[Prospect]:
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Prospect).offset(skip).limit(limit))
        return list(result.scalars().all())
