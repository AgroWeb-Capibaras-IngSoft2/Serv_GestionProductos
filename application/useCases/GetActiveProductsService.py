"""
===============================
READ OPERATIONS - USE CASES
===============================

Get Active Products Service
Handles business logic for retrieving only active/available products.

Architecture Layer: Application Layer - Use Cases
Dependencies: Domain Repository, Product Entity
Database: Cassandra (filtered by isActive status)

Features:
- Filters for customer-visible products only
- Automatic sorting by creation date (newest first)
- Performance-optimized for storefront display
- Comprehensive error handling and logging
"""

from domain.repositorio.product_repo import ProductRepository
from domain.entidades.product_model import Product
from typing import List
import logging

logger = logging.getLogger(__name__)

class GetActiveProductsService:
    """
    Use case service for retrieving active products for customer display.
    
    This service provides filtered product data suitable for customer-facing
    interfaces, ensuring only available products are returned.
    
    Attributes:
        product_repository (ProductRepository): Repository for data access
    """
    
    def __init__(self, product_repository: ProductRepository):
        """
        Initialize the service with a product repository.
        
        Args:
            product_repository (ProductRepository): Data access layer
        """
        self.product_repository = product_repository
    
    def execute(self) -> List[Product]:
        """
        Retrieves active products optimized for customer storefront display.
        
        Business Rules:
        - Returns only products with isActive = True
        - Automatically sorts by creation date (newest first)
        - Suitable for customer-facing product catalogs
        - Excludes discontinued or draft products
        
        Returns:
            List[Product]: Filtered and sorted list of active Product instances
                         Empty list if no active products exist
                         Sorted by createdAt (newest first)
            
        Raises:
            Exception: For repository errors or system failures
            
        Performance Notes:
        - Optimized for storefront display
        - Pre-sorted for immediate UI consumption
        - Logs active product count for analytics
        
        Example:
            service = GetActiveProductsService(repository)
            active_products = service.execute()
            # Display in storefront UI
            for product in active_products:
                print(f"{product.name} - ${product.price}")
        """
        try:
            # Retrieve active products from repository
            products = self.product_repository.get_active_products()
            
            # Sort by creation date (newest products first for better UX)
            products.sort(key=lambda p: p.createdAt, reverse=True)
            
            # Log success with business metrics
            logger.info(
                f"Successfully retrieved active product catalog - "
                f"Active products: {len(products)} (sorted by newest first)"
            )
            
            return products
            
        except Exception as e:
            logger.error(f"Failed to retrieve active products: {str(e)}")
            raise Exception(f"Failed to retrieve active products: {str(e)}")
