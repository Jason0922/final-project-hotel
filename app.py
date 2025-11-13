from flask import Flask, render_template
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Mock data generator functions
def generate_monthly_revenue():
    """Generate mock monthly revenue data"""
    months = []
    base_revenue = 50000
    for i in range(12):
        month_date = datetime(2024, 1, 1) + timedelta(days=30*i)
        months.append({
            'month': month_date.strftime('%Y-%m'),
            'total_revenue': base_revenue + random.randint(-10000, 15000),
            'unique_customers': random.randint(45, 80),
            'total_charges': random.randint(200, 400)
        })
    return months

def generate_service_revenue():
    """Generate mock service revenue data"""
    services = [
        {'service_name': 'meal', 'number_of_charges': 450, 'total_revenue': 67500, 'average_charge': 150.00},
        {'service_name': 'phone', 'number_of_charges': 320, 'total_revenue': 4800, 'average_charge': 15.00},
        {'service_name': 'business_service', 'number_of_charges': 180, 'total_revenue': 5400, 'average_charge': 30.00},
        {'service_name': 'room_service', 'number_of_charges': 250, 'total_revenue': 12500, 'average_charge': 50.00},
        {'service_name': 'retail', 'number_of_charges': 150, 'total_revenue': 22500, 'average_charge': 150.00},
        {'service_name': 'health_club', 'number_of_charges': 200, 'total_revenue': 4000, 'average_charge': 20.00}
    ]
    return services

def generate_occupancy_rate():
    """Generate mock occupancy rate data"""
    months = []
    base_occupancy = 65
    for i in range(12):
        month_date = datetime(2024, 1, 1) + timedelta(days=30*i)
        months.append({
            'month': month_date.strftime('%Y-%m'),
            'total_stays': random.randint(80, 120),
            'unique_rooms_occupied': random.randint(60, 90),
            'total_available_rooms': 100,
            'occupancy_rate': base_occupancy + random.randint(-10, 15)
        })
    return months

def generate_top_customers():
    """Generate mock top customers data"""
    customers = [
        {'customer_name': 'Acme Corporation', 'party_type': 'organization', 'total_revenue': 125000, 'total_reservations': 15, 'last_visit_date': '2024-11-15'},
        {'customer_name': 'John Smith', 'party_type': 'guest', 'total_revenue': 85000, 'total_reservations': 8, 'last_visit_date': '2024-11-20'},
        {'customer_name': 'Tech Solutions Inc.', 'party_type': 'organization', 'total_revenue': 78000, 'total_reservations': 12, 'last_visit_date': '2024-11-18'},
        {'customer_name': 'Sarah Johnson', 'party_type': 'guest', 'total_revenue': 65000, 'total_reservations': 6, 'last_visit_date': '2024-11-22'},
        {'customer_name': 'Global Events LLC', 'party_type': 'organization', 'total_revenue': 58000, 'total_reservations': 5, 'last_visit_date': '2024-11-10'},
        {'customer_name': 'Michael Brown', 'party_type': 'guest', 'total_revenue': 52000, 'total_reservations': 7, 'last_visit_date': '2024-11-25'},
        {'customer_name': 'Emily Davis', 'party_type': 'guest', 'total_revenue': 48000, 'total_reservations': 5, 'last_visit_date': '2024-11-12'},
        {'customer_name': 'Conference Organizers', 'party_type': 'organization', 'total_revenue': 45000, 'total_reservations': 4, 'last_visit_date': '2024-11-08'},
        {'customer_name': 'David Wilson', 'party_type': 'guest', 'total_revenue': 42000, 'total_reservations': 6, 'last_visit_date': '2024-11-19'},
        {'customer_name': 'Corporate Travel Co.', 'party_type': 'organization', 'total_revenue': 40000, 'total_reservations': 8, 'last_visit_date': '2024-11-14'}
    ]
    return customers

def generate_top_rooms():
    """Generate mock top rooms data"""
    rooms = [
        {'room_number': '1201', 'building_name': 'Main Building', 'total_bookings': 45, 'total_revenue_generated': 67500},
        {'room_number': '0805', 'building_name': 'Main Building', 'total_bookings': 42, 'total_revenue_generated': 63000},
        {'room_number': '1503', 'building_name': 'Tower Wing', 'total_bookings': 40, 'total_revenue_generated': 60000},
        {'room_number': '2101', 'building_name': 'Luxury Tower', 'total_bookings': 38, 'total_revenue_generated': 95000},
        {'room_number': '0902', 'building_name': 'Main Building', 'total_bookings': 36, 'total_revenue_generated': 54000},
        {'room_number': '1705', 'building_name': 'Tower Wing', 'total_bookings': 35, 'total_revenue_generated': 52500},
        {'room_number': '2203', 'building_name': 'Luxury Tower', 'total_bookings': 34, 'total_revenue_generated': 85000},
        {'room_number': '1104', 'building_name': 'Main Building', 'total_bookings': 33, 'total_revenue_generated': 49500},
        {'room_number': '1608', 'building_name': 'Tower Wing', 'total_bookings': 32, 'total_revenue_generated': 48000},
        {'room_number': '2301', 'building_name': 'Luxury Tower', 'total_bookings': 30, 'total_revenue_generated': 75000},
        {'room_number': '1007', 'building_name': 'Main Building', 'total_bookings': 29, 'total_revenue_generated': 43500},
        {'room_number': '1802', 'building_name': 'Tower Wing', 'total_bookings': 28, 'total_revenue_generated': 42000},
        {'room_number': '2005', 'building_name': 'Luxury Tower', 'total_bookings': 27, 'total_revenue_generated': 67500},
        {'room_number': '1306', 'building_name': 'Main Building', 'total_bookings': 26, 'total_revenue_generated': 39000},
        {'room_number': '1909', 'building_name': 'Tower Wing', 'total_bookings': 25, 'total_revenue_generated': 37500}
    ]
    return rooms

