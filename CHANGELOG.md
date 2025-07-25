# CHANGELOG
## [1.2.4] - 2025-07-23
### Fixed
- **Manejo de imágenes en registro de productos:** Se corrigió el flujo de subida y almacenamiento de imágenes, asegurando que la imagen se guarde con el nombre basado en el productId y se actualice correctamente el campo imageUrl en la base de datos.
- **Validación de tipos en backend:** Se corrigió la conversión de los campos `stock` y `price` a enteros y flotantes respectivamente antes de crear el producto, evitando errores de comparación de tipos.

### Changed
- **Integración con Serv_Usuarios:** Se mejoró la validación de existencia de usuario antes de registrar un producto, asegurando la consistencia de los datos y la comunicación entre microservicios.

### Improved
- **Experiencia de usuario:** Se mejoró la respuesta de error y éxito en el registro de productos, mostrando mensajes más claros en el frontend.

## [1.2.3] - 2025-07-22
### Fixed
- **Validación de categorías:** Se corrigieron los valores de categoría en los datos de prueba y en la validación del backend para aceptar únicamente las categorías válidas como (`vegetales`, `frutas`, `lácteos`, `hierbas`).
- **Edge cases de productos:** Se ajustaron los tests y la lógica de creación para manejar correctamente productos con datos límite o inusuales.
- **Endpoint `/products/user/<user_id>`:** Se corrigió un error 500 al consultar productos por usuario, asegurando manejo robusto de datos y respuestas.
- **Consistencia de nombres de campos:** Se revisó y unificó el uso de `user_id` en todo el flujo de productos y validaciones.

### Improved
- **Rendimiento bajo carga:** Se optimizó el manejo de errores y la respuesta de endpoints críticos para mejorar el throughput y la latencia en escenarios de carga y error.
- **Documentación:** Se actualizaron los ejemplos y la documentación Swagger para reflejar los valores válidos de categoría y los cambios en los endpoints.
- **Cobertura de pruebas:** Se ampliaron y corrigieron los tests de integración para cubrir casos límite y asegurar la estabilidad del servicio.

---
## [1.2.2] - 2025-07-21
### Fixed
- **Hotfix de integración con Serv_Usuarios:**
  - Se corrigieron referencias al servicio de usuarios para la validación de existencia antes de registrar un producto.
  - Se ajustó el uso de `user_id` en vez de `UserId` en las llamadas y validaciones.
  - Se corrigió el puerto de referencia del microservicio de usuarios, cambiando de 5000 a 5001 en las llamadas HTTP.

## [1.2.1] - 2025-07-20
### Added
- **Campo `user_id`** añadido al modelo de productos para asociar cada producto al usuario que lo registró.
- **Endpoint `/products/byUser/<user_id>`** para consultar productos por usuario asociado.

### Changed
- **Índice secundario**: Se eliminó el índice por categoría y se añadió índice secundario por `user_id` en Cassandra para optimizar búsquedas por usuario.
- **Búsqueda de productos**: El endpoint `/products` ahora retorna únicamente productos activos (`isActive = true`), alineado con el catálogo del frontend.
- **Observabilidad Prometheus**: La integración con Prometheus ahora es nativa en Python, sin depender de Docker ni de Grafana. Las métricas se consultan directamente en el endpoint `/metrics`.
- **Documentación y ejemplos**: Actualizados para reflejar los cambios en la estructura del modelo y la observabilidad.

### Removed
- **Índice por categoría** en Cassandra (el filtrado por categoría se realiza en el frontend).
- **Grafana**: Ya no se utiliza para dashboards de métricas en este servicio.
- **Prometheus en Docker**: La recolección de métricas se realiza directamente desde el servicio Python.

### Fixed
- **Validación de usuario**: Se verifica que el usuario exista antes de registrar un producto.
- **Consistencia de datos**: El filtrado por productos activos está correctamente implementado en el backend.

---

## [1.2.0] - 2025-07-13
### Added
- **Observabilidad integrada** con Prometheus y Grafana para monitoreo en tiempo real
- **Docker Compose** completo con Cassandra, Prometheus y Grafana orchestration
- **Auto-generación de productId** usando UUID para mayor seguridad y escalabilidad
- **Instrumentación de métricas** con prometheus-flask-exporter para análisis de rendimiento
- **Dashboard preconfigurado** en Grafana "AgroWeb - Servicio de Productos"
- **Script de demostración** `generate_observability_demo.py` para testing de métricas
- **Endpoints de observabilidad**: `/health` y `/metrics` para monitoreo
- **Tests automatizados** `test_observability.py` para validación de endpoints de monitoreo

### Changed
- **Arquitectura de datos**: ProductId ahora se auto-genera en lugar de ser requerido en requests
- **Integración completa de infraestructura**: Cassandra, Prometheus y Grafana unificados en el servicio
- **Configuración de entorno**: Mandatory Anaconda/conda para compatibilidad con cassandra-driver
- **Validación de API**: Campos requeridos actualizados para reflejar auto-generación de IDs
- **Documentación README**: Completamente reescrita con guías de observabilidad y troubleshooting

### Removed
- **Dependencia de infrastructure externa**: Todo integrado dentro del servicio productos
- **IDs manuales**: ProductId ya no se requiere en POST requests (auto-generado)

### Fixed
- **Instrumentación de Flask**: Métricas de latencia, throughput y error rates funcionando correctamente
- **Conectividad Docker**: Networking entre contenedores configurado apropiadamente
- **Fallback de base de datos**: Sistema robusto de fallback pandas si Cassandra no está disponible
- **Error handling en adaptador**: Productos inválidos se omiten en lugar de detener el procesamiento
- **Cálculo de inStock**: Campo se calcula automáticamente desde stock > 0 en __post_init__
- **Endpoints de demo**: Removidos endpoints inválidos de filtrado por categoría (se hace en frontend)

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
- Validación de campos