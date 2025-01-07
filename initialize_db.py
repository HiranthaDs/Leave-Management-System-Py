import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('leave_management.db')

# Enable foreign key support (Important for relational integrity)
conn.execute('PRAGMA foreign_keys = ON;')

cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

# Create leave_requests table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        job_id TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        leave_dates TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully.")