def generate_event_performance():
    """Generate mock event performance data"""
    events = [
        {'event_name': 'Tech Conference 2024', 'host_organization': 'Tech Solutions Inc.', 'rooms_used': 5, 'time_slots_used': 12, 'estimated_attendance': 500, 'eating_slots': 8, 'non_eating_slots': 4, 'guest_reservations_generated': 120, 'total_event_revenue': 45000},
        {'event_name': 'Annual Corporate Meeting', 'host_organization': 'Acme Corporation', 'rooms_used': 3, 'time_slots_used': 8, 'estimated_attendance': 300, 'eating_slots': 5, 'non_eating_slots': 3, 'guest_reservations_generated': 80, 'total_event_revenue': 32000},
        {'event_name': 'Wedding Reception', 'host_organization': 'Private Event', 'rooms_used': 2, 'time_slots_used': 6, 'estimated_attendance': 200, 'eating_slots': 4, 'non_eating_slots': 2, 'guest_reservations_generated': 50, 'total_event_revenue': 25000},
        {'event_name': 'Product Launch', 'host_organization': 'Global Events LLC', 'rooms_used': 4, 'time_slots_used': 10, 'estimated_attendance': 400, 'eating_slots': 6, 'non_eating_slots': 4, 'guest_reservations_generated': 100, 'total_event_revenue': 38000},
        {'event_name': 'Training Workshop', 'host_organization': 'Corporate Training Co.', 'rooms_used': 2, 'time_slots_used': 5, 'estimated_attendance': 150, 'eating_slots': 3, 'non_eating_slots': 2, 'guest_reservations_generated': 40, 'total_event_revenue': 18000}
    ]
    return events

def generate_customer_retention():
    """Generate mock customer retention data"""
    customers = [
        {'guest_name': 'John Smith', 'total_visits': 8, 'first_visit': '2023-01-15', 'last_visit': '2024-11-20', 'days_between_first_last': 675, 'total_nights': 24, 'avg_nights_per_visit': 3.0},
        {'guest_name': 'Sarah Johnson', 'total_visits': 6, 'first_visit': '2023-03-20', 'last_visit': '2024-11-22', 'days_between_first_last': 612, 'total_nights': 18, 'avg_nights_per_visit': 3.0},
        {'guest_name': 'Michael Brown', 'total_visits': 7, 'first_visit': '2023-05-10', 'last_visit': '2024-11-25', 'days_between_first_last': 564, 'total_nights': 21, 'avg_nights_per_visit': 3.0},
        {'guest_name': 'Emily Davis', 'total_visits': 5, 'first_visit': '2023-07-05', 'last_visit': '2024-11-12', 'days_between_first_last': 495, 'total_nights': 15, 'avg_nights_per_visit': 3.0},
        {'guest_name': 'David Wilson', 'total_visits': 6, 'first_visit': '2023-09-18', 'last_visit': '2024-11-19', 'days_between_first_last': 428, 'total_nights': 18, 'avg_nights_per_visit': 3.0}
    ]
    return customers

def generate_seasonal_revenue():
    """Generate mock seasonal revenue data"""
    seasons = [
        {'season': 'Winter', 'year': 2023, 'total_charges': 1250, 'total_revenue': 187500, 'avg_charge_amount': 150.00, 'unique_customers': 85},
        {'season': 'Spring', 'year': 2024, 'total_charges': 1380, 'total_revenue': 207000, 'avg_charge_amount': 150.00, 'unique_customers': 92},
        {'season': 'Summer', 'year': 2024, 'total_charges': 1520, 'total_revenue': 228000, 'avg_charge_amount': 150.00, 'unique_customers': 105},
        {'season': 'Fall', 'year': 2024, 'total_charges': 1450, 'total_revenue': 217500, 'avg_charge_amount': 150.00, 'unique_customers': 98}
    ]
    return seasons

@app.route('/')
def index():
    """Main dashboard page"""
    # Generate mock data
    monthly_revenue = generate_monthly_revenue()
    service_revenue = generate_service_revenue()
    occupancy_rate = generate_occupancy_rate()
    top_customers = generate_top_customers()
    top_rooms = generate_top_rooms()
    event_performance = generate_event_performance()
    customer_retention = generate_customer_retention()
    seasonal_revenue = generate_seasonal_revenue()
    
    # Calculate summary statistics
    total_revenue = sum(row['total_revenue'] for row in monthly_revenue)
    avg_occupancy = sum(row['occupancy_rate'] for row in occupancy_rate) / len(occupancy_rate) if occupancy_rate else 0
    unique_customers_count = len(top_customers)
    
    return render_template('index.html',
        monthly_revenue=monthly_revenue,
        service_revenue=service_revenue,
        occupancy_rate=occupancy_rate,
        top_customers=top_customers,
        top_rooms=top_rooms,
        event_performance=event_performance,
        customer_retention=customer_retention,
        seasonal_revenue=seasonal_revenue,
        total_revenue=total_revenue,
        avg_occupancy=avg_occupancy,
        unique_customers_count=unique_customers_count
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



