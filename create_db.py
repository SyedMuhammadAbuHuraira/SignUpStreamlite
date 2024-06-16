
import sqlite3
def create_user(username, password, glucose_level, sugar_level):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    hashed_password = hash_password(password)
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
    user_id = c.lastrowid
    c.execute('INSERT INTO health_data (user_id, glucose_level, sugar_level) VALUES (?, ?, ?)',
              (user_id, glucose_level, sugar_level))
    conn.commit()
    conn.close()
# SQL commands to create tables
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
"""

CREATE_HEALTH_DATA_TABLE = """
CREATE TABLE IF NOT EXISTS health_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    glucose_level REAL,
    sugar_level REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
"""

# Connect to the database and execute table creation SQL
conn = sqlite3.connect('health_data.db')
c = conn.cursor()
c.execute(CREATE_USERS_TABLE)
c.execute(CREATE_HEALTH_DATA_TABLE)
conn.commit()
conn.close()
