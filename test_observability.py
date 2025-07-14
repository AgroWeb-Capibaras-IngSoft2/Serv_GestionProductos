"""
Tests para endpoints de observabilidad del servicio de productos
"""
import requests
import json
import pytest
from unittest.mock import patch

# Base URL del servicio
BASE_URL = "http://localhost:5000"

def test_health_endpoint_response_format():
    """Test que el endpoint /health retorna formato JSON correcto con status 200"""
    try:
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
        
        print("✅ Health endpoint test passed")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint test failed - Connection error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Health endpoint test failed - Invalid JSON: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Health endpoint test failed - Assertion error: {e}")
        return False
    except Exception as e:
        print(f"❌ Health endpoint test failed - Unexpected error: {e}")
        return False

def test_metrics_endpoint_availability():
    """Test que el endpoint /metrics está disponible y retorna métricas de Prometheus"""
    try:
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
        
        print("✅ Metrics endpoint test passed")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Metrics endpoint test failed - Connection error: {e}")
        return False
    except AssertionError as e:
        print(f"❌ Metrics endpoint test failed - Assertion error: {e}")
        return False
    except Exception as e:
        print(f"❌ Metrics endpoint test failed - Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Ejecutando tests de observabilidad...")
    print("=" * 50)
    
    # Ejecutar tests
    health_result = test_health_endpoint_response_format()
    metrics_result = test_metrics_endpoint_availability()
    
    print("=" * 50)
    if health_result and metrics_result:
        print("🎉 Todos los tests de observabilidad pasaron correctamente")
    else:
        print("⚠️ Algunos tests fallaron - revisar logs anteriores")
        print("💡 Asegúrate de que el servicio esté ejecutándose en http://localhost:5000")
