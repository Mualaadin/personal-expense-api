# Personal Expense API

A simple Flask API for tracking personal expenses and income.

## 🚀 Docker Upgrade (New!)
The API now supports Docker containerization with PostgreSQL database for better scalability and deployment.

### Quick Start with Docker
```bash
# Start the application with database
docker-compose up --build

# Access the API at: http://localhost:5000
```

### New Features Added:
- ✅ Docker containerization
- ✅ PostgreSQL database
- ✅ Environment variables configuration
- ✅ Health check endpoint (`GET /health`)
- ✅ Same API compatibility maintained

## Developer
**Eid Muhammad**
- Backend API Development (Flask)
- Data Storage & Persistence (CSV → PostgreSQL + Docker Upgrade)
- API Testing & Validation
- Documentation & Deployment

## Installation

### Option 1: Docker (Recommended)
```bash
docker-compose up --build
```

### Option 2: Traditional Setup
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

#### GET /health *(New!)*
Check API and database connection status.

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

**Check health status:** *(New!)*
```bash
GET http://localhost:5000/health
```

## Data Storage
**Upgraded from CSV to PostgreSQL database** for better reliability and scalability. The database is automatically initialized when using Docker Compose.

### Environment Configuration *(New!)*
The application now uses environment variables for database configuration:
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
