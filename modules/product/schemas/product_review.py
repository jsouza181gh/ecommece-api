from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from uuid import UUID

class SaveProductReviewSchema(BaseModel):
    product_id: UUID
    title: Optional[str]
    score: int
    description: Optional[str]


class ProductReviewSchema(BaseModel):
    id: UUID
    product_id: UUID
    title: Optional[str]
    score: int
    description: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)