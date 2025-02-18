import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from dotenv import load_dotenv, find_dotenv
from models import Base

load_dotenv(find_dotenv())


engine = create_async_engine(os.getenv('DB_URL'), echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)