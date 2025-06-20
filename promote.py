# promote.py
import sqlite3

DB       = "database.db"
USERNAME = "xenia"

with sqlite3.connect(DB) as conn:
    conn.execute("UPDATE 'user' SET is_admin = 1 WHERE username = ?", (USERNAME,))
    conn.commit()
print(f"✅ {USERNAME} is now an admin")
