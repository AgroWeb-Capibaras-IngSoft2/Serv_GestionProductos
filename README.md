# 🥕 Servicio de Gestión de Productos - AgroWeb

## 📖 Descripción General

Microservicio para gestión de productos agrícolas colombianos con **observabilidad integrada**. 
Permite registrar, consultar y listar productos con métricas en tiempo real de peticiones, latencia y errores.

## 🗂️ Estructura del Proyecto

```
Serv_GestionProductos/
├── app.py                          # Aplicación Flask con instrumentación
├── docker-compose.yml              # Cassandra + Prometheus + Grafana
├── requirements.txt                # Dependencias incluyendo observabilidad
├── generate_observability_demo.py  # Script de demostración de métricas
├── application/                    # Casos de uso del negocio
├── domain/                         # Entidades y repositorios
├── Infrastructure/                 # Adaptadores de BD
├── flask_interface/                # Endpoints HTTP
├── swagger/                        # Documentación API
└── observability/                  # Configuración de observabilidad
    ├── prometheus.yml              # Config de recolección de métricas
    ├── grafana-datasources/        # Conexión Prometheus-Grafana
    └── grafana-dashboards/         # Dashboard preconfigurado
```

## ✅ Requisitos

- **Runtime:** Python 3.8+ (recomendado: 3.11 con Anaconda/Miniconda)
- **Base de Datos:** Cassandra 4.0 (via Docker)
- **Observabilidad:** Prometheus, Grafana (via Docker)
- **Dependencias Python:** Flask, prometheus-flask-exporter, pandas, flasgger, cassandra-driver

### Instalación de Dependencias:
```bash
# OBLIGATORIO: Instalar Anaconda/Miniconda para compatibilidad con Cassandra
# Descargar de: https://docs.conda.io/en/latest/miniconda.html

# Crear entorno conda (REQUERIDO)
conda create -n agroweb python=3.11 -y
conda activate agroweb

# Instalar driver de Cassandra (SOLO funciona con conda)
conda install cassandra-driver -y

# Instalar otras dependencias
pip install -r requirements.txt
```

⚠️ **IMPORTANTE:** Este servicio **REQUIERE Anaconda/Miniconda** - no funcionará con pip nativo debido a incompatibilidades del cassandra-driver con Python 3.13.

## 🚀 Ejecución Paso a Paso

### Prerequisito: Configurar Entorno Python
```bash
# 1. OBLIGATORIO: Instalar Anaconda/Miniconda
# Descargar de: https://docs.conda.io/en/latest/miniconda.html

# 2. Crear y activar entorno (REQUERIDO)
conda create -n agroweb python=3.11 -y
conda activate agroweb

# 3. Instalar dependencias (orden importante)
conda install cassandra-driver -y
pip install -r requirements.txt

# 4. Verificar archivo de entorno existe
# Archivo .env ya configurado con USE_CASSANDRA=true
```

### 1. Iniciar Infraestructura (Base de Datos + Observabilidad)
```bash
# Iniciar Cassandra, Prometheus y Grafana
docker-compose up -d

# Verificar que estén ejecutándose
docker-compose ps

# Esperar que Cassandra esté listo (30-60 segundos)
docker-compose logs -f cassandra
# Buscar: "Listening for thrift clients..."
```

### 2. Iniciar API con Observabilidad
```bash
# IMPORTANTE: Usar Anaconda Prompt y activar entorno
conda activate agroweb

# Ejecutar API con métricas instrumentadas
python app.py
```

### 3. Verificar Servicios
- **API:** http://localhost:5000/apidocs (Swagger UI)
- **Health:** http://localhost:5000/health (Estado del servicio)
- **Métricas:** http://localhost:5000/metrics (Prometheus metrics)
- **Prometheus:** http://localhost:9090 (Query interface)
- **Grafana:** http://localhost:3001 (admin/agroweb2025)

## 📊 Observabilidad - Métricas Implementadas

### ¿Qué es la Observabilidad?
La **observabilidad** es la capacidad de entender el estado interno de un sistema basándose en los datos que produce. En AgroWeb, implementamos observabilidad usando **Prometheus** y **Grafana** para monitorear el rendimiento y salud de nuestros microservicios en tiempo real.

