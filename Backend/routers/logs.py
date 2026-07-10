#logs.py - This file defines the API routes for managing monitoring logs in the application. It uses FastAPI's APIRouter to create a modular set of routes related to monitoring logs functionality. The routes include retrieving logs for a specific API and retrieving statistics for a specific API based on the monitoring logs. Each route interacts with the SQLite database using functions from the database module to perform the necessary operations, such as fetching logs and calculating statistics based on the monitoring logs for a given API. The routes also handle error cases, such as when an API is not found for retrieving logs or statistics, by raising appropriate HTTP exceptions.
from fastapi import APIRouter, HTTPException
from database import get_connection

router = APIRouter()


@router.get("/apis/{api_id}/logs")
def get_logs(api_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM monitored_apis WHERE id = ?", (api_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="API not found!")
    
    cursor.execute(
        "SELECT * FROM monitoring_logs WHERE api_id = ? ORDER BY checked_at DESC",
        (api_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@router.get("/apis/{api_id}/stats")
def get_stats(api_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM monitored_apis WHERE id = ?", (api_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="API not found!")

    cursor.execute(
        "SELECT COUNT(*) as total FROM monitoring_logs WHERE api_id = ?",
        (api_id,)
    )

    total  = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as success FROM monitoring_logs WHERE api_id = ? AND success = 1",
        (api_id,)
    )
    success = cursor.fetchone()["success"]

    cursor.execute(
        "SELECT AVG(response_time) as avg_response FROM monitoring_logs WHERE api_id = ?",
        (api_id,)
    )

    avg_response = cursor.fetchone()["avg_response"]
    # avg_response = round(cursor.fetchone()["avg_response"] or 0, 2)

    conn.close()

    uptime = round((success / total) * 100, 2) if total > 0 else 0

    return {
        "total_checks": total,
        "successful_checks": success,
        "uptime_percentage": uptime,
        "avg_response_time_ms": round(avg_response or 0, 2)
    }


