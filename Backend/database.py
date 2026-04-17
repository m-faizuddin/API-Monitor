
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

def add_api(name, url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO monitored_apis (name, url) VALUES (?, ?)", (name, url)) 

    conn.commit()
    conn.close()

def get_apis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM monitored_apis")
    apis = cursor.fetchall() # Fetch all rows from the monitored_apis table and store them in the apis variable as a list of sqlite3.Row objects

    result = []
    for api in apis:
        result.append({
            "id": api["id"],
            "name": api["name"],
            "url": api["url"],
            "created_at": api["created_at"],
            "is_active": bool(api["is_active"]) # Convert the is_active value from the database (which is stored as an integer) to a boolean value (True or False) before adding it to the result list
        })

    conn.close()

    return result


   



   



