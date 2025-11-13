# Web Interface Implementation Guide

## Technology Stack

### Backend
- **Framework**: Flask (Python)
- **Database Connector**: mysql-connector-python or psycopg2
- **Template Engine**: Jinja2 (built into Flask)

### Frontend
- **HTML/CSS**: Bootstrap 5 or Tailwind CSS (for styling)
- **JavaScript**: Vanilla JS or jQuery
- **Charts**: Chart.js or Plotly.js
- **Icons**: Font Awesome or Bootstrap Icons

## Project Structure

```
web/
├── app.py                 # Main Flask application
├── config.py             # Database configuration
├── queries.py            # Query functions
├── templates/
│   ├── base.html        # Base template
│   ├── index.html       # Dashboard/home page
│   └── dashboard.html   # Alternative dashboard layout
├── static/
│   ├── css/
│   │   └── style.css    # Custom styles
│   ├── js/
│   │   └── charts.js    # Chart initialization
│   └── images/          # Any images/logos
└── requirements.txt      # Python dependencies
```

## Implementation Steps

### Step 1: Setup Flask Application

**app.py** - Basic structure:
```python
from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from queries import execute_query

app = Flask(__name__)

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    """Main dashboard page"""
    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
    
    try:
        # Execute queries
        monthly_revenue = execute_query(connection, 'monthly_revenue')
        service_revenue = execute_query(connection, 'service_revenue')
        occupancy_rate = execute_query(connection, 'monthly_occupancy')
        top_customers = execute_query(connection, 'top_customers')
        top_rooms = execute_query(connection, 'top_rooms')
        event_performance = execute_query(connection, 'event_performance')
        customer_retention = execute_query(connection, 'customer_retention')
        seasonal_revenue = execute_query(connection, 'seasonal_revenue')
        
        # Calculate summary statistics
        total_revenue = sum(row['total_revenue'] for row in monthly_revenue)
        avg_occupancy = sum(row['occupancy_rate'] for row in occupancy_rate) / len(occupancy_rate) if occupancy_rate else 0
        
        return render_template('index.html',
            monthly_revenue=monthly_revenue,
            service_revenue=service_revenue,
            occupancy_rate=occupancy_rate,
            top_customers=top_customers[:10],  # Top 10
            top_rooms=top_rooms[:15],  # Top 15
            event_performance=event_performance,
            customer_retention=customer_retention,
            seasonal_revenue=seasonal_revenue,
            total_revenue=total_revenue,
            avg_occupancy=avg_occupancy
        )
    except Error as e:
        return f"Error executing queries: {e}", 500
    finally:
        if connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Step 2: Database Configuration

**config.py**:
```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'last_resort_hotels',
    'user': 'your_username',
    'password': 'your_password',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}
```

### Step 3: Query Functions

**queries.py**:
```python
from mysql.connector import Error
import mysql.connector.cursor

def execute_query(connection, query_name):
    """Execute predefined queries and return results as list of dicts"""
    queries = {
        'monthly_revenue': """
            SELECT 
                DATE_FORMAT(charge_date, '%Y-%m') AS month,
                SUM(amount) AS total_revenue,
                COUNT(DISTINCT billed_party_id) AS unique_customers,
                COUNT(charge_id) AS total_charges
            FROM Charges
            WHERE charge_status IN ('billed', 'paid')
            GROUP BY DATE_FORMAT(charge_date, '%Y-%m')
            ORDER BY month
        """,
        'service_revenue': """
            SELECT 
                st.service_name,
                COUNT(c.charge_id) AS number_of_charges,
                SUM(c.amount) AS total_revenue,
                AVG(c.amount) AS average_charge
            FROM Charges c
            JOIN ServiceTypes st ON c.service_type_id = st.service_type_id
            WHERE c.charge_status IN ('billed', 'paid')
            GROUP BY st.service_name
            ORDER BY total_revenue DESC
        """,
        # Add other queries here...
    }
    
    if query_name not in queries:
        raise ValueError(f"Query '{query_name}' not found")
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(queries[query_name])
        results = cursor.fetchall()
        cursor.close()
        return results
    except Error as e:
        print(f"Error executing query {query_name}: {e}")
        raise
```

### Step 4: Base Template

**templates/base.html**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Last Resort Hotels - Management Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-hotel"></i> Last Resort Hotels - Management Dashboard
            </span>
        </div>
    </nav>
    
    <div class="container-fluid mt-4">
        {% block content %}{% endblock %}
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Step 5: Dashboard Template

**templates/index.html**:
```html
{% extends "base.html" %}

