from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text
from typing import AsyncGenerator
from app.core.settings import settings
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    settings.get_database_url,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_pre_ping=True
)

# Create async session factory
async_session_factory = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide an async database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db() -> None:
    """Initialize the database connection."""
    try:
        # Test connection
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1;"))
            logger.info(f"Database connection test: {result.scalar()}")
            
        # When not using Alembic, uncomment to create tables
        # async with engine.begin() as conn:
        #     await conn.run_sync(SQLModel.metadata.create_all)
        #     logger.info("Database tables created successfully")
            
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def shutdown_db() -> None:
    """Gracefully shutdown the database engine."""
    await engine.dispose()
    logger.info("Database engine disposed")
