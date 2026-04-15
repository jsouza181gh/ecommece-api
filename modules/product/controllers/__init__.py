from .product_category import router as category_router
from .product import router as product_router

routers = [
    category_router,
    product_router
]