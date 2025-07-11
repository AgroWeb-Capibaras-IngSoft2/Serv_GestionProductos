"""
Database Seeding Script for Product Management Service
Clears existing data and populates the database with sample products
"""

import requests
import json
import sys
from typing import Dict, List

BASE_URL = "http://127.0.0.1:5000"
TIMEOUT = 10  # seconds

# Sample product data for the catalog
products = [
    {
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


class DatabaseSeeder:
    """Database seeding utility for Product Management Service"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def check_server_health(self) -> bool:
        """Check if the API server is running and accessible"""
        try:
            response = self.session.get(f"{self.base_url}/products", timeout=TIMEOUT)
            print(f"✅ Server is accessible (Status: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Server is not accessible: {e}")
            print("   Make sure the service is running: python app.py")
            return False
    
    def clear_database(self) -> bool:
        """Clear all existing data from the database"""
        print("\n🧹 Clearing existing database...")
        try:
            # Import and use the database directly for clearing
            from Infrastructure.adapterProductRepo import AdapterProductRepo
            from Infrastructure.cassandra_db import CassandraDB
            from Infrastructure.DB import db as pandas_db
            import os
            
            # Check which database backend is being used
            use_cassandra = os.getenv('USE_CASSANDRA', 'true').lower() == 'true'
            
            if use_cassandra:
                try:
                    # Use Cassandra database directly
                    cassandra_db = CassandraDB()
                    # Get all products as dictionaries
                    all_products = cassandra_db.get_all_products()
                    
                    if not all_products:
                        print("✅ Database is already empty")
                        return True
                    
                    print(f"   Found {len(all_products)} existing products")
                    
                    # Delete each product
                    deleted_count = 0
                    for product in all_products:
                        try:
                            product_id = product['productId']
                            if cassandra_db.delete_product(product_id):
                                deleted_count += 1
                                print(f"   🗑️  Deleted: {product_id}")
                        except Exception as e:
                            print(f"   ⚠️  Warning: Could not delete product: {e}")
                    
                    print(f"✅ Cleared {deleted_count} products from Cassandra database")
                    return True
                    
                except Exception as e:
                    print(f"   ⚠️  Cassandra clearing failed: {e}")
                    print("   Falling back to repository method...")
            
            # Fallback: Use repository method (works for both backends)
            repo = AdapterProductRepo()
            all_products = repo.get_all_products()  # Returns Product objects
            
            if not all_products:
                print("✅ Database is already empty")
                return True
            
            print(f"   Found {len(all_products)} existing products")
            
            # Delete each product using Product objects
            deleted_count = 0
            for product in all_products:
                try:
                    product_id = product.productId  # Access as Product object attribute
                    if repo.delete_product(product_id):
                        deleted_count += 1
                        print(f"   🗑️  Deleted: {product_id}")
                except Exception as e:
                    print(f"   ⚠️  Warning: Could not delete product {product.productId}: {e}")
            
            print(f"✅ Cleared {deleted_count} products from database")
            return True
            
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            print("   Continuing with seeding (existing products may cause conflicts)...")
            return False
            return False
    
    def create_product(self, product_data: Dict) -> bool:
        """Create a single product via API"""
        try:
            response = self.session.post(
                f"{self.base_url}/products",
                json=product_data,
                timeout=TIMEOUT
            )
            if response.status_code == 201:
                created_product = response.json()
                product_id = created_product.get('productId', 'unknown')
                print(f"  ✅ Created: {product_data['name']} (ID: {product_id})")
                return True
            else:
                print(f"  ❌ Failed to create {product_data['name']}: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"     Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"     Response: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"  ❌ Network error creating {product_data['name']}: {e}")
            return False
    
    def seed_products(self) -> bool:
        """Seed the database with sample products"""
        print(f"\n🌱 Seeding database with {len(products)} products...")
        
        success_count = 0
        for i, product in enumerate(products, 1):
            print(f"  [{i:2d}/{len(products)}] Creating {product['name']}...")
            if self.create_product(product):
                success_count += 1
        
        print(f"\n📊 Seeding Results: {success_count}/{len(products)} products created successfully")
        return success_count == len(products)
    
    def verify_seeding(self) -> bool:
        """Verify that the products were created correctly"""
        print("\n🔍 Verifying seeded data...")
        try:
            response = self.session.get(f"{self.base_url}/products", timeout=TIMEOUT)
            if response.status_code == 200:
                products_in_db = response.json()
                print(f"✅ Database now contains {len(products_in_db)} products")
                
                # Show summary by category
                categories = {}
                active_count = 0
                in_stock_count = 0
                
                for product in products_in_db:
                    category = product.get('category', 'unknown')
                    categories[category] = categories.get(category, 0) + 1
                    
                    if product.get('isActive', False):
                        active_count += 1
                    
                    if product.get('inStock', False):
                        in_stock_count += 1
                
                print(f"   📈 {active_count} active products")
                print(f"   📦 {in_stock_count} products in stock")
                print("   📂 Categories:")
                for category, count in sorted(categories.items()):
                    print(f"      - {category}: {count} products")
                
                return True
            else:
                print(f"❌ Failed to verify data: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error verifying data: {e}")
            return False
    
    def run_full_seeding(self) -> bool:
        """Run the complete seeding process"""
        print("🎯 Product Database Seeding Script")
        print("=" * 50)
        
        # Step 1: Check server health
        if not self.check_server_health():
            return False
        
        # Step 2: Clear existing data
        self.clear_database()
        
        # Step 3: Seed with new data
        if not self.seed_products():
            print("\n❌ Seeding failed!")
            return False
        
        # Step 4: Verify results
        if not self.verify_seeding():
            print("\n⚠️  Verification failed!")
            return False
        
        print("\n🎉 Database seeding completed successfully!")
        print(f"   API Base URL: {self.base_url}")
        print(f"   Total Products: {len(products)}")
        print("   Ready for development and testing!")
        
        return True


def main():
    """Main function to run the database seeding"""
    seeder = DatabaseSeeder()
    
    try:
        success = seeder.run_full_seeding()
        if success:
            print("\n✅ Database is ready!")
            print("   You can now:")
            print("   - Run tests: python test_products_clean.py")
            print("   - Access API: http://localhost:5000/products")
            print("   - View Swagger: http://localhost:5000/swagger")
        else:
            print("\n❌ Seeding process failed!")
            print("   Check the errors above and try again.")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Seeding interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
