import psycopg2
import os

def init_database():
    """Initialize database tables"""
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'appuser'),
        password=os.getenv('DB_PASSWORD', 'apppass'),
        database=os.getenv('DB_NAME', 'appdb')
    )
    
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            amount DECIMAL(10,2) NOT NULL,
            date DATE NOT NULL,
            category VARCHAR(50) NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for better performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_expenses_date 
        ON expenses(date)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_expenses_category 
        ON expenses(category)
    ''')
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()