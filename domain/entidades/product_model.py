from dataclasses import dataclass, field
from datetime import datetime, date
import uuid

@dataclass
class Product:
    # Campos requeridos en el input - Deben proporcionarse al crear un producto
    name: str              # Nombre del producto
    category: str          # Categoría del producto (ej: "Vegetales", "Frutas")
    price: float           # Precio de venta actual
    unit: str              # Unidad de medida (ej: "kg", "lb", "unidad")
    imageUrl: str          # URL de la imagen del producto
    stock: int             # Cantidad en inventario actual
    origin: str            # Lugar de origen (ej: "Boyacá", "Valle del Cauca")
    description: str       # Descripción del producto
    
    # Campos opcionales en el input - Pueden proporcionarse, usarán valor por defecto si no
    originalPrice: float = None    # Precio original antes de descuentos
    isActive: bool = True          # Si el producto está activo en el catálogo
    isOrganic: bool = None         # Si el producto tiene certificación orgánica
    freeShipping: bool = False     # Si el producto califica para envío gratuito

    # Campos opcionales al hacer update - Pueden proporcionarse, usarán valor por defecto si no
    isBestSeller: bool = None      # Se actualiza según rendimiento de ventas
    
    # Campos por defecto, generados - Se establecen automáticamente, no se esperan como input
    productId: str = field(default_factory=lambda: f"PROD-{str(uuid.uuid4())[:8].upper()}")  # Auto-generated unique ID
    createdAt: date = field(default_factory=lambda: datetime.now().date())    # Marca de tiempo de creación
    updatedAt: date = field(default_factory=lambda: datetime.now().date())    # Marca de tiempo de última actualización
    inStock: bool = field(init=False, default=None)                           # Calculado desde stock > 0

    def __post_init__(self):
        # Convert dates if needed
        if isinstance(self.createdAt, str):
            self.createdAt = datetime.fromisoformat(self.createdAt).date()
        if isinstance(self.updatedAt, str):
            self.updatedAt = datetime.fromisoformat(self.updatedAt).date()
        
        # Calculate inStock based on stock availability
        self.inStock = self.stock > 0
        
        # Validations
        if self.price < 0:
            raise ValueError("El precio no puede ser negativo")
        if self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
        if not self.name:
            raise ValueError("El nombre es obligatorio")
        if not self.unit:
            raise ValueError("La unidad de medida es obligatoria")
        if not self.origin:
            raise ValueError("El origen es obligatorio")
        if not self.imageUrl:
            raise ValueError("La URL de la imagen es obligatoria")

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