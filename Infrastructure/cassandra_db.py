"""
Cassandra Database Operations (Infrastructure Layer)
Implements CRUD operations using Cassandra for high scalability and performance.
Handles data persistence, querying, and JSON serialization for the Product entity.
"""

from domain.entidades.product_model import Product
from Infrastructure.cassandra_connection import get_cassandra_connection
from datetime import date, datetime
import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

# ===============================
# CASSANDRA DATABASE OPERATIONS
# ===============================

class CassandraDB:
    """
    Database operations for products using Cassandra NoSQL database.
    
    Features:
    - High-performance CRUD operations
    - JSON serialization support
    - Automatic date formatting
    - Connection management
    - Error handling and logging
    """
    
    def __init__(self):
        """Initialize Cassandra connection and session"""
        self.connection = get_cassandra_connection()
        self.session = None
        self._ensure_connection()
    
    def _ensure_connection(self):
        """Ensures database connection is active"""
        try:
            self.session = self.connection.get_session()
        except Exception as e:
            logger.error(f"Failed to establish Cassandra connection: {str(e)}")
            raise ConnectionError(f"Database connection failed: {str(e)}")

    # ===============================
    # CREATE OPERATIONS
    # ===============================
    def add_product(self, product: Product) -> None:
        """
        Adds a new product to the Cassandra database.
        
        Args:
            product (Product): Product entity to be persisted
            
        Raises:
            ValueError: If product with same ID already exists
            Exception: If database operation fails
        """
        try:
            # Check for duplicate product ID
            if self.get_product_by_id(product.productId):
                raise ValueError("Ya existe un producto con ese ID")
            
            # Prepare insert statement
            insert_query = """
            INSERT INTO products (
                product_id, name, category, price, original_price, unit, 
                image_url, stock, origin, description, created_at, updated_at,
                is_active, is_organic, is_best_seller, free_shipping
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            values = (
                product.productId, product.name, product.category, product.price,
                product.originalPrice, product.unit, product.imageUrl, product.stock,
                product.origin, product.description, product.createdAt, product.updatedAt,
                product.isActive, product.isOrganic, product.isBestSeller, product.freeShipping
            )
            
            self.session.execute(insert_query, values)
            logger.info(f"Product {product.productId} added successfully")
            
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to add product {product.productId}: {str(e)}")
            raise Exception(f"Database error while adding product: {str(e)}")

    # ===============================
    # READ OPERATIONS
    # ===============================
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single product by its unique ID.
        
        Args:
            product_id (str): Unique product identifier
            
        Returns:
            Optional[Dict[str, Any]]: Product data as dictionary or None if not found
        """
        try:
            query = "SELECT * FROM products WHERE product_id = %s"
            result = self.session.execute(query, [product_id])
            row = result.one()
            
            if row:
                return self._row_to_dict(row)
            return None
            
        except Exception as e:
            logger.error(f"Failed to get product {product_id}: {str(e)}")
            raise Exception(f"Database error while retrieving product: {str(e)}")
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Retrieves all products from the database.
        
        Returns:
            List[Dict[str, Any]]: List of all products as dictionaries
        """
        try:
            query = "SELECT * FROM products"
            result = self.session.execute(query)
            
            products = []
            for row in result:
                products.append(self._row_to_dict(row))
            
            logger.info(f"Retrieved {len(products)} products from database")
            return products
            
        except Exception as e:
            logger.error(f"Failed to get all products: {str(e)}")
            raise Exception(f"Database error while retrieving products: {str(e)}")
    
    def get_products_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Retrieves products filtered by category"""
        try:
            query = "SELECT * FROM products WHERE category = %s ALLOW FILTERING"
            result = self.session.execute(query, [category])
            
            products = []
            for row in result:
                products.append(self._row_to_dict(row))
            
            logger.info(f"Retrieved {len(products)} products for category {category}")
            return products
            
        except Exception as e:
            logger.error(f"Failed to get products by category {category}: {str(e)}")
            raise Exception(f"Database error while retrieving products by category: {str(e)}")
    
    def get_active_products(self) -> List[Dict[str, Any]]:
        """Retrieves only active products"""
        try:
            query = "SELECT * FROM products WHERE is_active = true ALLOW FILTERING"
            result = self.session.execute(query)
            
            products = []
            for row in result:
                products.append(self._row_to_dict(row))
            
            logger.info(f"Retrieved {len(products)} active products")
            return products
            
        except Exception as e:
            logger.error(f"Failed to get active products: {str(e)}")
            raise Exception(f"Database error while retrieving active products: {str(e)}")

    # ===============================
    # DELETE OPERATIONS
    # ===============================
    
    def delete_product(self, product_id: str) -> bool:
        """
        Deletes a product from the database.
        
        Args:
            product_id (str): ID of the product to delete
            
        Returns:
            bool: True if product was deleted, False if not found
        """
        try:
            # Check if product exists first
            if not self.get_product_by_id(product_id):
                return False
            
            query = "DELETE FROM products WHERE product_id = %s"
            self.session.execute(query, [product_id])
            logger.info(f"Product {product_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete product {product_id}: {str(e)}")
            raise Exception(f"Database error while deleting product: {str(e)}")
    
    def clear_test_data(self) -> None:
        """
        Clears test products from the database.
        Removes products with IDs starting with 'test-' for testing cleanup.
        """
        try:
            # Get all products with test IDs
            query = "SELECT product_id FROM products"
            result = self.session.execute(query)
            
            test_products = []
            for row in result:
                if row.product_id.startswith('test-'):
                    test_products.append(row.product_id)
            
            # Delete each test product
            for product_id in test_products:
                delete_query = "DELETE FROM products WHERE product_id = %s"
                self.session.execute(delete_query, [product_id])
            
            logger.info(f"Cleared {len(test_products)} test products from database")
            
        except Exception as e:
            logger.error(f"Failed to clear test data: {str(e)}")
            raise Exception(f"Database error while clearing test data: {str(e)}")

    # ===============================
    # UTILITY METHODS
    # ===============================
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """
        Converts a Cassandra row to a dictionary compatible with Product model.
        
        Features:
        - Handles date serialization for JSON compatibility
        - Calculates computed fields (inStock)
        - Maps database column names to Product field names
        
        Args:
            row: Cassandra row object
            
        Returns:
            Dict[str, Any]: Product data as dictionary
        """
        def format_date(date_obj):
            """Convert date objects to ISO format strings for JSON serialization"""
            if date_obj is None:
                return None
            if hasattr(date_obj, 'isoformat'):
                return date_obj.isoformat()
            return str(date_obj)
        
        # Calculate inStock based on stock quantity
        stock = row.stock if row.stock is not None else 0
        in_stock = stock > 0
        
        return {
            "productId": row.product_id,
            "name": row.name,
            "category": row.category,
            "price": row.price,
            "originalPrice": row.original_price,
            "unit": row.unit,
            "imageUrl": row.image_url,
            "stock": stock,
            "origin": row.origin,
            "description": row.description,
            "createdAt": format_date(row.created_at),
            "updatedAt": format_date(row.updated_at),
            "isActive": row.is_active,
            "isOrganic": row.is_organic,
            "isBestSeller": row.is_best_seller,
            "freeShipping": row.free_shipping,
            "inStock": in_stock
        }

    # ===============================
    # CONNECTION MANAGEMENT
    # ===============================
    
    def disconnect(self):
        """
        Properly closes the database connection.
        
        Features:
        - Graceful shutdown of Cassandra cluster connection
        - Clears connection state for clean teardown
        - Logs disconnection status for monitoring
        
        Usage:
            db = CassandraDB()
            # ... database operations ...
            db.disconnect()  # Clean shutdown
        """
        try:
            if self.connection and hasattr(self.connection, 'disconnect'):
                self.connection.disconnect()
                logger.info("Successfully disconnected from Cassandra")
        except Exception as e:
            logger.error(f"Error during disconnection: {str(e)}")
    
    def close_connection(self):
        """
        Legacy method for closing database connection.
        
        Note: Use disconnect() for new code - this method maintained for backward compatibility.
        """
        self.disconnect()
    
    def is_connected(self) -> bool:
        """
        Checks if the database connection is active and healthy.
        
        Returns:
            bool: True if connected and responsive, False otherwise
            
        Usage:
            if not db.is_connected():
                # Reconnection logic here
                pass
        """
        try:
            if not self.connection:
                return False
            # Check if connection has a session and is responsive
            return hasattr(self.connection, 'session') and self.connection.session is not None
        except Exception:
            return False

# Factory function for backward compatibility
def db():
    """Factory function that returns a CassandraDB instance"""
    return CassandraDB()
