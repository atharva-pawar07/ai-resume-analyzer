import pytest_asyncio

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from backend.app.core.database import Base, get_db
from backend.app.models.user import User
from backend.app.models.resume import Resume
from backend.app.models.analysis import Analysis
from backend.app.models.job import Job
from backend.main import app


TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def test_db(test_engine_cleanup):
    test_tables = [
        User.__table__,
        Resume.__table__,
        Analysis.__table__,
        Job.__table__
    ]

    async with test_engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: Base.metadata.create_all(
                sync_connection,
                tables=test_tables
            )
        )

    async with TestingSessionLocal() as session:
        yield session

    async with test_engine.begin() as connection:
        await connection.run_sync(
            lambda sync_connection: Base.metadata.drop_all(
                sync_connection,
                tables=test_tables
            )
        )


@pytest_asyncio.fixture
async def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    from httpx import AsyncClient, ASGITransport

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_engine_cleanup():
    yield
    await test_engine.dispose()
