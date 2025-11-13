# Last Resort Hotels - Prototype Website

## Overview
This is a prototype website that displays management dashboard queries using **mock data**. The data can be easily modified in `app.py` and later replaced with real database queries.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Website
Open your browser and navigate to:
```
http://localhost:5000
```

## Current Features

### Dashboard Components
- **Summary Cards**: Total Revenue, Average Occupancy, Top Customers count
- **Charts**:
  - Monthly Revenue Trend (Line Chart)
  - Occupancy Rate Trend (Line Chart)
  - Revenue by Service Type (Pie Chart)
  - Seasonal Revenue Analysis (Bar Chart)
- **Tables**:
  - Top Revenue-Generating Customers
  - Most Booked Rooms
  - Event Performance
  - Customer Retention

## Modifying Mock Data

All mock data is generated in `app.py` using functions like:
- `generate_monthly_revenue()`
- `generate_service_revenue()`
- `generate_occupancy_rate()`
- `generate_top_customers()`
- etc.

To modify the data, simply edit these functions in `app.py`. For example:

```python
def generate_top_customers():
    customers = [
        {'customer_name': 'Your Company', 'party_type': 'organization', 
         'total_revenue': 100000, 'total_reservations': 10, 'last_visit_date': '2024-11-20'},
        # Add more customers...
    ]
    return customers
```

## Converting to Real Database Queries

When you're ready to connect to a real database:

### Step 1: Create config.py
Copy `config.example.py` to `config.py` and update with your database credentials.

### Step 2: Update app.py
Replace the mock data functions with database queries:

```python
from config import DB_CONFIG
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def get_monthly_revenue():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            DATE_FORMAT(charge_date, '%Y-%m') AS month,
            SUM(amount) AS total_revenue,
            COUNT(DISTINCT billed_party_id) AS unique_customers,
            COUNT(charge_id) AS total_charges
        FROM Charges
        WHERE charge_status IN ('billed', 'paid')
        GROUP BY DATE_FORMAT(charge_date, '%Y-%m')
        ORDER BY month
    """)
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results
```

### Step 3: Update the route
```python
@app.route('/')
def index():
    # Replace mock functions with real queries
    monthly_revenue = get_monthly_revenue()  # Instead of generate_monthly_revenue()
    # ... etc
```

## Project Structure

```
groupproject/
├── app.py                 # Main Flask application (with mock data)
├── requirements.txt       # Python dependencies
├── config.example.py      # Database config template
├── templates/
│   ├── base.html         # Base template
│   └── index.html        # Dashboard page
└── static/
    └── css/
        └── style.css     # Custom styles
```

## Features

- ✅ Responsive design (works on mobile and desktop)
- ✅ Interactive charts using Chart.js
- ✅ Professional styling with Bootstrap 5
- ✅ Scrollable tables with sticky headers
- ✅ Easy to modify mock data
- ✅ Ready to connect to real database

## Next Steps

1. **Customize the mock data** to match your expected data structure
2. **Test the interface** and adjust styling as needed
3. **When database is ready**, replace mock functions with real queries
4. **Add more queries** as needed for your project requirements

## Notes

- The prototype uses mock data, so no database connection is required
- All data is generated dynamically on each page load
- Charts are interactive (hover to see details)
- Tables are scrollable for better UX
- The design is ready for A-level work with enhancements

## Troubleshooting

### Port already in use
If port 5000 is busy, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Charts not displaying
- Check browser console for JavaScript errors
- Ensure Chart.js is loading (check network tab)
- Verify data is being passed correctly to templates

### Styling issues
- Clear browser cache
- Check that `static/css/style.css` is loading
- Verify Bootstrap CDN is accessible



