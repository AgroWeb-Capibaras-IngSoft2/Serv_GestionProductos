"""
Get Products by Category Use Case
Handles business logic for retrieving products filtered by category
"""

from domain.repositorio.product_repo import ProductRepository
from domain.entidades.product_model import Product
from typing import List
import logging

logger = logging.getLogger(__name__)

class GetProductsByCategoryService:
    """Use case service for retrieving products by category"""
    
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, category: str) -> List[Product]:
        """
        Retrieves products that belong to the specified category
        
        Args:
            category: Category name to filter by
            
        Returns:
            List of Product instances in the specified category
            
        Raises:
            ValueError: If category is empty or invalid
            Exception: For repository errors
        """
        # Input validation
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        
        category = category.strip()
        
        try:
            products = self.product_repository.get_products_by_category(category)
            logger.info(f"Retrieved {len(products)} products for category '{category}'")
            return products
            
        except Exception as e:
            logger.error(f"Error retrieving products for category '{category}': {str(e)}")
            raise Exception(f"Failed to retrieve products by category: {str(e)}")
