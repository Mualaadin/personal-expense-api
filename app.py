from flask import Flask, request, jsonify
import os
from datetime import datetime
from typing import List, Dict
from database import db
from init_db import init_database

app = Flask(__name__)

# Configuration
CATEGORIES = ['food', 'transport', 'entertainment', 'utilities', 'health', 'other']

@app.route('/')
def home():
    return jsonify({
        "message": "Personal Expense API (Docker + PostgreSQL)",
        "endpoints": {
            "add_expense": "POST /expenses",
            "get_expenses": "GET /expenses",
            "get_summary": "GET /expenses/summary",
            "get_monthly": "GET /expenses/monthly",
            "health_check": "GET /health"
        }
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        db.get_connection().close()
        return jsonify({"status": "OK", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "ERROR", "database": "disconnected", "error": str(e)}), 500

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
        'id': db.get_next_id(),
        'amount': amount,
        'date': data['date'],
        'category': data['category'],
        'description': data['description']
    }
    
    # Save to database
    expense_id = db.write_expense(expense)
    
    return jsonify({
        "message": "Expense added successfully", 
        "expense": {**expense, 'id': expense_id}
    }), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    """Get all expenses with optional filtering"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')
    
    expenses = db.read_expenses(start_date, end_date, category)
    
    return jsonify({
        "count": len(expenses),
        "expenses": expenses
    })

@app.route('/expenses/summary', methods=['GET'])
def get_summary():
    """Get summary by category"""
    category_totals = db.get_category_totals()
    total_amount = db.get_total_amount()
    expenses = db.read_expenses()
    
    return jsonify({
        "total_amount": total_amount,
        "category_totals": category_totals,
        "expense_count": len(expenses)
    })

@app.route('/expenses/monthly', methods=['GET'])
def get_monthly():
    """Get monthly totals"""
    monthly_totals = db.get_monthly_totals()
    return jsonify({"monthly_totals": monthly_totals})

# Initialize database when starting the app
with app.app_context():
    init_database()

if __name__ == '__main__':
    print("Starting Personal Expense API with PostgreSQL...")
    print("Available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
