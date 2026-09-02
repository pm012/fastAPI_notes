from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

# Зверніть увагу на +asyncpg у рядку підключення
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://serhii:secret01@localhost:5432/rest_app"

# Створюємо асинхронний рушій
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Створюємо фабрику асинхронних сесій
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Асинхронний генератор сесій для FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