### 🔍 Prometheus - Recolección de Métricas
**Prometheus** es un sistema de monitoreo que:
- **Recolecta métricas** del API cada 5 segundos
- **Almacena datos** en una base de datos de series temporales
- **Consulta métricas** usando PromQL (Prometheus Query Language)
- **Detecta problemas** mediante reglas de alertas

#### Métricas que Prometheus Registra:
- **`agroweb_productos_requests_total`** - Contador de peticiones HTTP
  - Labels: method, endpoint, status
  - Ejemplo: POST /products → 201, GET /products → 200
- **`agroweb_productos_request_duration_seconds`** - Latencia de peticiones  
  - Labels: method, endpoint
  - Percentiles: 50, 95, 99 (tiempo de respuesta)
- **`flask_http_request_total`** - Métricas base de Flask
  - Peticiones totales por endpoint
- **`flask_http_request_duration_seconds`** - Histograma de duración
  - Distribución de tiempos de respuesta

### 📈 Grafana - Visualización de Datos
**Grafana** es una plataforma de visualización que:
- **Conecta a Prometheus** como fuente de datos
- **Crea dashboards** con gráficos en tiempo real
- **Muestra tendencias** y patrones de uso
- **Alerta automáticamente** cuando hay problemas

#### Dashboard "AgroWeb - Servicio de Productos":
- **📊 Peticiones por segundo** - Tráfico del API en tiempo real
- **⏱️ Latencia P95** - Tiempo de respuesta del 95% de peticiones
- **❌ Errores por código HTTP** - Monitoreo de errores 4xx/5xx
- **🎯 Distribución por endpoint** - Qué endpoints se usan más
- **Actualización:** Cada 5 segundos automáticamente

### 🔄 Flujo de Observabilidad:
```
API Flask → Genera métricas → Prometheus recolecta → Grafana visualiza
     ↓              ↓                    ↓                ↓
/products       requests_total      Series DB       Dashboard
/health         duration_seconds     PromQL          Alertas
```

### Demo de Observabilidad
```bash
# Generar tráfico automático para demostrar métricas en tiempo real
python generate_observability_demo.py

# El script genera 4 patrones de tráfico:
# 🌱 Tráfico normal (30 requests, 2 concurrent)  
# 🚀 Pico de tráfico (60 requests, 5 concurrent)
# 🐌 Tráfico lento (15 requests, 1 concurrent)
# 📈 Carga mixta (40 requests, 3 concurrent)

# Monitorear en tiempo real:
# - Prometheus: http://localhost:9090
# - Grafana Dashboard: http://localhost:3001
```

### Tests de Observabilidad
```bash
# Ejecutar tests automatizados para endpoints de monitoreo
python test_observability.py

# O usar pytest para testing más avanzado (requiere: pip install pytest)
pytest test_observability.py -v

# Los tests validan:
# ✅ Endpoint /health retorna JSON con formato correcto
# ✅ Endpoint /metrics expone métricas de Prometheus
# ✅ Códigos de respuesta HTTP correctos
# ✅ Estructura de datos esperada en las respuestas
```

## 📡 Endpoints de la API

### POST `/products` - Crear Producto
- **Descripción:** Crea un nuevo producto (productId se auto-genera)
- **Content-Type:** application/json
- **Campos requeridos:** name, category, price, unit, imageUrl, stock, origin, description
- **Campos opcionales:** isActive, originalPrice, isOrganic, isBestSeller, freeShipping
- **Respuestas:**
  - **201:** Producto creado exitosamente
  - **400:** Error de validación o datos incompletos
  - **415:** Content-Type no soportado
  - **500:** Error interno del servidor

### GET `/products` - Listar Productos
- **Descripción:** Obtiene todos los productos registrados
- **Respuestas:**
  - **200:** Lista de productos (array JSON)
  - **500:** Error interno del servidor

### GET `/products/<productId>` - Consultar Producto
- **Descripción:** Obtiene un producto específico por ID
- **Respuestas:**
  - **200:** Producto encontrado
  - **400:** ID inválido
  - **404:** Producto no encontrado
  - **500:** Error interno del servidor

### GET `/health` - Estado del Servicio
- **Descripción:** Endpoint de monitoreo para verificar salud del servicio
- **Respuestas:**
  - **200:** Servicio operativo con información de métricas

