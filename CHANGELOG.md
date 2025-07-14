# CHANGELOG

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
- Validación de campos obligatorios.