import psycopg2
import os
from typing import List, Dict, Optional

class Database:
    def __init__(self):
        self.conn_params = {
            'host': os.getenv('DB_HOST', 'db'),
            'port': os.getenv('DB_PORT', '5432'),
            'user': os.getenv('DB_USER', 'appuser'),
            'password': os.getenv('DB_PASSWORD', 'apppass'),
            'database': os.getenv('DB_NAME', 'appdb')
        }
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.conn_params)
    
    def get_next_id(self) -> int:
        """Get the next available ID for new expenses"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COALESCE(MAX(id), 0) + 1 FROM expenses')
        next_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return next_id
    
    def read_expenses(self, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None, 
                     category: Optional[str] = None) -> List[Dict]:
        """Read all expenses with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT id, amount, date, category, description FROM expenses WHERE 1=1'
        params = []
        
        if start_date:
            query += ' AND date >= %s'
            params.append(start_date)
        
        if end_date:
            query += ' AND date <= %s'
            params.append(end_date)
            
        if category:
            query += ' AND category = %s'
            params.append(category)
        
        query += ' ORDER BY date DESC'
        
        cursor.execute(query, params)
        expenses = []
        for row in cursor.fetchall():
            expenses.append({
                'id': row[0],
                'amount': float(row[1]),
                'date': row[2].isoformat(),
                'category': row[3],
                'description': row[4]
            })
        
        cursor.close()
        conn.close()
        return expenses
    
    def write_expense(self, expense: Dict) -> int:
        """Write a single expense to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (id, amount, date, category, description)
            VALUES (%s, %s, %s, %s, %s)
        ''', (expense['id'], expense['amount'], expense['date'], 
              expense['category'], expense['description']))
        
        conn.commit()
        cursor.close()
        conn.close()
        return expense['id']
    
    def get_category_totals(self) -> Dict:
        """Get total amounts by category"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, SUM(amount) 
            FROM expenses 
            GROUP BY category
        ''')
        
        category_totals = {}
        for row in cursor.fetchall():
            category_totals[row[0]] = float(row[1])
        
        cursor.close()
        conn.close()
        return category_totals
    
    def get_monthly_totals(self) -> Dict:
        """Get monthly totals"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT TO_CHAR(date, 'YYYY-MM') as month, SUM(amount)
            FROM expenses
            GROUP BY month
            ORDER BY month
        ''')
        
        monthly_totals = {}
        for row in cursor.fetchall():
            monthly_totals[row[0]] = float(row[1])
        
        cursor.close()
        conn.close()
        return monthly_totals
    
    def get_total_amount(self) -> float:
        """Get total amount of all expenses"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT SUM(amount) FROM expenses')
        total = cursor.fetchone()[0] or 0.0
        
        cursor.close()
        conn.close()
        return float(total)

# Global database instance
db = Database()