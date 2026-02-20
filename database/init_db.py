import sqlite3

def init_database():
    conn = sqlite3.connect("database/soc_engine.db")
    cursor = conn.cursor()

    with open("database/schema.sql", "r") as f:
        schema = f.read()

    cursor.executescript(schema)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully.")
    