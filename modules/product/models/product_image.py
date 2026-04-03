from infrastructure.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Enum, ForeignKey, Index, text
from sqlalchemy.orm import relationship

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    image_url = Column("image_url", String, nullable=False)
    image_type = Column("image_type", Enum("main", "gallery", "description", name="image_type_enum"), nullable=False)
    position = Column(Integer, default=0)

    product = relationship(
        "Product",
        back_populates="images"
    )

    __table_args__ = (
        Index("idx_product_images_product_position", "product_id", "position"),
    )

    def __init__(self, product_id, image_url, image_type, position=0):
        self.product_id = product_id
        self.image_url = image_url
        self.image_type = image_type
        self.position = position