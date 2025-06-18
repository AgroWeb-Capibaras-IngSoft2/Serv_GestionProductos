# 🥕 Servicio de Gestión de Productos - AgroWeb

---

## 📖 Descripción General

Este microservicio permite la gestión de productos del agro colombiano, permitiendo registrar, consultar y listar productos con información relevante como nombre, categoría, origen, unidad de medida, precio, stock, URL de imagen y atributos adicionales como si es orgánico, más vendido, envío gratis, precio original y disponibilidad (`inStock`). Está diseñado bajo principios de arquitectura limpia y es fácilmente extensible para futuras integraciones (por ejemplo, bases de datos o autenticación).

---

## 🗂️ Estructura del Servicio

```
Serv_GestionProductos/
├── app.py
├── test_products.py
├── README.md
├── CHANGELOG.md
├── swagger/
│   └── swagger.yaml
├── application/
│   └── useCases/
│       ├── CreateProductService.py
│       ├── GetAllProductsService.py
│       └── GetProductByIdService.py
├── domain/
│   ├── entidades/
│   │   └── product_model.py
│   └── repositorio/
│       └── product_repo.py
├── Infrastructure/
│   ├── DB.py
│   └── adapterProductRepo.py
└── flask_interface/
    └── routes.py
```

---

## ✅ Requisitos

- Python 3.8+
- Flask
- pandas
- requests (solo para pruebas locales)
- flasgger (para documentación Swagger en `/apidocs`)
- flask-cors (si usas frontend separado)

Instala dependencias con:
```
pip install flask pandas requests flasgger flask-cors
```

---

## 📄 Instrucciones de Instalación

1. Clona el repositorio o descarga el código.
2. Instala las dependencias.
3. Ejecuta el microservicio:
   ```
   python app.py
   ```
4. (Opcional) Ejecuta el script de pruebas:
   ```
   python test_products.py
   ```
5. Accede a la documentación Swagger en:  
   [http://localhost:5000/apidocs](http://localhost:5000/apidocs)

---

## 📡 Endpoints de la API

### POST `/products`
- **201**: Producto creado exitosamente.
- **400**: Error de validación o datos incompletos.
- **415**: Content-Type no soportado.
- **500**: Error interno del servidor.

### GET `/products`
- **200**: Lista de productos.
- **500**: Error interno del servidor.

### GET `/products/<productId>`
- **200**: Producto encontrado.
- **400**: ID inválido.
- **404**: Producto no encontrado.
- **500**: Error interno del servidor.

### GET `/test`
- **200**: Servicio activo.
- **500**: Error interno del servidor.

---

## 🧪 Ejemplos de Pruebas (curl)

```sh
# Crear producto (incluye todos los campos relevantes)
curl -X POST http://localhost:5000/products -H "Content-Type: application/json" -d "{\"productId\": \"P001\", \"name\": \"Papa Pastusa\", \"description\": \"Papa de excelente calidad\", \"category\": \"Tubérculo\", \"price\": 1200.0, \"stock\": 100, \"unit\": \"kg\", \"origin\": \"Boyacá\", \"imageUrl\": \"https://example.com/images/papa.jpg\", \"isOrganic\": true, \"isBestSeller\": false, \"freeShipping\": false, \"originalPrice\": 1500.0}"

# Listar todos los productos
curl -X GET http://localhost:5000/products

# Consultar producto por ID
curl -X GET http://localhost:5000/products/P001

# Ruta de prueba
curl -X GET http://localhost:5000/test
```

---

## 📄 Documentación Swagger

La documentación OpenAPI/Swagger está disponible en el archivo [`swagger/swagger.yaml`](swagger/swagger.yaml) y en [http://localhost:5000/apidocs](http://localhost:5000/apidocs).

---

## 📝 Notas

- Los datos se almacenan en memoria usando pandas DataFrame (no persistentes).
- El campo `imageUrl` permite que el frontend muestre imágenes de los productos (puede ser URL externa o base64).
- El campo `inStock` es calculado automáticamente a partir del stock.
- El servicio está preparado para ser extendido a una base de datos real en el futuro.
- El código sigue principios de arquitectura limpia para facilitar el mantenimiento y la escalabilidad.
- Todos los endpoints devuelven respuestas informativas y en formato JSON para errores comunes (400, 404, 415, 500).
- El frontend ahora consume los productos directamente desde la API, eliminando datos estáticos.

---

## Historial de Cambios

[Ver historial de cambios (CHANGELOG.md)](CHANGELOG.md)

---