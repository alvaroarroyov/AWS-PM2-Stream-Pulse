import sqlite3

def init_db():
    conn = sqlite3.connect('pulse.db')
    c = conn.cursor()
    
    # Create table for chat logs with a timestamp
    # Schema: ID (Auto), Username, Message, Exact Time
    c.execute('''CREATE TABLE IF NOT EXISTS chat_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  message TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()
    print("✅ Database 'pulse.db' initialized successfully.")

if __name__ == '__main__':
    init_db()