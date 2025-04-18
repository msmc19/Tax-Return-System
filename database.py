from db_connection import connection_pool

# Database operations for CRUD actions and table management

# Executes a SQL query and handles connection pooling
def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    connection = None
    try:
        # Acquire connection from the pool
        connection = connection_pool.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
                connection.commit()  # Commit after fetch
                return result
            elif fetch_all:
                results = cursor.fetchall()
                connection.commit()  # Commit after fetch
                return results
            connection.commit()  # Default commit for write operations
    except Exception as e:
        if connection:
            connection.rollback()  # Rollback on failure
        print(f"Database error: {e}")  # Log error for debugging
        raise
    finally:
        if connection:
            connection_pool.release_connection(connection)  # Always release the connection

# Function to reset the sequence for a table
def reset_sequence(table_name, id_column):
    query = f"SELECT SETVAL(pg_get_serial_sequence(%s, %s), COALESCE(MAX({id_column}), 0) + 1, false) FROM {table_name}"
    execute_query(query, (table_name, id_column))


# Create tables
def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS CPAs (
            cpa_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS Clients (
            client_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address VARCHAR(255),
            income DECIMAL(10, 2),
            tax_materials_submitted BOOLEAN DEFAULT FALSE,
            cpa_id INT REFERENCES CPAs(cpa_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS TaxFilingAssistants (
            assistant_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS TaxReturns (
            return_id SERIAL PRIMARY KEY,
            client_id INT UNIQUE REFERENCES Clients(client_id),
            status BOOLEAN DEFAULT FALSE,
            filing_timestamp TIMESTAMP,
            checked_by_cpa BOOLEAN DEFAULT FALSE,
            filed_by_assistant BOOLEAN DEFAULT FALSE
        )
        """
    ]
    for query in queries:
        execute_query(query)
    print("All tables created successfully.")

# CRUD operations for CPAs
def insert_cpa(name):
    query = "INSERT INTO CPAs (name) VALUES (%s) RETURNING cpa_id"
    return execute_query(query, (name,), fetch_one=True)

def get_cpa_by_id(cpa_id):
    query = "SELECT * FROM CPAs WHERE cpa_id = %s"
    return execute_query(query, (cpa_id,), fetch_one=True)

def update_cpa_name(cpa_id, new_name):
    query = "UPDATE CPAs SET name = %s WHERE cpa_id = %s"
    execute_query(query, (new_name, cpa_id))

def delete_cpa(cpa_id):
    query = "DELETE FROM CPAs WHERE cpa_id = %s"
    execute_query(query, (cpa_id,))
    reset_sequence("CPAs", "cpa_id")

# CRUD operations for Clients
def insert_client(name, address, income, cpa_id):
    query = """
        INSERT INTO Clients (name, address, income, cpa_id) 
        VALUES (%s, %s, %s, %s) RETURNING client_id
    """
    return execute_query(query, (name, address, income, cpa_id), fetch_one=True)

def get_client_by_id(client_id):
    query = "SELECT * FROM Clients WHERE client_id = %s"
    return execute_query(query, (client_id,), fetch_one=True)

def update_client_field(client_id, field, new_value):
    query = f"UPDATE Clients SET {field} = %s WHERE client_id = %s"
    execute_query(query, (new_value, client_id))

def delete_client(client_id):
    query = "DELETE FROM Clients WHERE client_id = %s"
    execute_query(query, (client_id,))
    reset_sequence("Clients", "client_id")

# CRUD operations for Tax Filing Assistants
def insert_tax_filing_assistant(name):
    query = "INSERT INTO TaxFilingAssistants (name) VALUES (%s) RETURNING assistant_id"
    return execute_query(query, (name,), fetch_one=True)

def get_tax_filing_assistant_by_id(assistant_id):
    query = "SELECT * FROM TaxFilingAssistants WHERE assistant_id = %s"
    return execute_query(query, (assistant_id,), fetch_one=True)

def update_tax_filing_assistant_name(assistant_id, new_name):
    query = "UPDATE TaxFilingAssistants SET name = %s WHERE assistant_id = %s"
    execute_query(query, (new_name, assistant_id))

def delete_tax_filing_assistant(assistant_id):
    query = "DELETE FROM TaxFilingAssistants WHERE assistant_id = %s"
    execute_query(query, (assistant_id,))
    reset_sequence("TaxFilingAssistants", "assistant_id")

# CRUD operations for Tax Returns
def insert_tax_return(client_id, status, filing_timestamp, checked_by_cpa, filed_by_assistant):
    # Check if the client already has a tax return
    existing_tax_return_query = "SELECT * FROM TaxReturns WHERE client_id = %s"
    existing_tax_return = execute_query(existing_tax_return_query, (client_id,), fetch_one=True)
    if existing_tax_return:
        raise ValueError(f"Client with ID {client_id} already has a tax return.")

    # Insert the new tax return
    query = """
        INSERT INTO TaxReturns (client_id, status, filing_timestamp, checked_by_cpa, filed_by_assistant)
        VALUES (%s, %s, %s, %s, %s) RETURNING return_id
    """
    return execute_query(query, (client_id, status, filing_timestamp, checked_by_cpa, filed_by_assistant),fetch_one=True)

def get_tax_return_by_client_id(client_id):
    query = "SELECT * FROM TaxReturns WHERE client_id = %s"
    return execute_query(query, (client_id,), fetch_one=True)

def update_tax_return_field(return_id, field, new_value):
    query = f"UPDATE TaxReturns SET {field} = %s WHERE return_id = %s"
    execute_query(query, (new_value, return_id))

def mark_filed_by_assistant(return_id):
    query = """
        UPDATE TaxReturns
        SET status = TRUE, filing_timestamp = NOW(), filed_by_assistant = TRUE, checked_by_cpa = FALSE
        WHERE return_id = %s
    """
    execute_query(query, (return_id,))





