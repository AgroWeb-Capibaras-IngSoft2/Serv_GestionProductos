"""
Tests para endpoints de observabilidad del servicio de productos
"""
import requests
import json
from unittest.mock import patch

# Base URL del servicio
BASE_URL = "http://localhost:5000"

def test_health_endpoint_response_format():
    """Test que el endpoint /health retorna formato JSON correcto con status 200"""
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    
    # Verificar código de respuesta
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Verificar que es JSON válido
    data = response.json()
    
    # Verificar estructura esperada
    required_fields = ['status', 'service', 'version', 'metrics_endpoint']
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
    
    # Verificar valores específicos
    assert data['status'] == 'healthy', f"Expected status 'healthy', got {data['status']}"
    assert data['service'] == 'productos', f"Expected service 'productos', got {data['service']}"
    assert data['version'] == '1.2.0', f"Expected version '1.2.0', got {data['version']}"
    assert data['metrics_endpoint'] == '/metrics', f"Expected metrics_endpoint '/metrics', got {data['metrics_endpoint']}"

def test_metrics_endpoint_availability():
    """Test que el endpoint /metrics está disponible y retorna métricas de Prometheus"""
    response = requests.get(f"{BASE_URL}/metrics", timeout=5)
    
    # Verificar código de respuesta
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    # Verificar que contiene métricas esperadas
    content = response.text
    expected_metrics = [
        'agroweb_productos_info',
        'flask_http_requests_total',
        'flask_http_request_duration_seconds'
    ]
    
    for metric in expected_metrics:
        assert metric in content, f"Expected metric '{metric}' not found in response"

if __name__ == "__main__":
    print("🧪 Ejecutando tests de observabilidad...")
    print("=" * 50)
    
    # Ejecutar tests individuales con manejo de excepciones para el modo standalone
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Health endpoint
    try:
        test_health_endpoint_response_format()
        print("✅ Health endpoint test passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")
    
    # Test 2: Metrics endpoint  
    try:
        test_metrics_endpoint_availability()
        print("✅ Metrics endpoint test passed")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Metrics endpoint test failed: {e}")
    
    print("=" * 50)
    if tests_passed == total_tests:
        print("🎉 Todos los tests de observabilidad pasaron correctamente")
    else:
        print(f"⚠️ {tests_passed}/{total_tests} tests pasaron - revisar errores anteriores")
        print("💡 Asegúrate de que el servicio esté ejecutándose en http://localhost:5000")
