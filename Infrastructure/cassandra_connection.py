"""
Cassandra Database Connection and Configuration
Handles connection to Cassandra cluster and keyspace setup
"""

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement
import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)

class CassandraConnection:
    """
    Manages Cassandra database connection and provides session access
    """
    
    def __init__(self):
        self._session = None
        self._cluster = None
        self.keyspace = os.getenv('CASSANDRA_KEYSPACE', 'productos_db')
        self.hosts = os.getenv('CASSANDRA_HOSTS', '127.0.0.1').split(',')
        self.port = int(os.getenv('CASSANDRA_PORT', '9042'))
        self.username = os.getenv('CASSANDRA_USERNAME')
        self.password = os.getenv('CASSANDRA_PASSWORD')
        
    def connect(self) -> bool:
        """
        Establishes connection to Cassandra cluster
        Returns True if successful, False otherwise
        """
        try:
            # Setup authentication if credentials provided
            auth_provider = None
            if self.username and self.password:
                auth_provider = PlainTextAuthProvider(
                    username=self.username, 
                    password=self.password
                )
            
            # Create cluster connection with timeout
            self._cluster = Cluster(
                contact_points=self.hosts,
                port=self.port,
                auth_provider=auth_provider,
                connect_timeout=10,  # 10 second connection timeout
                control_connection_timeout=10  # 10 second control connection timeout
            )
            
            # Create session with timeout
            print(f"🔗 Connecting to Cassandra at {self.hosts}:{self.port}...")
            self._session = self._cluster.connect()
            print("✅ Cassandra session established")
            
            # Create keyspace if it doesn't exist
            self._create_keyspace()
            
            # Use the keyspace
            self._session.set_keyspace(self.keyspace)
            
            # Create tables if they don't exist
            self._create_tables()
            
            logger.info(f"Successfully connected to Cassandra cluster at {self.hosts}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Cassandra: {str(e)}")
            return False
    
    def disconnect(self):
        """
        Closes the connection to Cassandra
        """
        if self._session:
            self._session.shutdown()
        if self._cluster:
            self._cluster.shutdown()
        logger.info("Disconnected from Cassandra")
    
    def get_session(self):
        """
        Returns the active Cassandra session
        """
        if not self._session:
            if not self.connect():
                raise ConnectionError("Unable to establish Cassandra connection")
        return self._session
    
    def _create_keyspace(self):
        """
        Creates the keyspace if it doesn't exist
        """
        create_keyspace_query = f"""
        CREATE KEYSPACE IF NOT EXISTS {self.keyspace}
        WITH REPLICATION = {{
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }}
        """
        self._session.execute(create_keyspace_query)
        logger.info(f"Keyspace '{self.keyspace}' ready")
    
    def _create_tables(self):
        """
        Creates the products table if it doesn't exist
        """
        create_products_table = """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            price DOUBLE,
            original_price DOUBLE,
            unit TEXT,
            image_url TEXT,
            stock INT,
            origin TEXT,
            description TEXT,
            user_id TEXT,
            created_at DATE,
            updated_at DATE,
            is_active BOOLEAN,
            is_organic BOOLEAN,
            is_best_seller BOOLEAN,
            free_shipping BOOLEAN
        )
        """
        
        # Create secondary indexes for common queries
        
        create_active_index = """
        CREATE INDEX IF NOT EXISTS products_active_idx 
        ON products (is_active)
        """
        
        create_user_id_index = """
        CREATE INDEX IF NOT EXISTS products_user_id_idx
        ON products (user_id)
        """

        session = self.get_session()
        session.execute(create_products_table)
        session.execute(create_user_id_index)
        session.execute(create_active_index)
        
        logger.info("Products table and indexes created successfully")

# Global connection instance
_cassandra_connection = None

def get_cassandra_connection() -> CassandraConnection:
    """
    Returns a singleton instance of CassandraConnection
    """
    global _cassandra_connection
    if _cassandra_connection is None:
        _cassandra_connection = CassandraConnection()
    return _cassandra_connection
