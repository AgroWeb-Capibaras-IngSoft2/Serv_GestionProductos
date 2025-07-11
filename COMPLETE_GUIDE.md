# 🎯 Servicio de Productos - Guía Completa

## 📋 Resumen

Servicio de Gestión de Productos con Arquitectura Limpia, usando **Cassandra como base de datos principal** con IDs auto-generados para mayor seguridad y escalabilidad.

## ✅ Estado Actual del Servicio

**🎉 El servicio está completamente funcional y operativo**

- **Backend principal:** Cassandra (base de datos NoSQL escalable)
- **Pruebas:** 12/12 pasando ✅
- **API:** Completamente funcional en `http://localhost:5000`
- **Documentación:** Swagger UI disponible en `/swagger`
- **IDs de productos:** Auto-generados automáticamente (UUID)

### Configuración Actual
```bash
# En archivo .env:
USE_CASSANDRA=true  # Cassandra como backend principal

# Beneficios:
# ✅ Base de datos escalable para producción
# ✅ IDs auto-generados (más seguro)
# ✅ CRUD completo implementado
# ✅ Fallback automático a pandas si es necesario
```

## ⚠️ Nota Importante

**Este servicio requiere Anaconda Prompt** debido a la compatibilidad del driver de Cassandra con Python 3.13. Tus otros servicios en el proyecto pueden continuar usando terminal/símbolo del sistema regular como antes.

## 🚀 Configuración Rápida

### Paso 1: Instalar Miniconda (si no está instalado)
Descargar de: https://docs.conda.io/en/latest/miniconda.html

### Paso 2: Configurar Entorno (Anaconda Prompt)
```bash
# Crear entorno conda con Python 3.11
conda create -n agroweb python=3.11 -y
conda activate agroweb

# Navegar al directorio del servicio
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\Serv_GestionProductos"

# Instalar driver de Cassandra (conda requerido para compatibilidad)
conda install cassandra-driver -y

# Instalar otras dependencias
pip install -r requirements.txt

# Configurar entorno
copy .env.example .env
# Por defecto: USE_CASSANDRA=true (Cassandra como base de datos principal)

# Verificar instalación
python test_installation.py
```

### Paso 3: Instalar y Configurar Docker Desktop
```bash
# 1. Descargar e instalar Docker Desktop
# Desde: https://www.docker.com/products/docker-desktop
# Instalar y iniciar Docker Desktop - no requiere configuración adicional

# 2. Verificar instalación de Docker
docker --version
```

### Paso 4: Iniciar Base de Datos Cassandra con Docker
```bash
# Navegar a la raíz del proyecto
cd "d:\UN\2025-1\Ingesoft 2\Proyecto"

# Iniciar Cassandra (primera vez descargará la imagen)
docker-compose up -d

# Verificar que esté ejecutándose
docker-compose ps

# Esperar a que Cassandra esté listo (30-60 segundos)
# Verificar logs hasta ver: "Listening for thrift clients..."
docker-compose logs -f cassandra

# Probar conexión (debe funcionar después de 1-2 minutos)
docker exec -it agroweb-cassandra cqlsh
```

### Comandos Docker Útiles
```bash
# Iniciar Cassandra
docker-compose up -d

# Detener Cassandra
docker-compose down

# Ver logs
docker-compose logs cassandra

# Conectar a shell de Cassandra
docker exec -it agroweb-cassandra cqlsh

# Eliminar todo (para empezar de cero)
docker-compose down -v

# Verificar puertos disponibles
netstat -an | findstr 9042
```

### Paso 5: Iniciar Servicio (Anaconda Prompt)
```bash
# Siempre usar Anaconda Prompt para este servicio
conda activate agroweb
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\Serv_GestionProductos"
python app.py

# Servicio disponible en: http://localhost:5000
```

### Paso 6: Poblar Base de Datos y Probar (en Anaconda Prompt)
```bash
# IMPORTANTE: Ejecutar en Anaconda Prompt, no en CMD regular
conda activate agroweb

# Verificar instalación
python test_installation.py

# Poblar base de datos con datos de ejemplo
python populate_database.py

# Ejecutar pruebas completas
python test_products_clean.py

# O prueba manual rápida
curl http://localhost:5000/info
```

## 🗄️ Scripts de Base de Datos

### Poblar Base de Datos
```bash
# Limpiar y poblar con datos de ejemplo
python populate_database.py

# Esto creará 12 productos de ejemplo con IDs auto-generados
```

### Ejecutar Pruebas
```bash
# Pruebas completas del API
python test_products_clean.py

# Las pruebas ahora manejan IDs auto-generados correctamente
```

⚠️ **Recordatorio Importante:** 
- Siempre usar **Anaconda Prompt** para este servicio
- Activar el entorno: `conda activate agroweb`
- El servicio debe estar ejecutándose: `python app.py`

## 🔧 Flujo de Trabajo Multi-Servicio

### Este Servicio (Gestión de Productos)
```bash
# Siempre usar Anaconda Prompt para este servicio
conda activate agroweb
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\Serv_GestionProductos"
python app.py
# Se ejecuta en: http://localhost:5000
```

