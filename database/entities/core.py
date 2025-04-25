from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    """Асинхронный доступ к движку и сессиям"""
    async_engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
    async_session_factory: async_sessionmaker = async_sessionmaker(async_engine, expire_on_commit=False)

    def session(self):
        return self.async_session_factory()

class Base(DeclarativeBase):
    pass
