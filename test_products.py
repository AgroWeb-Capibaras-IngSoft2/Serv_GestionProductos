import requests

BASE_URL = "http://127.0.0.1:5000"

# Test data for products
# Each product is a dictionary with the required fields
# this script also helps to test the API endpoints for product management

products = [
    {
        "productId": "1",
        "name": "Lechuga",
        "category": "vegetables",
        "price": 6000,
        "unit": "Unidad / 500g",
        "imageUrl": "http://localhost:5000/static/catalog/lechuga.avif",
        "stock": 10,
        "origin": "Cundinamarca",
        "description": "Lechuga fresca y crujiente, ideal para ensaladas.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": True,
        "freeShipping": False,
    },
    {
        "productId": "2",
        "name": "Brocoli",
        "category": "vegetables",
        "price": 5000,
        "unit": "500g",
        "imageUrl": "http://localhost:5000/static/catalog/brocoli.jpg",
        "stock": 15,
        "origin": "Boyacá",
        "description": "Brocoli fresco.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": False,
    },
    {
        "productId": "3",
        "name": "Papa sabanera",
        "category": "fruits",
        "price": 6000,
        "unit": "1kg",
        "imageUrl": "http://localhost:5000/static/catalog/papa_sabanera.jpg",
        "stock": 40,  
        "origin": "Sogamoso",  
        "description": "Papa sabanera con un sabor único.",
        "isActive": True,
        # Optional fields:
        "originalPrice": 7000,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": True,
    },
    {
        "productId": "4",
        "name": "Mango",
        "category": "dairy",
        "price": 3000,
        "unit": "1 kg",
        "imageUrl": "http://localhost:5000/static/catalog/mango.jpg",
        "stock": 40,  
        "origin": "Melgar", 
        "description": "Mango fresco y jugoso.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": True,
        "freeShipping": False,
    },
    {
        "productId": "5",
        "name": "Piña",
        "category": "vegetables",
        "price": 12000,
        "unit": "1kg",
        "imageUrl": "http://localhost:5000/static/catalog/pina.jpg",
        "stock": 0, 
        "origin": "Santander", 
        "description": "Piña para la niña",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": False,
    },
    {
        "productId": "6",
        "name": "Fresas",
        "category": "fruits",
        "price": 4000,
        "unit": "250g",
        "imageUrl": "http://localhost:5000/static/catalog/fresas.avif",
        "stock": 0, 
        "origin": "Chocontá", 
        "description": "Jugosas fresas.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": False,
        "isBestSeller": True,
        "freeShipping": False,
    },
    {
        "productId": "7",
        "name": "Huevos campesinos",
        "category": "dairy",
        "price": 3000,
        "unit": "Docena",
        "imageUrl": "http://localhost:5000/static/catalog/huevos_campesinos.jpeg",
        "stock": 20, 
        "origin": "Buga", 
        "description": "Huevos frescos de granja, ideales para el desayuno.",
        "isActive": True,
        # Optional fields:
        "originalPrice": 4000,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": True,
    },
    {
        "productId": "8",
        "name": "Banano",
        "category": "herbs",
        "price": 3000,
        "unit": "Racimo",
        "imageUrl": "http://localhost:5000/static/catalog/banano.jpeg",
        "stock": 40,
        "origin": "Sibaté",
        "description": "Banano fresco.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": False,
    },
    {
        "productId": "9",
        "name": "Cebolla",
        "category": "vegetables",
        "price": 2000,
        "unit": "500g",
        "imageUrl": "http://localhost:5000/static/catalog/cebolla.jpg",
        "stock": 30,
        "origin": "Aquitania",
        "description": "Cebolla fresca y sabrosa, ideal para cocinar.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": False,
        "isBestSeller": False,
        "freeShipping": False
    },
    {
        "productId": "10",
        "name": "Maiz",
        "category": "fruits",
        "price": 6000,
        "unit": "Costal",
        "imageUrl": "http://localhost:5000/static/catalog/maiz.jpg",
        "stock": 0,
        "origin": "Duitama",
        "description": "Maiz dulce y fresco.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": True,
        "freeShipping": True
    },
    {
        "productId": "11",
        "name": "Tomate",
        "category": "dairy",
        "price": 3000,
        "unit": "250g",
        "imageUrl": "http://localhost:5000/static/catalog/tomate.jpg",
        "stock": 30,
        "origin": "Ventaquemada",
        "description": "Tomate fresco.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": True,
    },
    {
        "productId": "12",
        "name": "Zanahoria",
        "category": "herbs",
        "price": 8000,
        "unit": "500g",
        "imageUrl": "http://localhost:5000/static/catalog/zanahoria.jpg",
        "stock": 0,
        "origin": "Soacha",
        "description": "Zanahoria fresca.",
        "isActive": True,
        # Optional fields:
        "originalPrice": None,
        "isOrganic": True,
        "isBestSeller": False,
        "freeShipping": False
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
    products = resp.json()
    print("Response JSON:", products)
    for prod in products:
        print(prod)
        # Assert inStock is correct
        assert prod["inStock"] == (prod["stock"] > 0)

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