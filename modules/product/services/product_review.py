from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID

from ..repositories import ProductReviewRepository, ProductRepository
from ..schemas import SaveProductReviewSchema, ProductReviewSchema
from ..models import ProductReview

@dataclass
class ProductReviewService:
    review_repository: ProductReviewRepository
    product_repository:ProductRepository

    async def create(self, review_schema: SaveProductReviewSchema) -> ProductReviewSchema:
        product_exists = await self.product_repository.exists(review_schema.product_id)

        if not product_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product was not found'
            )

        review_model = self.convert_schema_to_model(review_schema)

        try:
            await self.review_repository.create(review_model)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not create review due to data conflict'
            )
        
        return ProductReviewSchema.model_validate(review_model)


    async def find_by_id(self, review_id: UUID) -> ProductReviewSchema:
        review = await self.review_repository.find_by_id(review_id)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review was not found'
            )
        
        return ProductReviewSchema.model_validate(review)


    async def find_all(self) -> List[ProductReviewSchema]:
        reviews = await self.review_repository.find_all()

        return [
            ProductReviewSchema.model_validate(review)
            for review in reviews
        ]


    async def update(
        self, 
        review_id: UUID, 
        review_schema: SaveProductReviewSchema
    ) -> ProductReviewSchema:
        review = await self.review_repository.find_by_id(review_id)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review was not found'
            )
        
        review_model = self.convert_schema_to_model(review_schema)

        review.title=review_model.title
        review.score=review_model.score
        review.description=review_model.description

        try:
            new_review = await self.review_repository.update(review)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Invalid request body'
            )

        return ProductReviewSchema.model_validate(new_review)


    async def delete(self, review_id: UUID) -> None:
        review = await self.review_repository.find_by_id(review_id)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review was not found'
            )

        await self.review_repository.delete(review)


    @staticmethod
    def convert_schema_to_model(review_schema: SaveProductReviewSchema) -> ProductReview:
        return ProductReview(
            product_id=review_schema.product_id,
            title=review_schema.title,
            score=review_schema.score,
            description=review_schema.description
        )