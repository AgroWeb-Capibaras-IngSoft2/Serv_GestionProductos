from domain.repositorio.product_repo import ProductRepository
from domain.entidades.product_model import Product
from dataclasses import dataclass
from typing import Dict

@dataclass
class CreateProductService:
    repo: ProductRepository

    def execute(self, data: Dict) -> Product:
        product = Product(**data)
        self.repo.add_product(product)
        return product