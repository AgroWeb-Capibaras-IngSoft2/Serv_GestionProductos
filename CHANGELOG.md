# CHANGELOG

## [1.1.0] - 2025-06-18
### Changed
- Actualización y corrección de la documentación Swagger del servicio de productos para reflejar la estructura real de los productos y los endpoints.
- Ejemplos de Swagger ahora incluyen todos los campos relevantes (`isOrganic`, `isBestSeller`, `freeShipping`, `inStock`, etc.) en las respuestas y peticiones.
- Ajuste en la lógica del backend para calcular correctamente el campo `inStock` a partir de `stock`.
- Integración frontend-backend para que el catálogo consuma productos dinámicamente desde el backend y muestre correctamente los datos e imágenes.
- Eliminación de datos estáticos en el frontend y uso exclusivo de la API de productos.
- Documentación y ejemplos actualizados para recomendar el uso de URLs absolutas en el campo `imageUrl` para integración robusta con el frontend.

## [1.0.1] - 2025-06-16
### Added
- Campo `imageUrl` para integración con frontend.
- Script de pruebas automatizadas.
- Documentación Swagger y README.

## [1.0.0] - 2025-06-12
### Added
- Estructura inicial del microservicio de productos agrocolombianos.
- Endpoints para crear, listar y consultar productos.
- Validación de campos obligatorios.