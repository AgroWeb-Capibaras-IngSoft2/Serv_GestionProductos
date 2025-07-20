from domain.repositorio.product_repo import ProductRepository
from dataclasses import dataclass

@dataclass
class GetProductsByUserIDService:
    repo: ProductRepository

    def execute(self):
        return self.repo.get_products_by_user_id(self.user_id)