### GET `/metrics` - Métricas de Prometheus
- **Descripción:** Endpoint de métricas para observabilidad
- **Respuestas:**
  - **200:** Métricas en formato Prometheus

### GET `/test` - Test de Conectividad
- **Descripción:** Endpoint simple para verificar que el servicio responde
- **Respuestas:**
  - **200:** Servicio activo

## 🧪 Ejemplos de Uso

```bash
# Verificar estado del servicio
curl http://localhost:5000/health

# Ver métricas de observabilidad  
curl http://localhost:5000/metrics

# Crear producto (productId se auto-genera)
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Papa Pastusa", 
    "category": "vegetables", 
    "price": 1200.0,
    "unit": "1kg",
    "imageUrl": "http://localhost:5000/static/catalog/papa.jpg",
    "stock": 50,
    "origin": "Cundinamarca",
    "description": "Papa pastusa fresca de alta calidad",
    "isOrganic": true,
    "isBestSeller": false,
    "freeShipping": false
  }'

# Listar todos los productos
curl http://localhost:5000/products

# Consultar producto específico (usar ID retornado en creación)
curl http://localhost:5000/products/PROD-12345678
```

## 🔧 Configuración de Observabilidad

### Prometheus (puerto 9090)
- **Configuración:** `observability/prometheus.yml`
- **Target:** API nativo en `host.docker.internal:5000/metrics`
- **Scrape interval:** 5 segundos

### Grafana (puerto 3001)  
- **Credenciales:** admin/agroweb2025
- **Datasource:** Prometheus automáticamente configurado
- **Dashboard:** "AgroWeb - Servicio de Productos" pre-cargado

## 📄 Documentación API

Swagger UI disponible en: http://localhost:5000/apidocs

## � Monitoreo y Debugging

### Logs de la Aplicación
```bash
# El API muestra logs en tiempo real incluyendo:
# - Requests recibidos
# - Métricas generadas  
# - Errores de conexión
```

### Queries Útiles en Prometheus
```promql
# Tasa de peticiones por segundo
rate(flask_http_request_total[1m])

# Latencia percentil 95
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket[5m]))

# Errores HTTP 4xx y 5xx
flask_http_request_total{status=~"4..|5.."}
```

## 🛠️ Troubleshooting

| Problema | Solución |
|----------|----------|
| **API no responde** | Verificar `conda activate agroweb` y `python app.py` ejecutándose |
| **Error cassandra-driver** | Instalar con conda: `conda install cassandra-driver -y` |
| **Prometheus sin datos** | Comprobar `host.docker.internal:5000/metrics` accesible |
| **Grafana "datasource not found"** | Reiniciar contenedor: `docker-compose restart grafana` |
| **Error de dependencias** | Usar conda environment: `conda activate agroweb` |
| **Contenedores no inician** | Verificar Docker Desktop ejecutándose |
| **Puerto 5000 ocupado** | Cambiar puerto en app.py o cerrar proceso conflictivo |

## 📝 Notas Técnicas

- **Base de Datos:** Cassandra como backend principal con IDs auto-generados (formato: PROD-{UUID})
- **Fallback:** Sistema automático a pandas DataFrame si Cassandra no está disponible
- **Extensibilidad:** Arquitectura limpia preparada para escalabilidad
- **Observabilidad:** Métricas estándar de Prometheus integradas con refresh de 5 segundos
- **CORS:** Configurado para frontend en puerto 5173
- **Entorno:** REQUIERE Anaconda/Miniconda para compatibilidad con cassandra-driver
- **Auto-generación:** ProductId se genera automáticamente, no incluir en POST requests

### Configuración de Base de Datos
```bash
# Configuración por defecto en .env:
USE_CASSANDRA=true  # Cassandra como backend principal

# Beneficios del sistema actual:
# ✅ Base de datos escalable para producción
# ✅ IDs auto-generados UUID (más seguro que IDs manuales)
# ✅ CRUD completo implementado con validación robusta
# ✅ Fallback automático a pandas si Cassandra no disponible
# ✅ Observabilidad completa con métricas de rendimiento
```

### Comandos Docker Útiles
```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios  
docker-compose down

# Ver logs de Cassandra
docker-compose logs cassandra

# Acceder a CLI de Cassandra
docker exec -it agroweb-cassandra cqlsh

# Reiniciar solo Grafana
docker-compose restart grafana
```