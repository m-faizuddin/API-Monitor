#database.py - This file contains the database connection and setup functions for the API monitoring application. It defines the get_connection() function to establish a connection to the SQLite database and set the row factory for easier access to columns by name. The create_tables() function is responsible for creating the necessary tables (monitored_apis and monitoring_logs) in the database if they do not already exist. The monitored_apis table stores information about the APIs being monitored, while the monitoring_logs table stores logs of each monitoring check, including status code, response time, success status, and timestamps. This file serves as the foundation for interacting with the database throughout the application.

import sqlite3

DB_PATH = "database/monitor.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH) # Connect to the SQLite database specified by DB_PATH 
    conn.row_factory = sqlite3.Row # This allows us to access columns by name instead of index 
    return conn # Return the connection object to the caller

def create_tables():
    conn = get_connection() #without this line, we won't be able to execute any SQL commands because we won't have a connection to the database. The get_connection() function establishes a connection to the SQLite database and returns a connection object that we can use to interact with the database. By calling get_connection() at the beginning of the create_tables() function, we ensure that we have a valid connection to the database before attempting to create any tables or execute any SQL commands.
    cursor = conn.cursor() # Create a cursor object from the connection. The cursor is used to execute SQL commands and queries against the database. It acts as an intermediary between the connection and the database, allowing us to send SQL statements and retrieve results. By creating a cursor, we can execute SQL commands such as creating tables, inserting data, and querying the database.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitored_apis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1 
        
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoring_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        api_id INTEGER NOT NULL,
        status_code INTEGER,
        response_time INTEGER,
        success BOOLEAN,
        checked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (api_id) REFERENCES monitored_apis(id) 
    )
    """)
    conn.commit()
    conn.close()



   



   



