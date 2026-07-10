import requests
import time
from database import get_connection


def check_apis():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM monitored_apis WHERE is_active = 1")
    apis = cursor.fetchall()

    for api in apis:
        start = time.time()

        try:
            response = requests.get(api["url"], timeout=10)
            status_code = response.status_code
            success = status_code < 400
        except Exception:
            status_code = 0
            success = False

        response_time = int((time.time() - start) * 1000)

        cursor.execute(
            "INSERT INTO monitoring_logs (api_id, status_code, response_time, success) VALUES(?, ?, ?, ?)",
            (api["id"], status_code, response_time, success)
        )
    conn.commit()
    conn.close()
    print("Health check done")