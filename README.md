# Personal Expense API

A simple Flask API for tracking personal expenses and income.

## Developer
**Eid Muhammad**
- Backend API Development (Flask)
- Data Storage & Persistence (CSV)
- API Testing & Validation
- Documentation & Deployment
## Installation

1. Make sure you have Python 3.7+ installed
2. Open the project folder in VSCode
3. Open terminal in VSCode (Terminal → New Terminal)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The server will start at: http://localhost:5000

## API Documentation

### Setup Instructions
1. Install Python 3.7+
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python app.py`
4. Access API at: http://localhost:5000

### Testing the API
Use Thunder Client or any API testing tool:

**Add Expense (POST /expenses)**
```json
{
    "amount": 25.50,
    "date": "2024-01-15",
    "category": "food",
    "description": "Lunch at cafe"
}
```

**Available Categories:** food, transport, entertainment, utilities, health, other

### API Endpoints

#### GET /
Returns API information and available endpoints.

#### POST /expenses
Add a new expense.

**Body (JSON):**
```json
{
    "amount": 25.50,
    "date": "2024-01-15",
    "category": "food",
    "description": "Lunch at cafe"
}
```

#### GET /expenses
Get all expenses. Optional query parameters:
- `start_date`: Filter from date (YYYY-MM-DD)
- `end_date`: Filter to date (YYYY-MM-DD)
- `category`: Filter by category

#### GET /expenses/summary
Get summary with total amount and category breakdown.

#### GET /expenses/monthly
Get monthly totals.

## Example Usage

**Add an expense:**
```bash
POST http://localhost:5000/expenses
Content-Type: application/json

{
    "amount": 45.00,
    "date": "2024-01-16",
    "category": "transport",
    "description": "Bus pass"
}
```

**View all expenses:**
```bash
GET http://localhost:5000/expenses
```

**Get spending summary:**
```bash
GET http://localhost:5000/expenses/summary
```

**Get monthly breakdown:**
```bash
GET http://localhost:5000/expenses/monthly
```

## Data Storage
All data is stored in `expenses.csv` file. No database required. The file is automatically created when you first run the application.

