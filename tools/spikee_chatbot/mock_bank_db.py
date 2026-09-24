import sqlite3
import json

# Use a shared in-memory database so multiple connections can access the same data
DB_URI = "file::memory:?cache=shared"

# Keep one persistent connection open so the shared in-memory db isn't destroyed
_global_conn = sqlite3.connect(DB_URI, uri=True, check_same_thread=False)

def get_connection():
    # uri=True allows us to use the shared memory URI
    conn = sqlite3.connect(DB_URI, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            account_type TEXT,
            balance REAL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            type TEXT,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Check if we already seeded (since it's a shared in-memory, we only want to seed once)
    cursor.execute('SELECT COUNT(*) as cnt FROM users')
    if cursor.fetchone()['cnt'] == 0:
        # Seed Users
        users = [
            (123, 'Marty McFly', 'marty@hillvalley.com'),
            (124, 'Biff Tannen', 'biff@biffsautodetailing.com'),
            (125, 'Emmett Brown', 'doc@delorean.time')
        ]
        cursor.executemany('INSERT INTO users (id, name, email) VALUES (?, ?, ?)', users)
        
        # Seed Accounts
        accounts = [
            (1, 123, 'Checking', 1500.50),
            (2, 123, 'Savings', 5000.00),
            (3, 124, 'Checking', 99999.99),
            (4, 125, 'Checking', 1.21)
        ]
        cursor.executemany('INSERT INTO accounts (id, user_id, account_type, balance) VALUES (?, ?, ?, ?)', accounts)
        
        # Seed Transactions
        transactions = [
            (123, -50.00, 'Debit', 'Cafe 80s'),
            (123, -15.50, 'Debit', 'Hoverboard Wax'),
            (124, 10000.00, 'Credit', 'Sports Almanac Winnings'),
            (125, -500.00, 'Debit', 'Plutonium Purchase')
        ]
        cursor.executemany('INSERT INTO transactions (user_id, amount, type, description) VALUES (?, ?, ?, ?)', transactions)
    
    conn.commit()
    conn.close()

# Run initialization when module is imported
init_db()

def get_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_accounts(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_user_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def execute_sql(query):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if query.strip().upper().startswith('SELECT'):
            rows = cursor.fetchall()
            conn.close()
            return {"status": "success", "data": [dict(row) for row in rows]}
        else:
            conn.commit()
            rowcount = cursor.rowcount
            conn.close()
            return {"status": "success", "message": f"Query executed. Rows affected: {rowcount}"}
    except Exception as e:
        conn.close()
        return {"status": "error", "message": str(e)}
