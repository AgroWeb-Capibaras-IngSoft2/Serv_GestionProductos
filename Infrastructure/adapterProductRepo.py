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
        return Product(**data) if data else None

    def get_all_products(self):
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
        for prod in self.database.get_all_products():
            try:
                cleaned = clean(prod)
                p = Product(**cleaned)
                cleaned_products.append(p)
            except Exception as e:
                # Skip invalid products and continue processing
                continue
        return cleaned_products