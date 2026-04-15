from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SaveProductCategorySchema(BaseModel):
    name: str

class ProductCategorySchema(BaseModel):
    id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)