### Otros Servicios (Servicio de Usuarios, etc.)
```bash
# Usar terminal/símbolo del sistema regular como antes
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\Serv_Usuarios"
pip install -r requirements.txt  # si es necesario
python app.py
# Se ejecuta en: http://localhost:5001 (o tu puerto configurado)
```

### Frontend (sin cambios)
```bash
# Usar terminal regular como antes
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\FrontEnd"
npm run dev
# Se ejecuta en: http://localhost:3000
```

### Base de Datos (compartida)
```bash
# Iniciar una vez para todos los servicios
cd "d:\UN\2025-1\Ingesoft 2\Proyecto"
docker-compose up -d
```

## 🧪 Pruebas

### Pruebas Automatizadas
```bash
# Ejecutar suite completo de pruebas
python test_products_clean.py

# Salida esperada:
# ✅ Servidor accesible
# ✅ Producto creado: Test Lechuga
# ✅ Recuperados 5 productos
# 🎉 ¡Todas las pruebas pasaron!
```

### Ejemplos de Pruebas Manuales
```bash
# Crear un producto de prueba (ID se genera automáticamente)
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tomate de Prueba",
    "category": "vegetables",
    "price": 3000,
    "unit": "kg",
    "imageUrl": "http://localhost:5000/static/catalog/tomato.jpg",
    "stock": 50,
    "origin": "Colombia",
    "description": "Tomate fresco para pruebas",
    "isActive": true
  }'

# Verificar creación (usar el ID devuelto en la respuesta)
curl http://localhost:5000/products/{id-generado}

# Probar filtro por categoría
curl http://localhost:5000/products/category/vegetables

# Probar productos activos
curl http://localhost:5000/products/active

# Poblar base de datos con datos de ejemplo
python populate_database.py
```

## 🔧 Solución de Problemas

### Errores 500 en las Pruebas
```bash
# 1. Asegúrate de usar Anaconda Prompt
# Abrir Anaconda Prompt (no CMD regular)
conda activate agroweb

# 2. Verificar que el servicio esté ejecutándose
# En una ventana de Anaconda Prompt:
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\Serv_GestionProductos"
python app.py

# 3. En otra ventana de Anaconda Prompt, ejecutar las pruebas:
conda activate agroweb
cd "d:\UN\2025-1\Ingesoft 2\Proyecto\Serv_GestionProductos"
python test_products_clean.py
```

### Problemas de Instalación
```bash
# Probar tu instalación
python test_installation.py

# Si el driver de Cassandra falla, el servicio usa automáticamente fallback a pandas
# Esto es normal y esperado para desarrollo
```

### Problemas con Docker y Cassandra
```bash
# Verificar que Docker esté ejecutándose
docker --version

# Verificar si Cassandra no inicia
netstat -an | findstr 9042

# Reiniciar con datos limpios
docker-compose down -v
docker-compose up -d

# Verificar logs de Cassandra
docker-compose logs cassandra | findstr "Listening"

# Probar conexión a Cassandra
docker exec -it agroweb-cassandra cqlsh -e "describe cluster"
```

### Problemas del Servicio
```bash
# Verificar si el puerto 5000 está disponible
netstat -an | findstr 5000

# Verificar si Cassandra está ejecutándose
docker ps | grep cassandra

# Reiniciar Cassandra si es necesario
docker-compose restart cassandra

# Verificar que Cassandra esté completamente iniciado
docker-compose logs cassandra | findstr "Listening for thrift clients"
```

### Variables de Entorno
Asegúrate de que tu archivo `.env` tenga:
```bash
USE_CASSANDRA=true
CASSANDRA_HOSTS=127.0.0.1
CASSANDRA_PORT=9042
CASSANDRA_KEYSPACE=productos_db
```

## 📊 Beneficios Clave

### Configuración con Docker
- ✅ **Sin instalación compleja de Cassandra**
- ✅ **Tu flujo de trabajo Python/React permanece igual**
- ✅ **Base de datos persiste entre reinicios**
- ✅ **Fácil de remover cuando termine**
- ✅ **Misma configuración funciona en cualquier computadora**

### Experiencia del Desarrollador
- **Configuración Simple**: Configuración de entorno conda de una sola vez
- **Separación Clara**: Solo este servicio requiere Anaconda Prompt
- **Fallback Automático**: Fallback a pandas si Cassandra no está disponible
- **Pruebas Fáciles**: Suite completo de pruebas

### Listo para Producción
- **Escalable**: Cassandra para producción de alto rendimiento
- **Arquitectura Limpia**: Separación apropiada de capas
- **Manejo de Errores**: Mecanismos robustos de fallback
- **Documentación**: Documentación completa de la API vía Swagger

---

## 📞 Referencia Rápida

- **URL del Servicio**: `http://localhost:5000`
- **Documentación API**: `http://localhost:5000/swagger`
- **Verificación de Salud**: `http://localhost:5000/health`
- **Suite de Pruebas**: `python test_products_clean.py`

**🎉 ¡Tu Servicio de Gestión de Productos está listo para desarrollo y producción!**
