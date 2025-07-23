from domain.repositorio.product_repo import ProductRepository
from Infrastructure.cassandra_db import CassandraDB
from domain.entidades.product_model import Product

class AdapterProductRepo(ProductRepository):
    def __init__(self):
        self.database = CassandraDB()

    def add_product(self, product: Product):
        self.database.add_product(product)
        return product

    def get_product_by_id(self, product_id: str):
        data = self.database.get_product_by_id(product_id)
        if data and "inStock" in data:
            del data["inStock"]
        try:
            return Product(**data) if data else None
        except Exception as e:
            return None

    def get_all_products(self):
        import math
        import logging
        logger = logging.getLogger(__name__)
        def clean(prod):
            prod = dict(prod)
            prod.pop("inStock", None)
            for k, v in prod.items():
                if isinstance(v, float) and math.isnan(v):
                    prod[k] = None
                if v == "NaT":
                    prod[k] = None
            return prod

        cleaned_products = []
        for prod in self.database.get_all_products():
            try:
                cleaned = clean(prod)
                logger.debug(f"Attempting to create Product with: {cleaned}")
                p = Product(**cleaned)
                cleaned_products.append(p)
            except Exception as e:
                logger.error(f"Skipping product due to error: {e}. Data: {cleaned}")
                continue
        logger.info(f"Total products returned: {len(cleaned_products)}")
        return cleaned_products
    
    def get_products_by_user_id(self, user_id: str):
        import math
        def clean(prod):
            prod = dict(prod)
            prod.pop("inStock", None)
            for k, v in prod.items():
                if isinstance(v, float) and math.isnan(v):
                    prod[k] = None
                if v == "NaT":
                    prod[k] = None
            return prod

        cleaned_products = []
        for prod in self.database.get_products_by_user_id(user_id):
            try:
                cleaned = clean(prod)
                p = Product(**cleaned)
                cleaned_products.append(p)
            except Exception as e:
                # Skip invalid products and continue processing
                continue
        return cleaned_products
    
    def update_image_url(self, product_id, image_url):
        self.database.update_image_url(product_id, image_url)