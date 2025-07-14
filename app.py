from flask import Flask, jsonify, request
from flask_interface.routes import bp
from flasgger import Swagger
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import os

app = Flask(__name__, static_folder='static')

# OBSERVABILIDAD: Configuración de métricas con Prometheus
metrics = PrometheusMetrics(app)

# Métricas de información del servicio
metrics.info('agroweb_productos_info', 'Servicio de Gestión de Productos AgroWeb', version='1.2.0')

# Contador de peticiones HTTP (con método, endpoint y código de estado)
request_count = metrics.counter(
    'agroweb_productos_requests_total', 
    'Total de peticiones al servicio de productos',
    labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint, 'status': lambda r: r.status_code}
)

# Histograma de latencia/duración de peticiones
request_duration = metrics.histogram(
    'agroweb_productos_request_duration_seconds',
    'Duración de peticiones en segundos',
    labels={'method': lambda: request.method, 'endpoint': lambda: request.endpoint}
)

swagger = Swagger(app, template_file='swagger/swagger.yaml')
CORS(app, origins=["http://localhost:5173"])
app.register_blueprint(bp)

# Manejadores de errores HTTP
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error.description) if hasattr(error, "description") else "Solicitud incorrecta"}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({"error": "Content-Type must be application/json"}), 415

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

# Endpoint de salud para monitoreo y observabilidad
@app.route('/health')
def health():
    """Health check endpoint para verificar estado del servicio"""
    return jsonify({
        'status': 'healthy',
        'service': 'productos',
        'version': '1.2.0',
        'metrics_endpoint': '/metrics'
    })

if __name__ == "__main__":
    print("🔧 Iniciando configuración de Flask...")
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print("🌱 Servicio de Productos AgroWeb iniciado")
    print("📋 API Documentation: http://127.0.0.1:5000/apidocs")
    print("🏥 Health Check: http://127.0.0.1:5000/health")
    print("📊 Métricas Prometheus: http://127.0.0.1:5000/metrics")
    print("🚀 Iniciando servidor en puerto 5000...")
    print("=" * 50)
    print("✅ SERVIDOR LISTO - Esperando conexiones HTTP...")
    print("=" * 50)
    app.run(debug=debug_mode, port=5000, host="127.0.0.1")
