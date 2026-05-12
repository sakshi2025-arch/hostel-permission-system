import sqlite3

conn = sqlite3.connect('hostel.db')

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS requests (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    student_name TEXT,
    branch TEXT,
    year TEXT,
    hostel_no TEXT,
    room_no TEXT,

    student_no TEXT,
    parent_no TEXT,

    outgoing_date TEXT,
    incoming_date TEXT,

    reason TEXT,
    emergency_level TEXT,
    emergency TEXT,

    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()
conn.close()

print("Database & Table Created Successfully ✅")