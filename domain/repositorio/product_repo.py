from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entidades.product_model import Product

class ProductRepository(ABC):
    @abstractmethod
    def add_product(self, product: Product) -> Product:
        pass

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass
