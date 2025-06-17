from dataclasses import dataclass, field
from datetime import date, datetime

@dataclass
class Product:
    productId: str
    name: str
    description: str
    category: str
    price: float
    stock: int
    unit: str         # Unidad de medida (ej: kg, bulto, caja)
    origin: str       # Origen (ej: municipio, departamento)
    imageUrl: str
    createdAt: date = field(default_factory=lambda: datetime.now().date())
    updatedAt: date = field(default_factory=lambda: datetime.now().date())
    isActive: bool = True

    def __post_init__(self):
        if isinstance(self.createdAt, str):
            self.createdAt = datetime.fromisoformat(self.createdAt).date()
        if isinstance(self.updatedAt, str):
            self.updatedAt = datetime.fromisoformat(self.updatedAt).date()
        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name:
            raise ValueError("El nombre es obligatorio")
        if not self.productId:
            raise ValueError("El ID es obligatorio")
        if not self.unit:
            raise ValueError("La unidad de medida es obligatoria")
        if not self.origin:
            raise ValueError("El origen es obligatorio")
        if not self.imageUrl:
            raise ValueError("La URL de la imagen es obligatoria")

    def toDictionary(self) -> dict:
        return {
            "productId": self.productId,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "unit": self.unit,
            "origin": self.origin,
            "imageUrl": self.imageUrl,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
            "isActive": self.isActive,
        }