{% block content %}
<!-- Summary Cards -->
<div class="row mb-4">
    <div class="col-md-4">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <h5 class="card-title">Total Revenue</h5>
                <h2 class="card-text">${{ "{:,.2f}".format(total_revenue) }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-success">
            <div class="card-body">
                <h5 class="card-title">Average Occupancy</h5>
                <h2 class="card-text">{{ "{:.1f}".format(avg_occupancy) }}%</h2>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card text-white bg-info">
            <div class="card-body">
                <h5 class="card-title">Top Customers</h5>
                <h2 class="card-text">{{ top_customers|length }}</h2>
            </div>
        </div>
    </div>
</div>

<!-- Charts Row -->
<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5>Monthly Revenue Trend</h5>
            </div>
            <div class="card-body">
                <canvas id="revenueChart"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5>Occupancy Rate Trend</h5>
            </div>
            <div class="card-body">
                <canvas id="occupancyChart"></canvas>
            </div>
        </div>
    </div>
</div>

<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5>Revenue by Service Type</h5>
            </div>
            <div class="card-body">
                <canvas id="serviceChart"></canvas>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5>Seasonal Revenue</h5>
            </div>
            <div class="card-body">
                <canvas id="seasonalChart"></canvas>
            </div>
        </div>
    </div>
</div>

<!-- Tables Row -->
<div class="row mb-4">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5>Top Revenue-Generating Customers</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Customer</th>
                                <th>Type</th>
                                <th>Revenue</th>
                                <th>Reservations</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for customer in top_customers %}
                            <tr>
                                <td>{{ customer.customer_name }}</td>
                                <td>{{ customer.party_type }}</td>
                                <td>${{ "{:,.2f}".format(customer.total_revenue) }}</td>
                                <td>{{ customer.total_reservations }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h5>Most Booked Rooms</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Room</th>
                                <th>Building</th>
                                <th>Bookings</th>
                                <th>Revenue</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for room in top_rooms %}
                            <tr>
                                <td>{{ room.room_number }}</td>
                                <td>{{ room.building_name }}</td>
                                <td>{{ room.total_bookings }}</td>
                                <td>${{ "{:,.2f}".format(room.total_revenue_generated) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
// Revenue Chart
const revenueCtx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenueCtx, {
    type: 'line',
    data: {
        labels: {{ monthly_revenue|map(attribute='month')|list|tojson }},
        datasets: [{
            label: 'Revenue ($)',
            data: {{ monthly_revenue|map(attribute='total_revenue')|list|tojson }},
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    callback: function(value) {
                        return '$' + value.toLocaleString();
                    }
                }
            }
        }
    }
});

// Occupancy Chart
const occupancyCtx = document.getElementById('occupancyChart').getContext('2d');
const occupancyChart = new Chart(occupancyCtx, {
    type: 'line',
    data: {
        labels: {{ occupancy_rate|map(attribute='month')|list|tojson }},
        datasets: [{
            label: 'Occupancy Rate (%)',
            data: {{ occupancy_rate|map(attribute='occupancy_rate')|list|tojson }},
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                    callback: function(value) {
                        return value + '%';
                    }
                }
            }
        }
    }
});

// Service Revenue Chart
const serviceCtx = document.getElementById('serviceChart').getContext('2d');
const serviceChart = new Chart(serviceCtx, {
    type: 'pie',
    data: {
        labels: {{ service_revenue|map(attribute='service_name')|list|tojson }},
        datasets: [{
            data: {{ service_revenue|map(attribute='total_revenue')|list|tojson }},
            backgroundColor: [
                'rgba(255, 99, 132, 0.8)',
                'rgba(54, 162, 235, 0.8)',
                'rgba(255, 206, 86, 0.8)',
                'rgba(75, 192, 192, 0.8)',
                'rgba(153, 102, 255, 0.8)',
                'rgba(255, 159, 64, 0.8)'
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'right'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.label + ': $' + context.parsed.toLocaleString();
                    }
                }
            }
        }
    }
});
</script>
{% endblock %}
```

### Step 6: Custom Styling

**static/css/style.css**:
```css
body {
    background-color: #f5f5f5;
}

.card {
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.card-header {
    background-color: #343a40;
    color: white;
    font-weight: bold;
}

.table-responsive {
    max-height: 400px;
    overflow-y: auto;
}

canvas {
    max-height: 300px;
}
```

### Step 7: Requirements File

**requirements.txt**:
```
Flask==3.0.0
mysql-connector-python==8.2.0
python-dotenv==1.0.0
```

## Enhanced Features (A Level)

### 1. Interactive Date Range Selection
```python
@app.route('/dashboard')
def dashboard():
    start_date = request.args.get('start_date', default=None)
    end_date = request.args.get('end_date', default=None)
    # Modify queries to use date range
```

### 2. Export Functionality
```python
from flask import Response
import csv

@app.route('/export/<query_name>')
def export_data(query_name):
    # Execute query and return CSV
    results = execute_query(connection, query_name)
    # Generate CSV response
```

### 3. Responsive Design
- Use Bootstrap's grid system
- Mobile-friendly tables
- Collapsible sections

### 4. Additional Visualizations
- Heatmaps for room utilization
- Gauge charts for KPIs
- Sparklines for trends

## Testing Checklist

- [ ] Database connection works
- [ ] All queries execute without errors
- [ ] Data displays correctly in tables
- [ ] Charts render properly
- [ ] Currency formatting is correct
- [ ] Date formatting is consistent
- [ ] Page loads in reasonable time
- [ ] No JavaScript errors in console
- [ ] Responsive on mobile devices
- [ ] All 8+ queries are displayed

## Deployment Notes

### Local Development
```bash
python app.py
```

### Production Considerations
- Use environment variables for database credentials
- Enable error logging
- Use production WSGI server (gunicorn)
- Set up proper security headers
- Use HTTPS

## Security Best Practices

1. **Database Credentials**: Store in environment variables, not in code
2. **SQL Injection**: Use parameterized queries (already done with dictionary cursor)
3. **Error Handling**: Don't expose database errors to users
4. **Input Validation**: Even for static queries, validate any user input

## Performance Optimization

1. **Query Optimization**: Ensure indexes are in place
2. **Caching**: Consider caching query results for static dashboards
3. **Connection Pooling**: For production use connection pooling
4. **Lazy Loading**: Load charts asynchronously if needed



