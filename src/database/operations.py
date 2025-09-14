import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Prospect, ProspectStatus
from src.config import DATABASE_URL

async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db(engine=None):
    """Initialize database by creating all tables."""
    target_engine = engine or async_engine
    async with target_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_prospect(session: AsyncSession, prospect_id: str) -> Optional[Prospect]:
    """Get a prospect by ID."""
    result = await session.execute(select(Prospect).filter(Prospect.id == prospect_id))
    return result.scalars().first()

async def get_prospect_by_domain(session: AsyncSession, domain: str) -> Optional[Prospect]:
    """Get a prospect by domain."""
    result = await session.execute(select(Prospect).filter(Prospect.domain == domain))
    return result.scalars().first()

async def create_prospect(session: AsyncSession, prospect_id: str, company_name: str, domain: str) -> Prospect:
    """Create a new prospect."""
    prospect = Prospect(id=prospect_id, company_name=company_name, domain=domain)
    session.add(prospect)
    await session.commit()
    await session.refresh(prospect)
    return prospect

async def update_prospect_status(session: AsyncSession, prospect_id: str, status: ProspectStatus) -> Optional[Prospect]:
    """Update a prospect's status."""
    prospect = await get_prospect(session, prospect_id)
    if prospect:
        prospect.status = status
        await session.commit()
        await session.refresh(prospect)
    return prospect

async def delete_prospect(session: AsyncSession, prospect_id: str) -> bool:
    """Delete a prospect by ID."""
    prospect = await get_prospect(session, prospect_id)
    if prospect:
        await session.delete(prospect)
        await session.commit()
        return True
    return False

async def list_prospects(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[Prospect]:
    """List all prospects with pagination."""
    result = await session.execute(select(Prospect).offset(skip).limit(limit))
    return list(result.scalars().all())

# Convenience functions using default session for backward compatibility
async def get_prospect_default(prospect_id: str) -> Optional[Prospect]:
    """Get a prospect by ID using default session."""
    async with AsyncSessionLocal() as session:
        return await get_prospect(session, prospect_id)

async def get_prospect_by_domain_default(domain: str) -> Optional[Prospect]:
    """Get a prospect by domain using default session."""
    async with AsyncSessionLocal() as session:
        return await get_prospect_by_domain(session, domain)

async def create_prospect_default(prospect_id: str, company_name: str, domain: str) -> Prospect:
    """Create a new prospect using default session."""
    async with AsyncSessionLocal() as session:
        return await create_prospect(session, prospect_id, company_name, domain)

async def update_prospect_status_default(prospect_id: str, status: ProspectStatus) -> Optional[Prospect]:
    """Update a prospect's status using default session."""
    async with AsyncSessionLocal() as session:
        return await update_prospect_status(session, prospect_id, status)

async def delete_prospect_default(prospect_id: str) -> bool:
    """Delete a prospect by ID using default session."""
    async with AsyncSessionLocal() as session:
        return await delete_prospect(session, prospect_id)

async def list_prospects_default(skip: int = 0, limit: int = 100) -> List[Prospect]:
    """List all prospects with pagination using default session."""
    async with AsyncSessionLocal() as session:
        return await list_prospects(session, skip, limit)
