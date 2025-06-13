from domain.repositorio.product_repo import ProductRepository
from dataclasses import dataclass

@dataclass
class GetProductByIdService:
    repo: ProductRepository

    def execute(self, product_id: str):
        product = self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        return product