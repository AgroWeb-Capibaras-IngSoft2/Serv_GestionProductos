from domain.repositorio.product_repo import ProductRepository
from dataclasses import dataclass

@dataclass
class GetAllProductsService:
    repo: ProductRepository

    def execute(self):
        return self.repo.get_all_products()