from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from engine import engine

SessionLocal = sessionmaker(
    engine, 
    lass_=AsyncSession, 
    expire_on_commit=False
)