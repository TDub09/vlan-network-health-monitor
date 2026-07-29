
import sqlite3
import urllib.request
from urllib.error import URLError, HTTPError
from datetime import datetime

# Config
APACHE_HOST_IP = '10.10.1.2' 
APACHE_PORT = 80
URL_TO_CHECK = f'http://{APACHE_HOST_IP}:{APACHE_PORT}/hello.html'
DB_FILE = 'apache_health.db'

# DB SQLite 

def initialize_db(db_name):
    """Creates the SQLite database and the health_results table if they don't exist."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_results (
            timestamp TEXT,
            status TEXT,
            status_code INTEGER,
            message TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"[*] Database '{db_name}' initialized.")

def insert_result(db_name, status, status_code, message):
    """Inserts a health check result into the database."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO health_results (timestamp, status, status_code, message)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, status, status_code, message))
    conn.commit()
    conn.close()
    print(f"[+] Inserted result: {status} ({status_code}) at {timestamp}")

# HC

def check_apache_health(url):
    """Performs an HTTP HEAD request to check server status."""
    try:
        
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            if status_code == 200:
                return "UP", status_code, "HTTP 200 OK"
            else:
                return "DOWN", status_code, f"Unexpected HTTP Status: {status_code}"
    except HTTPError as e:
        return "DOWN", e.code, f"HTTP Error: {e.reason}"
    except URLError as e:
        return "DOWN", 0, f"Connection Error: {e.reason}"
    except Exception as e:
        return "DOWN", 0, f"General Error: {str(e)}"

if __name__ == "__main__":
   
    initialize_db(DB_FILE)
    
    health_status, code, msg = check_apache_health(URL_TO_CHECK)
    
    insert_result(DB_FILE, health_status, code, msg)

    print("--- Health Check Complete ---")
