import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor

# Manages database connection pooling for efficient resource use
class ConnectionPool:
    def __init__(self, database_uri):
        self.database_uri = database_uri
        self.pool = psycopg2.pool.SimpleConnectionPool(
            1, 10, dsn=self.database_uri, cursor_factory=RealDictCursor
        )

    # Retrieves a connection from the pool
    def get_connection(self):
        return self.pool.getconn()

    # Returns a connection to the pool
    def release_connection(self, connection):
        self.pool.putconn(connection)

    # Closes all connections in the pool
    def close_all(self):
        self.pool.closeall()

# Initialize the connection pool
DATABASE_URI = "postgresql://postgres.kckmdwvylxyuzdlavlku:vHIreCwrVv5xlKxk@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
connection_pool = ConnectionPool(DATABASE_URI)