"""Unit tests for database operations."""
import pytest
import tempfile
import os
from datetime import datetime, UTC
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.database.models import Prospect, ProspectStatus, Base
from src.database.operations import (
    init_db, get_prospect, get_prospect_by_domain, create_prospect,
    update_prospect_status, delete_prospect, list_prospects
)


@pytest.fixture
async def test_db():
    """Create a temporary SQLite database for testing."""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)
    
    # Create test database URL
    database_url = f"sqlite+aiosqlite:///{db_path}"
    
    # Create async engine for testing
    engine = create_async_engine(database_url, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    yield SessionLocal, engine
    
    # Cleanup
    await engine.dispose()
    os.unlink(db_path)


@pytest.fixture
async def db_session(test_db):
    """Get a database session for testing."""
    SessionLocal, engine = test_db
    async with SessionLocal() as session:
        yield session


class TestProspectModel:
    """Test the Prospect model."""
    
    def test_prospect_creation(self):
        """Test creating a Prospect instance."""
        now = datetime.now()
        prospect = Prospect(
            id="test-123",
            domain="example.com",
            company_name="Example Corp",
            status=ProspectStatus.NEW,
            created_at=now,
            updated_at=now
        )
        
        assert prospect.id == "test-123"
        assert prospect.domain == "example.com"
        assert prospect.company_name == "Example Corp"
        assert prospect.status == ProspectStatus.NEW
        assert prospect.created_at is not None
        assert prospect.updated_at is not None
    
    def test_prospect_status_enum(self):
        """Test ProspectStatus enum values."""
        assert ProspectStatus.NEW.value == "new"
        assert ProspectStatus.RESEARCHED.value == "researched"
        assert ProspectStatus.PROFILED.value == "profiled"
        assert ProspectStatus.ERROR.value == "error"


class TestDatabaseOperations:
    """Test database operations."""
    
    async def test_create_prospect(self, db_session):
        """Test creating a prospect."""
        prospect_id = "test-prospect-1"
        domain = "testcompany.com"
        company_name = "Test Company"
        
        prospect = await create_prospect(
            session=db_session,
            prospect_id=prospect_id,
            domain=domain,
            company_name=company_name
        )
        
        assert prospect.id == prospect_id
        assert prospect.domain == domain
        assert prospect.company_name == company_name
        assert prospect.status == ProspectStatus.NEW
        assert prospect.created_at is not None
        assert prospect.updated_at is not None
    
    async def test_get_prospect(self, db_session):
        """Test retrieving a prospect by ID."""
        # Create a prospect first
        prospect_id = "test-prospect-2"
        created_prospect = await create_prospect(
            session=db_session,
            prospect_id=prospect_id,
            domain="gettest.com",
            company_name="Get Test Company"
        )
        
        # Retrieve the prospect
        retrieved_prospect = await get_prospect(db_session, prospect_id)
        
        assert retrieved_prospect is not None
        assert retrieved_prospect.id == prospect_id
        assert retrieved_prospect.domain == "gettest.com"
        assert retrieved_prospect.company_name == "Get Test Company"
    
    async def test_get_prospect_not_found(self, db_session):
        """Test retrieving a non-existent prospect."""
        prospect = await get_prospect(db_session, "non-existent-id")
        assert prospect is None
    
    async def test_get_prospect_by_domain(self, db_session):
        """Test retrieving a prospect by domain."""
        # Create a prospect first
        domain = "domaintest.com"
        created_prospect = await create_prospect(
            session=db_session,
            prospect_id="test-prospect-3",
            domain=domain,
            company_name="Domain Test Company"
        )
        
        # Retrieve the prospect by domain
        retrieved_prospect = await get_prospect_by_domain(db_session, domain)
        
        assert retrieved_prospect is not None
        assert retrieved_prospect.domain == domain
        assert retrieved_prospect.company_name == "Domain Test Company"
    
    async def test_get_prospect_by_domain_not_found(self, db_session):
        """Test retrieving a prospect by non-existent domain."""
        prospect = await get_prospect_by_domain(db_session, "nonexistent.com")
        assert prospect is None
    
    async def test_update_prospect_status(self, db_session):
        """Test updating a prospect's status."""
        # Create a prospect first
        prospect_id = "test-prospect-4"
        created_prospect = await create_prospect(
            session=db_session,
            prospect_id=prospect_id,
            domain="statustest.com",
            company_name="Status Test Company"
        )
        
        # Update the status
        updated_prospect = await update_prospect_status(
            session=db_session,
            prospect_id=prospect_id,
            status=ProspectStatus.RESEARCHED
        )
        
        assert updated_prospect is not None
        assert updated_prospect.status == ProspectStatus.RESEARCHED
        assert updated_prospect.updated_at > updated_prospect.created_at
    
    async def test_update_prospect_status_not_found(self, db_session):
        """Test updating status of non-existent prospect."""
        updated_prospect = await update_prospect_status(
            session=db_session,
            prospect_id="non-existent",
            status=ProspectStatus.RESEARCHED
        )
        assert updated_prospect is None
    
    async def test_delete_prospect(self, db_session):
        """Test deleting a prospect."""
        # Create a prospect first
        prospect_id = "test-prospect-5"
        created_prospect = await create_prospect(
            session=db_session,
            prospect_id=prospect_id,
            domain="deletetest.com",
            company_name="Delete Test Company"
        )
        
        # Delete the prospect
        success = await delete_prospect(db_session, prospect_id)
        assert success is True
        
        # Verify it's gone
        retrieved_prospect = await get_prospect(db_session, prospect_id)
        assert retrieved_prospect is None
    
    async def test_delete_prospect_not_found(self, db_session):
        """Test deleting a non-existent prospect."""
        success = await delete_prospect(db_session, "non-existent")
        assert success is False
    
    async def test_list_prospects(self, db_session):
        """Test listing all prospects."""
        # Create multiple prospects
        prospects_data = [
            ("list-test-1", "list1.com", "List Company 1"),
            ("list-test-2", "list2.com", "List Company 2"),
            ("list-test-3", "list3.com", "List Company 3"),
        ]
        
        for prospect_id, domain, company_name in prospects_data:
            await create_prospect(
                session=db_session,
                prospect_id=prospect_id,
                domain=domain,
                company_name=company_name
            )
        
        # List all prospects
        prospects = await list_prospects(db_session)
        
        # Should have at least the 3 we created
        assert len(prospects) >= 3
        
        # Check that our test prospects are in the list
        prospect_ids = {p.id for p in prospects}
        for prospect_id, _, _ in prospects_data:
            assert prospect_id in prospect_ids
    
    async def test_list_prospects_empty(self, db_session):
        """Test listing prospects when database is empty."""
        prospects = await list_prospects(db_session)
        assert prospects == []


class TestDatabaseIntegration:
    """Test database initialization and integration."""
    
    async def test_init_db(self):
        """Test database initialization."""
        # Create temporary database file
        db_fd, db_path = tempfile.mkstemp(suffix='.db')
        os.close(db_fd)
        
        try:
            # Test database initialization
            database_url = f"sqlite+aiosqlite:///{db_path}"
            engine = create_async_engine(database_url, echo=False)
            
            # This should create all tables without error
            await init_db(engine)
            
            # Verify tables were created by checking if we can create a session
            from sqlalchemy.orm import sessionmaker
            SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
            
            async with SessionLocal() as session:
                # Try to create a prospect to verify schema
                prospect = await create_prospect(
                    session=session,
                    prospect_id="init-test",
                    domain="inittest.com",
                    company_name="Init Test Company"
                )
                assert prospect is not None
            
            await engine.dispose()
            
        finally:
            # Cleanup
            if os.path.exists(db_path):
                os.unlink(db_path)


@pytest.mark.asyncio
async def test_concurrent_operations(test_db):
    """Test concurrent database operations."""
    SessionLocal, engine = test_db
    
    async def create_test_prospect(session, prospect_id):
        return await create_prospect(
            session=session,
            prospect_id=prospect_id,
            domain=f"{prospect_id}.com",
            company_name=f"Company {prospect_id}"
        )
    
    # Create multiple sessions and prospects concurrently
    import asyncio
    
    async def concurrent_task(i):
        async with SessionLocal() as session:
            return await create_test_prospect(session, f"concurrent-{i}")
    
    # Run concurrent operations
    tasks = [concurrent_task(i) for i in range(3)]
    results = await asyncio.gather(*tasks)
    
    # All should succeed
    assert len(results) == 3
    for result in results:
        assert result is not None
    
    # Verify all were created
    async with SessionLocal() as session:
        prospects = await list_prospects(session)
        concurrent_ids = {p.id for p in prospects if p.id.startswith("concurrent-")}
        assert len(concurrent_ids) == 3
