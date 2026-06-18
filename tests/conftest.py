import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.database import AsyncSessionLocal, init_db as create_tables
from src.main import app
from src.models import User

TEST_DATABASE_URL = "postgresql+asyncpg://kubsu:kubsu@127.0.0.1:5432/kubsu"
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestAsyncSessionLocal = sessionmaker(
    bind=test_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
async def init_db() -> None:
    async with test_engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(User.metadata.drop_all)


@pytest_asyncio.fixture(scope='function')
async def db() -> AsyncSession:
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope='function')
async def test_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(autouse=True, scope='function')
async def clear_table(init_db, db: AsyncSession) -> None:
    await db.execute(text("TRUNCATE users RESTART IDENTITY CASCADE;"))
    await db.commit()


@pytest_asyncio.fixture(scope='function')
async def user(db: AsyncSession) -> User:
    user = User(name="John Doe")
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user