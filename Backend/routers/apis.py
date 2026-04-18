from fastapi import APIRouter, HTTPException
from database import get_connection
from models.api_target import APICreate, APIUpdate, APIStatus


router = APIRouter() #This line creates an instance of the APIRouter class and assigns it to the variable router. The APIRouter class is a component of FastAPI that allows us to define a group of related routes and their associated logic. By creating an instance of APIRouter, we can organize our API endpoints into logical groups, making our code more modular and easier to maintain. The router variable will be used to register routes related to API monitoring functionality as we build out our application further.


@router.post("/apis")
def add_api(data: APICreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO monitored_apis (name, url) VALUES (?, ?)",
        (data.name, data.url)
    )

    conn.commit()
    conn.close()

    return {"message": "API added successfully!"}

@router.get("/apis")
def get_apis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM monitored_apis")
    rows = cursor.fetchall() #This line executes a SQL query to retrieve all rows from the monitored_apis table in the database. The cursor.execute() method is used to execute the SQL query, and the result is stored in the variable rows. The fetchall() method is then called on the cursor object to retrieve all the rows returned by the query and store them in the rows variable as a list of tuples. Each tuple represents a row from the monitored_apis table, containing the values of the columns for that row.
    conn.close()
    
    results =[]
    for row in rows:
        results.append(dict(row))

    return results

@router.put("/apis/{api_id}")
def update_api(api_id: int, data: APIUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * FROM monitored_apis WHERE id = ?", (api_id,))
    row = cursor.fetchone() # This line executes a SQL query to retrieve a single row from the monitored_apis table in the database based on the provided api_id. The cursor.execute() method is used to execute the SQL query, and the result is stored in the variable row. The fetchone() method is then called on the cursor object to retrieve the first row returned by the query and store it in the row variable as a tuple. If no row is found with the specified api_id, the row variable will be None.

    if not row:
        raise HTTPException(status_code=404, detail="API not found")
    
    cursor.execute(
        "UPDATE monitored_apis SET name = ?, url = ? WHERE id = ?",
        (data.name, data.url, api_id)
    )

    conn.commit()
    conn.close()

    return {"message": "API updated successfully!"}


@router.patch("/apis/{api_id}/status")
def update_status(api_id: int, data: APIStatus):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("Select * FROM monitored_apis WHERE id = ?", (api_id,))
    row = cursor.fetchone() # This line executes a SQL query to retrieve a single row from the monitored_apis table in the database based on the provided api_id. The cursor.execute() method is used to execute the SQL query, and the result is stored in the variable row. The fetchone() method is then called on the cursor object to retrieve the first row returned by the query and store it in the row variable as a tuple. If no row is found with the specified api_id, the row variable will be None.

    if not row:
        raise HTTPException(status_code=404, detail="API not found")

    cursor.execute(
        "UPDATE monitored_apis SET is_active = ? WHERE id = ?",
        (data.is_active, api_id)
    )

    conn.commit()
    conn.close()

    # message = "API marked"

    # if(data.is_active):
    #     message += " active"
    # else:
    #     message += " inactive"

    return {"message": f"API marked {'active' if data.is_active else 'inactive'}"}
