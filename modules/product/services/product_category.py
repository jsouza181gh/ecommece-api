from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from uuid import UUID

from ..schemas import SaveProductCategorySchema, ProductCategorySchema
from ..repositories import ProductCategoryRepository
from ..models import ProductCategory

@dataclass
class ProductCategoryService:
    category_repository: ProductCategoryRepository

    async def create(self, category_schema: SaveProductCategorySchema) -> ProductCategorySchema:
        category = ProductCategory(
            name=category_schema.name
        )

        try:
            new_category = await self.category_repository.create(category)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Category already exists'
            )

        return ProductCategorySchema.model_validate(new_category)
    

    async def find_by_id(self, category_id: UUID) -> ProductCategorySchema:
        category = await self.category_repository.find_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )
        
        return ProductCategorySchema.model_validate(category)
    

    async def find_all(self, name: Optional[str]) -> List[ProductCategorySchema]:
        categories = await self.category_repository.find_all(name)

        return [
            ProductCategorySchema.model_validate(category)
            for category in categories
        ]
    

    async def update(
        self,
        category_id: UUID,
        category_schema: SaveProductCategorySchema
    ) -> ProductCategorySchema:

        category = await self.category_repository.find_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )
        
        category.name = category_schema.name

        try:
            new_category = await self.category_repository.update(category)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Category with this name already exists'
            )

        return ProductCategorySchema.model_validate(new_category)
    
    async def delete(self, category_id: UUID) -> None:
        category = await self.category_repository.find_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )
        
        await self.category_repository.delete(category)