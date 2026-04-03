from infrastructure.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index, CheckConstraint, text
from sqlalchemy.orm import relationship

class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    title = Column("title", String(50), nullable=False)
    score = Column("score", Integer, nullable=False)
    description = Column("description", Text)

    product = relationship(
        "Product",
        back_populates="reviews"
    )

    __table_args__ = (
        Index("idx_product_reviews_product_id", "product_id"),
        CheckConstraint("score >= 1 AND score <= 10", name="check_score_range"),
    )

    def __init__(self, product_id, title, score, description):
        self.product_id = product_id
        self.title = title
        self.score = score
        self.description = description