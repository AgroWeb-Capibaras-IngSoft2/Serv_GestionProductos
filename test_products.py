import requests

BASE_URL = "http://127.0.0.1:5000"

# Test data for products
# Each product is a dictionary with the required fields
# this script also helps to test the API endpoints for product management

products = [
    {
        "productId": "P001",
        "name": "Papa Pastusa",
        "description": "Papa de excelente calidad",
        "category": "Tubérculo",
        "price": 1200.0,
        "stock": 100,
        "unit": "kg",
        "origin": "Boyacá",
        "imageUrl": "https://example.com/images/papa.jpg"
    },
    {
        "productId": "P002",
        "name": "Mango Tommy",
        "description": "Mango dulce y jugoso",
        "category": "Fruta",
        "price": 2500.0,
        "stock": 50,
        "unit": "kg",
        "origin": "Tolima",
        "imageUrl": "https://example.com/images/mango.jpg"
    },
    {
        "productId": "P003",
        "name": "Café Supremo",
        "description": "Café de exportación",
        "category": "Grano",
        "price": 18000.0,
        "stock": 30,
        "unit": "kg",
        "origin": "Huila",
        "imageUrl": "https://example.com/images/cafe.jpg"
    },
    {
        "productId": "P004",
        "name": "Plátano Hartón",
        "description": "Plátano fresco",
        "category": "Fruta",
        "price": 900.0,
        "stock": 200,
        "unit": "kg",
        "origin": "Antioquia",
        "imageUrl": "https://example.com/images/platano.jpg"
    },
    {
        "productId": "P005",
        "name": "Yuca",
        "description": "Yuca blanca",
        "category": "Tubérculo",
        "price": 800.0,
        "stock": 150,
        "unit": "kg",
        "origin": "Córdoba",
        "imageUrl": "https://example.com/images/yuca.jpg"
    },
    {
        "productId": "P006",
        "name": "Aguacate Hass",
        "description": "Aguacate para exportación",
        "category": "Fruta",
        "price": 3500.0,
        "stock": 60,
        "unit": "kg",
        "origin": "Antioquia",
        "imageUrl": "https://example.com/images/aguacate.jpg"
    },
    {
        "productId": "P007",
        "name": "Cebolla Larga",
        "description": "Cebolla fresca",
        "category": "Verdura",
        "price": 1200.0,
        "stock": 80,
        "unit": "kg",
        "origin": "Boyacá",
        "imageUrl": "https://example.com/images/cebolla.jpg"
    },
    {
        "productId": "P008",
        "name": "Tomate Chonto",
        "description": "Tomate para ensalada",
        "category": "Verdura",
        "price": 1500.0,
        "stock": 90,
        "unit": "kg",
        "origin": "Cundinamarca",
        "imageUrl": "https://example.com/images/tomate.jpg"
    },
    {
        "productId": "P009",
        "name": "Maíz Amarillo",
        "description": "Maíz seco",
        "category": "Grano",
        "price": 1100.0,
        "stock": 120,
        "unit": "kg",
        "origin": "Meta",
        "imageUrl": "https://example.com/images/maiz.jpg"
    },
    {
        "productId": "P010",
        "name": "Frijol Bola Roja",
        "description": "Frijol seleccionado",
        "category": "Grano",
        "price": 4000.0,
        "stock": 70,
        "unit": "kg",
        "origin": "Santander",
        "imageUrl": "https://example.com/images/frijol.jpg"
    },
    {
        "productId": "P011",
        "name": "Banano",
        "description": "Banano de exportación",
        "category": "Fruta",
        "price": 1200.0,
        "stock": 300,
        "unit": "kg",
        "origin": "Magdalena",
        "imageUrl": "https://example.com/images/banano.jpg"
    },
    {
        "productId": "P012",
        "name": "Lulo",
        "description": "Lulo fresco",
        "category": "Fruta",
        "price": 3500.0,
        "stock": 40,
        "unit": "kg",
        "origin": "Nariño",
        "imageUrl": "https://example.com/images/lulo.jpg"
    }
]

def test_create_products():
    print("Testing product creation...")
    for prod in products:
        resp = requests.post(f"{BASE_URL}/products", json=prod)
        print(f"POST /products {prod['productId']} ->", resp.status_code, resp.json())

def test_get_all_products():
    print("\nTesting get all products...")
    resp = requests.get(f"{BASE_URL}/products")
    print("GET /products ->", resp.status_code)
    for prod in resp.json():
        print(prod)

def test_get_product_by_id(product_id):
    print(f"\nTesting get product by id: {product_id}")
    resp = requests.get(f"{BASE_URL}/products/{product_id}")
    print(f"GET /products/{product_id} ->", resp.status_code, resp.json())

def test_get_product_not_found():
    print("\nTesting get product by id (not found)...")
    resp = requests.get(f"{BASE_URL}/products/NO_EXISTE")
    print("GET /products/NO_EXISTE ->", resp.status_code, resp.json())

def test_test_route():
    print("\nTesting test route...")
    resp = requests.get(f"{BASE_URL}/test")
    print("GET /test ->", resp.status_code, resp.text)

if __name__ == "__main__":
    test_create_products()
    test_get_all_products()
    for prod in products:
        test_get_product_by_id(prod["productId"])
    test_get_product_not_found()
    test_test_route()