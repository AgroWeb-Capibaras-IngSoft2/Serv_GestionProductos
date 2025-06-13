from domain.repositorio.product_repo import ProductRepository
from Infrastructure.DB import db
from domain.entidades.product_model import Product

class AdapterProductRepo(ProductRepository):
    def __init__(self):
        self.database = db()

    def add_product(self, product: Product):
        self.database.add_product(product)
        return product

    def get_product_by_id(self, product_id: str):
        data = self.database.get_product_by_id(product_id)
        return Product(**data) if data else None

    def get_all_products(self):
        return [Product(**prod) for prod in self.database.get_all_products()]
    