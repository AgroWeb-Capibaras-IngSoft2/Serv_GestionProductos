from dataclasses import dataclass, field
from datetime import datetime, date

@dataclass
class Product:
    productId: str
    name: str
    category: str
    price: float
    unit: str
    imageUrl: str
    stock: int
    origin: str
    description: str
    originalPrice: float = None
    createdAt: date = field(default_factory=lambda: datetime.now().date())
    updatedAt: date = field(default_factory=lambda: datetime.now().date())
    isActive: bool = True
    isOrganic: bool = None
    isBestSeller: bool = None
    freeShipping: bool = False
    # inStock is not expected as input!
    inStock: bool = field(init=False, default=None)

    def __post_init__(self):
        # Convert dates if needed
        if isinstance(self.createdAt, str):
            self.createdAt = datetime.fromisoformat(self.createdAt).date()
        if isinstance(self.updatedAt, str):
            self.updatedAt = datetime.fromisoformat(self.updatedAt).date()
        # Validations
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
        # Always calculate inStock
        self.inStock = self.stock > 0

    def toDictionary(self):
        from math import isnan
        def clean(val):
            try:
                if isinstance(val, float) and isnan(val):
                    return None
            except:
                pass
            if hasattr(val, 'isoformat'):
                return val.isoformat()
            return val
        return {
            "productId": self.productId,
            "name": self.name,
            "category": self.category,
            "price": clean(self.price),
            "unit": self.unit,
            "imageUrl": self.imageUrl,
            "stock": clean(self.stock),
            "origin": self.origin,
            "description": self.description,
            "isActive": self.isActive,
            "originalPrice": clean(self.originalPrice),
            "isOrganic": self.isOrganic,
            "isBestSeller": self.isBestSeller,
            "freeShipping": self.freeShipping,
            "createdAt": clean(self.createdAt),
            "updatedAt": clean(self.updatedAt),
            "inStock": self.inStock,
        }