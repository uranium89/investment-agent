from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from pipeline.config import settings

engine = create_async_engine(settings.db_url, echo=False, pool_size=10, max_overflow=20)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


async def init_db():
    from pipeline.db.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    await engine.dispose()
