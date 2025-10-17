from flask import Flask, request, jsonify
import csv
import os
from datetime import datetime
from typing import List, Dict

app = Flask(__name__)

# Configuration
EXPENSES_FILE = 'expenses.csv'
CATEGORIES = ['food', 'transport', 'entertainment', 'utilities', 'health', 'other']

def init_csv():
    """Create CSV file with headers if it doesn't exist"""
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'amount', 'date', 'category', 'description'])

def get_next_id() -> int:
    """Get the next available ID for new expenses"""
    try:
        with open(EXPENSES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                return 1
            return max(int(row['id']) for row in rows) + 1
    except FileNotFoundError:
        return 1

def read_expenses() -> List[Dict]:
    """Read all expenses from CSV file"""
    expenses = []
    try:
        with open(EXPENSES_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert amount to float and keep other fields
                row['amount'] = float(row['amount'])
                expenses.append(row)
    except FileNotFoundError:
        pass
    return expenses

def write_expense(expense: Dict):
    """Write a single expense to CSV file"""
    with open(EXPENSES_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            expense['id'],
            expense['amount'],
            expense['date'],
            expense['category'],
            expense['description']
        ])

@app.route('/')
def home():
    return jsonify({
        "message": "Personal Expense API",
        "endpoints": {
            "add_expense": "POST /expenses",
            "get_expenses": "GET /expenses",
            "get_summary": "GET /expenses/summary",
            "get_monthly": "GET /expenses/monthly"
        }
    })

@app.route('/expenses', methods=['POST'])
def add_expense():
    """Add a new expense"""
    data = request.get_json()
    
    # Validation
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    required_fields = ['amount', 'date', 'category', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    
    # Validate amount
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a valid number"}), 400
    
    # Validate date
    try:
        datetime.fromisoformat(data['date'])
    except ValueError:
        return jsonify({"error": "Date must be in ISO format (YYYY-MM-DD)"}), 400
    
    # Validate category
    if data['category'] not in CATEGORIES:
        return jsonify({"error": f"Category must be one of: {', '.join(CATEGORIES)}"}), 400
    
    # Create expense record
    expense = {
        'id': get_next_id(),
        'amount': amount,
        'date': data['date'],
        'category': data['category'],
        'description': data['description']
    }
    
    # Save to CSV
    write_expense(expense)
    
    return jsonify({"message": "Expense added successfully", "expense": expense}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses with optional filtering"""
    expenses = read_expenses()
    
    # Filter by date range if provided
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    filtered_expenses = expenses
    
    if start_date:
        try:
            datetime.fromisoformat(start_date)
            filtered_expenses = [e for e in filtered_expenses if e['date'] >= start_date]
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
    
    if end_date:
        try:
            datetime.fromisoformat(end_date)
            filtered_expenses = [e for e in filtered_expenses if e['date'] <= end_date]
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
    
    if category:
        filtered_expenses = [e for e in filtered_expenses if e['category'] == category]
    
    return jsonify({
        "count": len(filtered_expenses),
        "expenses": filtered_expenses
    })

@app.route('/expenses/summary', methods=['GET'])
def get_summary():
    """Get summary by category"""
    expenses = read_expenses()
    
    # Calculate totals by category
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        if category not in category_totals:
            category_totals[category] = 0
        category_totals[category] += expense['amount']
    
    # Calculate overall total
    total_amount = sum(expense['amount'] for expense in expenses)
    
    return jsonify({
        "total_amount": total_amount,
        "category_totals": category_totals,
        "expense_count": len(expenses)
    })

@app.route('/expenses/monthly', methods=['GET'])
def get_monthly():
    """Get monthly totals"""
    expenses = read_expenses()
    
    monthly_totals = {}
    for expense in expenses:
        # Extract year-month from date (e.g., "2024-01-15" -> "2024-01")
        year_month = expense['date'][:7]
        if year_month not in monthly_totals:
            monthly_totals[year_month] = 0
        monthly_totals[year_month] += expense['amount']
    
    return jsonify({"monthly_totals": monthly_totals})

if __name__ == '__main__':
    init_csv()  # Initialize CSV file when starting the app
    print("Starting Personal Expense API...")
    print("Available at: http://localhost:5000")
    app.run(debug=True, port=5000)