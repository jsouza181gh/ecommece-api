from sqlalchemy.orm import declarative_base
from .engine import engine

Base = declarative_base()

from modules.product.models import Product, ProductImage, ProductReview, ProductCategory, ProductDescriptionSection

async def createDataBase():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)