import pandas as pd
from domain.entidades.product_model import Product

class db:
    def __init__(self):
        self.dataBase = pd.DataFrame(columns=[
            "productId", "name", "description", "category", "price", "stock", "unit", "origin",
            "imageUrl", "createdAt", "updatedAt", "isActive"
        ])

    def add_product(self, product: Product):
        if not self.dataBase[self.dataBase["productId"] == product.productId].empty:
            raise ValueError("Ya existe un producto con ese ID")
        self.dataBase = pd.concat([
            self.dataBase,
            pd.DataFrame([product.toDictionary()])
        ], ignore_index=True)

    def get_product_by_id(self, product_id: str):
        result = self.dataBase[self.dataBase["productId"] == product_id]
        return result.iloc[0].to_dict() if not result.empty else None

    def get_all_products(self):
        return self.dataBase.to_dict(orient="records")