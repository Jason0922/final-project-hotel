from flask import Flask, render_template
from datetime import datetime, timedelta
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_path():
    try:
        import config
        return config.DB_PATH
    except (ImportError, AttributeError):
        return os.getenv('DB_PATH', 'last_resort_hotels.db')

def get_db_connection():
    db_path = get_db_path()
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def get_total_revenue():
    connection = get_db_connection()
    if not connection:
        return 0.0
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT SUM(amount) AS total_revenue
            FROM Charges
            WHERE charge_status IN ('billed', 'paid')
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return float(result[0]) if result and result[0] else 0.0
    except sqlite3.Error as e:
        print(f"Error executing total revenue query: {e}")
        return 0.0
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_quarterly_revenue():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                CAST(strftime('%Y', c.charge_date) AS INTEGER) AS revenue_year,
                CAST((CAST(strftime('%m', c.charge_date) AS INTEGER) - 1) / 3 + 1 AS INTEGER) AS revenue_quarter,
                SUM(c.amount) AS total_revenue
            FROM Charges c
            WHERE c.charge_status = 'paid'
            GROUP BY 
                strftime('%Y', c.charge_date),
                revenue_quarter
            ORDER BY 
                revenue_year,
                revenue_quarter
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['revenue_year'] = int(row['revenue_year']) if row['revenue_year'] else 0
            row['revenue_quarter'] = int(row['revenue_quarter']) if row['revenue_quarter'] else 0
            row['total_revenue'] = float(row['total_revenue']) if row['total_revenue'] else 0.0
            row['quarter'] = f"{row['revenue_year']}-Q{row['revenue_quarter']}"
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing quarterly revenue query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_occupancy_rate_daily():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                DATE(ra.check_in_time) AS date,
                COUNT(DISTINCT ra.assignment_id) AS total_stays,
                COUNT(DISTINCT ra.room_id) AS unique_rooms_occupied,
                (SELECT COUNT(*) FROM Rooms WHERE room_status != 'renovation') AS total_available_rooms,
                (COUNT(DISTINCT ra.room_id) * 100.0 / 
                 MAX((SELECT COUNT(*) FROM Rooms WHERE room_status != 'renovation'), 1)) AS occupancy_rate
            FROM RoomAssignments ra
            WHERE ra.check_in_time IS NOT NULL
            GROUP BY date(ra.check_in_time)
            ORDER BY date DESC
            LIMIT 90
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['total_stays'] = int(row['total_stays']) if row['total_stays'] else 0
            row['unique_rooms_occupied'] = int(row['unique_rooms_occupied']) if row['unique_rooms_occupied'] else 0
            row['total_available_rooms'] = int(row['total_available_rooms']) if row['total_available_rooms'] else 0
            row['occupancy_rate'] = float(row['occupancy_rate']) if row['occupancy_rate'] else 0.0
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing daily occupancy query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_occupancy_rate_monthly():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                strftime('%Y-%m', ra.check_in_time) AS month,
                COUNT(DISTINCT ra.assignment_id) AS total_stays,
                COUNT(DISTINCT ra.room_id) AS unique_rooms_occupied,
                (SELECT COUNT(*) FROM Rooms WHERE room_status != 'renovation') AS total_available_rooms,
                (COUNT(DISTINCT ra.room_id) * 100.0 / 
                 MAX((SELECT COUNT(*) FROM Rooms WHERE room_status != 'renovation'), 1)) AS occupancy_rate
            FROM RoomAssignments ra
            WHERE ra.check_in_time IS NOT NULL
            GROUP BY strftime('%Y-%m', ra.check_in_time)
            ORDER BY month
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['total_stays'] = int(row['total_stays']) if row['total_stays'] else 0
            row['unique_rooms_occupied'] = int(row['unique_rooms_occupied']) if row['unique_rooms_occupied'] else 0
            row['total_available_rooms'] = int(row['total_available_rooms']) if row['total_available_rooms'] else 0
            row['occupancy_rate'] = float(row['occupancy_rate']) if row['occupancy_rate'] else 0.0
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing monthly occupancy query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_top_customers():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                bp.billed_party_id,
                COALESCE(bp.organization_name, bp.first_name || ' ' || bp.last_name) AS customer_name,
                bp.party_type,
                SUM(c.amount) AS total_revenue,
                COUNT(DISTINCT res.reservation_id) AS total_reservations,
                MAX(res.check_in_date) AS last_visit_date
            FROM BilledParties bp
            LEFT JOIN Charges c ON bp.billed_party_id = c.billed_party_id AND c.charge_status IN ('billed', 'paid')
            LEFT JOIN Reservations res ON bp.billed_party_id = res.billed_party_id
            GROUP BY bp.billed_party_id, customer_name, bp.party_type
            HAVING total_revenue > 0
            ORDER BY total_revenue DESC
            LIMIT 20
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['total_revenue'] = float(row['total_revenue']) if row['total_revenue'] else 0.0
            row['total_reservations'] = int(row['total_reservations']) if row['total_reservations'] else 0
            if row['last_visit_date']:
                row['last_visit_date'] = row['last_visit_date']
            else:
                row['last_visit_date'] = None
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing top customers query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_high_risk_customers():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                cq.billed_party_id,
                COALESCE(bp.first_name || ' ' || bp.last_name, bp.organization_name) AS customer_name,
                bp.party_type,
                cq.past_history_score,
                cq.cooperativeness_score,
                cq.flexibility_score,
                cq.payment_promptness_score,
                cq.overall_qualification_score,
                (0.4 * (100 - cq.payment_promptness_score) +
                 0.3 * (100 - cq.past_history_score) +
                 0.2 * (100 - cq.cooperativeness_score) +
                 0.1 * (100 - cq.flexibility_score)) AS risk_score,
                COUNT(DISTINCT res.reservation_id) AS total_reservations,
                COALESCE(SUM(CASE WHEN b.bill_status = 'overdue' THEN b.total_amount ELSE 0 END), 0) AS overdue_amount,
                MAX(res.check_in_date) AS last_visit_date
            FROM CustomerQualifications cq
            JOIN BilledParties bp ON cq.billed_party_id = bp.billed_party_id
            LEFT JOIN Reservations res ON bp.billed_party_id = res.billed_party_id
            LEFT JOIN Bills b ON bp.billed_party_id = b.billed_party_id
            GROUP BY cq.billed_party_id, customer_name, bp.party_type,
                     cq.past_history_score, cq.cooperativeness_score,
                     cq.flexibility_score, cq.payment_promptness_score,
                     cq.overall_qualification_score
            ORDER BY risk_score DESC
            LIMIT 50
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['past_history_score'] = int(row['past_history_score']) if row['past_history_score'] else 0
            row['cooperativeness_score'] = int(row['cooperativeness_score']) if row['cooperativeness_score'] else 0
            row['flexibility_score'] = int(row['flexibility_score']) if row['flexibility_score'] else 0
            row['payment_promptness_score'] = int(row['payment_promptness_score']) if row['payment_promptness_score'] else 0
            row['overall_qualification_score'] = float(row['overall_qualification_score']) if row['overall_qualification_score'] else 0.0
            row['risk_score'] = float(row['risk_score']) if row['risk_score'] else 0.0
            row['total_reservations'] = int(row['total_reservations']) if row['total_reservations'] else 0
            row['overdue_amount'] = float(row['overdue_amount']) if row['overdue_amount'] else 0.0
            if row['last_visit_date']:
                row['last_visit_date'] = row['last_visit_date']
            else:
                row['last_visit_date'] = None
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing high-risk customers query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_event_count_by_month():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                strftime('%Y-%m', e.start_date) AS month,
                COUNT(DISTINCT e.event_id) AS total_events,
                SUM(e.estimated_attendance) AS total_estimated_attendance,
                AVG(e.estimated_attendance) AS avg_attendance_per_event,
                COUNT(DISTINCT e.host_id) AS unique_hosts
            FROM Events e
            WHERE e.start_date IS NOT NULL
            GROUP BY strftime('%Y-%m', e.start_date)
            ORDER BY month
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['total_events'] = int(row['total_events']) if row['total_events'] else 0
            row['total_estimated_attendance'] = int(row['total_estimated_attendance']) if row['total_estimated_attendance'] else 0
            row['avg_attendance_per_event'] = float(row['avg_attendance_per_event']) if row['avg_attendance_per_event'] else 0.0
            row['unique_hosts'] = int(row['unique_hosts']) if row['unique_hosts'] else 0
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing event count by month query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_average_attendance():
    connection = get_db_connection()
    if not connection:
        return {}
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                COUNT(DISTINCT e.event_id) AS total_events,
                AVG(e.estimated_attendance) AS avg_estimated_attendance,
                AVG(er.actual_attendance) AS avg_actual_attendance,
                SUM(e.estimated_attendance) AS total_estimated_attendance,
                SUM(er.actual_attendance) AS total_actual_attendance
            FROM Events e
            LEFT JOIN EventRooms er ON e.event_id = er.event_id
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            result = dict(result)
            return {
                'total_events': int(result['total_events']) if result['total_events'] else 0,
                'avg_estimated_attendance': float(result['avg_estimated_attendance']) if result['avg_estimated_attendance'] else 0.0,
                'avg_actual_attendance': float(result['avg_actual_attendance']) if result['avg_actual_attendance'] else 0.0,
                'total_estimated_attendance': int(result['total_estimated_attendance']) if result['total_estimated_attendance'] else 0,
                'total_actual_attendance': int(result['total_actual_attendance']) if result['total_actual_attendance'] else 0
            }
        return {}
    except sqlite3.Error as e:
        print(f"Error executing average attendance query: {e}")
        return {}
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_avg_fb_spend_per_guest():
    connection = get_db_connection()
    if not connection:
        return {}
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                COUNT(DISTINCT c.billed_party_id) AS total_guests_with_fb,
                COUNT(DISTINCT mc.meal_charge_id) AS total_meal_charges,
                SUM(c.amount) AS total_fb_revenue,
                AVG(c.amount) AS avg_fb_spend_per_charge,
                SUM(c.amount) / COUNT(DISTINCT c.billed_party_id) AS avg_fb_spend_per_guest
            FROM Charges c
            JOIN MealCharges mc ON c.charge_id = mc.charge_id
            WHERE c.charge_status IN ('billed', 'paid')
        """
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            result = dict(result)
            return {
                'total_guests_with_fb': int(result['total_guests_with_fb']) if result['total_guests_with_fb'] else 0,
                'total_meal_charges': int(result['total_meal_charges']) if result['total_meal_charges'] else 0,
                'total_fb_revenue': float(result['total_fb_revenue']) if result['total_fb_revenue'] else 0.0,
                'avg_fb_spend_per_charge': float(result['avg_fb_spend_per_charge']) if result['avg_fb_spend_per_charge'] else 0.0,
                'avg_fb_spend_per_guest': float(result['avg_fb_spend_per_guest']) if result['avg_fb_spend_per_guest'] else 0.0
            }
        return {}
    except sqlite3.Error as e:
        print(f"Error executing avg F&B spend query: {e}")
        return {}
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_fb_revenue_by_meal_type():
    """Get F&B revenue by meal type"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
            SELECT 
                mc.meal_type,
                COUNT(mc.meal_charge_id) AS total_charges,
                SUM(c.amount) AS total_revenue,
                AVG(c.amount) AS avg_charge_amount,
                COUNT(DISTINCT c.billed_party_id) AS unique_customers,
                SUM(c.amount) * 100.0 / (
                    SELECT SUM(amount) 
                    FROM Charges c2
                    JOIN MealCharges mc2 ON c2.charge_id = mc2.charge_id
                    WHERE c2.charge_status IN ('billed', 'paid')
                ) AS percentage_of_total_fb
            FROM MealCharges mc
            JOIN Charges c ON mc.charge_id = c.charge_id
            WHERE c.charge_status IN ('billed', 'paid')
            GROUP BY mc.meal_type
            ORDER BY total_revenue DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        results = [dict(row) for row in results]
        
        for row in results:
            row['total_charges'] = int(row['total_charges']) if row['total_charges'] else 0
            row['total_revenue'] = float(row['total_revenue']) if row['total_revenue'] else 0.0
            row['avg_charge_amount'] = float(row['avg_charge_amount']) if row['avg_charge_amount'] else 0.0
            row['unique_customers'] = int(row['unique_customers']) if row['unique_customers'] else 0
            row['percentage_of_total_fb'] = float(row['percentage_of_total_fb']) if row['percentage_of_total_fb'] else 0.0
        
        return results
    except sqlite3.Error as e:
        print(f"Error executing F&B revenue by meal type query: {e}")
        return []
    finally:
        if connection:
            cursor.close()
            connection.close()

def get_summary_stats():
    total_revenue = get_total_revenue()
    quarterly_revenue = get_quarterly_revenue()
    occupancy_daily = get_occupancy_rate_daily()
    occupancy_monthly = get_occupancy_rate_monthly()
    top_customers = get_top_customers()
    high_risk_customers = get_high_risk_customers()
    event_count_by_month = get_event_count_by_month()
    average_attendance = get_average_attendance()
    avg_fb_spend = get_avg_fb_spend_per_guest()
    fb_revenue_by_meal = get_fb_revenue_by_meal_type()
    
    avg_occupancy_monthly = sum(row['occupancy_rate'] for row in occupancy_monthly) / len(occupancy_monthly) if occupancy_monthly else 0
    
    connection = get_db_connection()
    unique_customers_count = 0
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT COUNT(DISTINCT billed_party_id) 
                FROM Reservations 
                WHERE reservation_status IN ('confirmed', 'checked_in', 'checked_out')
            """)
            unique_customers_count = cursor.fetchone()[0] or 0
            cursor.close()
        except:
            unique_customers_count = len(top_customers) if top_customers else 0
        finally:
            connection.close()
    else:
        unique_customers_count = len(top_customers) if top_customers else 0
    
    return {
        'total_revenue': total_revenue,
        'quarterly_revenue': quarterly_revenue,
        'occupancy_daily': occupancy_daily,
        'occupancy_monthly': occupancy_monthly,
        'top_customers': top_customers,
        'high_risk_customers': high_risk_customers,
        'event_count_by_month': event_count_by_month,
        'average_attendance': average_attendance,
        'avg_fb_spend': avg_fb_spend,
        'fb_revenue_by_meal': fb_revenue_by_meal,
        'avg_occupancy_monthly': avg_occupancy_monthly,
        'unique_customers_count': unique_customers_count
    }

@app.route('/')
def summary():
    stats = get_summary_stats()
    return render_template('summary.html', **stats)

@app.route('/dashboard')
def dashboard():
    stats = get_summary_stats()
    return render_template('index.html', **stats)

@app.route('/revenue/total')
def total_revenue_detail():
    total_revenue = get_total_revenue()
    quarterly_revenue = get_quarterly_revenue()
    
    return render_template('metric_detail.html',
        metric_title='Total Revenue',
        metric_icon='fas fa-dollar-sign',
        metric_description='Total revenue overview',
        summary_card={
            'title': 'Total Revenue',
            'value': f'${total_revenue:,.2f}',
            'subtitle': f'{len(quarterly_revenue)} quarters tracked',
            'icon': 'fas fa-dollar-sign',
            'color': 'bg-primary'
        },
        chart_data=[row['total_revenue'] for row in quarterly_revenue],
        chart_labels=[row['quarter'] for row in quarterly_revenue],
        chart_type='bar',
        chart_title='Quarterly Revenue Trend',
        chart_icon='fas fa-chart-bar',
        chart_dataset_label='Revenue ($)',
        chart_bg_color='rgba(54, 162, 235, 0.8)',
        chart_border_color='rgba(54, 162, 235, 1)',
        chart_legend_position='top',
        chart_y_format='currency',
        table_data=quarterly_revenue,
        table_title='Quarterly Revenue Data',
        table_headers=['Year', 'Quarter', 'Total Revenue']
    )

@app.route('/revenue/quarterly')
def quarterly_revenue_detail():
    quarterly_revenue = get_quarterly_revenue()
    total_revenue = sum(row['total_revenue'] for row in quarterly_revenue) if quarterly_revenue else 0
    
    return render_template('metric_detail.html',
        metric_title='Quarterly Revenue Analysis',
        metric_icon='fas fa-chart-bar',
        metric_description='Revenue analysis by quarter',
        summary_card={
            'title': 'Total Quarterly Revenue',
            'value': f'${total_revenue:,.2f}',
            'subtitle': f'{len(quarterly_revenue)} quarters',
            'icon': 'fas fa-dollar-sign',
            'color': 'bg-info'
        },
        chart_data=[row['total_revenue'] for row in quarterly_revenue],
        chart_labels=[row['quarter'] for row in quarterly_revenue],
        chart_type='bar',
        chart_title='Quarterly Revenue Analysis',
        chart_icon='fas fa-chart-bar',
        chart_dataset_label='Revenue ($)',
        chart_bg_color='rgba(54, 162, 235, 0.8)',
        chart_border_color='rgba(54, 162, 235, 1)',
        chart_legend_position='top',
        chart_y_format='currency',
        table_data=quarterly_revenue,
        table_title='Quarterly Revenue Data',
        table_headers=['Year', 'Quarter', 'Total Revenue']
    )

@app.route('/occupancy/daily')
def occupancy_daily_detail():
    occupancy_daily = get_occupancy_rate_daily()
    avg_occupancy = sum(row['occupancy_rate'] for row in occupancy_daily) / len(occupancy_daily) if occupancy_daily else 0
    
    return render_template('metric_detail.html',
        metric_title='Daily Occupancy Rate',
        metric_icon='fas fa-calendar-day',
        metric_description='Daily room occupancy trends',
        summary_card={
            'title': 'Average Daily Occupancy',
            'value': f'{avg_occupancy:.1f}%',
            'subtitle': f'{len(occupancy_daily)} days tracked',
            'icon': 'fas fa-bed',
            'color': 'bg-success'
        },
        chart_data=[row['occupancy_rate'] for row in occupancy_daily],
        chart_labels=[str(row['date']) for row in occupancy_daily],
        chart_type='line',
        chart_title='Daily Occupancy Rate Trend',
        chart_icon='fas fa-chart-line',
        chart_dataset_label='Occupancy Rate (%)',
        chart_border_color='rgb(75, 192, 192)',
        chart_bg_color='rgba(75, 192, 192, 0.2)',
        chart_legend_position='top',
        chart_y_format='percentage',
        chart_max=100,
        table_data=occupancy_daily,
        table_title='Daily Occupancy Data',
        table_headers=['Date', 'Occupancy Rate (%)', 'Total Stays', 'Rooms Occupied']
    )

@app.route('/occupancy/monthly')
def occupancy_monthly_detail():
    occupancy_monthly = get_occupancy_rate_monthly()
    avg_occupancy = sum(row['occupancy_rate'] for row in occupancy_monthly) / len(occupancy_monthly) if occupancy_monthly else 0
    
    return render_template('metric_detail.html',
        metric_title='Monthly Occupancy Rate',
        metric_icon='fas fa-calendar-alt',
        metric_description='Monthly room occupancy trends',
        summary_card={
            'title': 'Average Monthly Occupancy',
            'value': f'{avg_occupancy:.1f}%',
            'subtitle': f'{len(occupancy_monthly)} months tracked',
            'icon': 'fas fa-bed',
            'color': 'bg-success'
        },
        chart_data=[row['occupancy_rate'] for row in occupancy_monthly],
        chart_labels=[row['month'] for row in occupancy_monthly],
        chart_type='line',
        chart_title='Monthly Occupancy Rate Trend',
        chart_icon='fas fa-chart-line',
        chart_dataset_label='Occupancy Rate (%)',
        chart_border_color='rgb(75, 192, 192)',
        chart_bg_color='rgba(75, 192, 192, 0.2)',
        chart_legend_position='top',
        chart_y_format='percentage',
        chart_max=100,
        table_data=occupancy_monthly,
        table_title='Monthly Occupancy Data',
        table_headers=['Month', 'Occupancy Rate (%)', 'Total Stays', 'Rooms Occupied']
    )

@app.route('/customers/top')
def top_customers_detail():
    top_customers = get_top_customers()
    total_revenue = sum(row['total_revenue'] for row in top_customers) if top_customers else 0
    
    return render_template('metric_detail.html',
        metric_title='Top Revenue-Generating Customers',
        metric_icon='fas fa-star',
        metric_description='Customers ranked by total revenue generated',
        summary_card={
            'title': 'Total Customer Revenue',
            'value': f'${total_revenue:,.2f}',
            'subtitle': f'{len(top_customers)} top customers',
            'icon': 'fas fa-users',
            'color': 'bg-info'
        },
        table_data=top_customers,
        table_title='Top Customers',
        table_headers=['Customer Name', 'Type', 'Total Revenue', 'Reservations', 'Last Visit']
    )

@app.route('/customers/high-risk')
def high_risk_customers_detail():
    high_risk_customers = get_high_risk_customers()
    
    return render_template('metric_detail.html',
        metric_title='High-Risk Customer List',
        metric_icon='fas fa-exclamation-triangle',
        metric_description='Customers with low qualification scores or overdue payments',
        summary_card={
            'title': 'High-Risk Customers',
            'value': len(high_risk_customers),
            'subtitle': 'Requires attention',
            'icon': 'fas fa-exclamation-triangle',
            'color': 'bg-danger'
        },
        table_data=high_risk_customers,
        table_title='High-Risk Customers',
        table_headers=['Customer Name', 'Type', 'Risk Score', 'Payment Score', 'Past History', 'Cooperativeness', 'Flexibility', 'Overall Score', 'Overdue Amount', 'Reservations']
    )

@app.route('/events/count')
def event_count_by_month_detail():
    event_count_by_month = get_event_count_by_month()
    total_events = sum(row['total_events'] for row in event_count_by_month) if event_count_by_month else 0
    
    return render_template('metric_detail.html',
        metric_title='Event Count by Month',
        metric_icon='fas fa-calendar-check',
        metric_description='Number of events scheduled by month',
        summary_card={
            'title': 'Total Events',
            'value': total_events,
            'subtitle': f'{len(event_count_by_month)} months tracked',
            'icon': 'fas fa-calendar-check',
            'color': 'bg-secondary'
        },
        chart_data=[row['total_events'] for row in event_count_by_month],
        chart_labels=[row['month'] for row in event_count_by_month],
        chart_type='bar',
        chart_title='Event Count by Month',
        chart_icon='fas fa-chart-bar',
        chart_dataset_label='Number of Events',
        chart_bg_color='rgba(153, 102, 255, 0.8)',
        chart_border_color='rgba(153, 102, 255, 1)',
        chart_legend_position='top',
        chart_y_format='number',
        table_data=event_count_by_month,
        table_title='Event Count by Month Data',
        table_headers=['Month', 'Total Events', 'Total Estimated Attendance', 'Avg Attendance', 'Unique Hosts']
    )

@app.route('/events/attendance')
def average_attendance_detail():
    average_attendance = get_average_attendance()
    
    return render_template('metric_detail.html',
        metric_title='Average Event Attendance',
        metric_icon='fas fa-users',
        metric_description='Average attendance statistics across all events',
        summary_card={
            'title': 'Average Estimated Attendance',
            'value': f'{average_attendance.get("avg_estimated_attendance", 0):.1f}',
            'subtitle': f'{average_attendance.get("total_events", 0)} total events',
            'icon': 'fas fa-users',
            'color': 'bg-info'
        },
        table_data=[average_attendance],
        table_title='Average Attendance Statistics',
        table_headers=['Total Events', 'Avg Estimated Attendance', 'Avg Actual Attendance', 'Total Estimated', 'Total Actual']
    )

@app.route('/food/avg-spend')
def avg_fb_spend_detail():
    avg_fb_spend = get_avg_fb_spend_per_guest()
    
    return render_template('metric_detail.html',
        metric_title='Average F&B Spend per Guest',
        metric_icon='fas fa-utensils',
        metric_description='Average food and beverage spending per guest',
        summary_card={
            'title': 'Avg F&B Spend per Guest',
            'value': f'${avg_fb_spend.get("avg_fb_spend_per_guest", 0):,.2f}',
            'subtitle': f'{avg_fb_spend.get("total_guests_with_fb", 0)} guests with F&B charges',
            'icon': 'fas fa-utensils',
            'color': 'bg-success'
        },
        table_data=[avg_fb_spend],
        table_title='F&B Spending Statistics',
        table_headers=['Total Guests', 'Total Meal Charges', 'Total F&B Revenue', 'Avg per Charge', 'Avg per Guest']
    )

@app.route('/food/meal-type')
def fb_revenue_by_meal_type_detail():
    fb_revenue_by_meal = get_fb_revenue_by_meal_type()
    total_revenue = sum(row['total_revenue'] for row in fb_revenue_by_meal) if fb_revenue_by_meal else 0
    
    return render_template('metric_detail.html',
        metric_title='F&B Revenue by Meal Type',
        metric_icon='fas fa-chart-pie',
        metric_description='Revenue breakdown by meal type (Breakfast, Lunch, Dinner)',
        summary_card={
            'title': 'Total F&B Revenue',
            'value': f'${total_revenue:,.2f}',
            'subtitle': f'{len(fb_revenue_by_meal)} meal types',
            'icon': 'fas fa-utensils',
            'color': 'bg-success'
        },
        chart_data=[row['total_revenue'] for row in fb_revenue_by_meal],
        chart_labels=[row['meal_type'].title() for row in fb_revenue_by_meal],
        chart_type='pie',
        chart_title='F&B Revenue by Meal Type',
        chart_icon='fas fa-chart-pie',
        chart_dataset_label='Revenue',
        chart_legend_position='right',
        table_data=fb_revenue_by_meal,
        table_title='F&B Revenue by Meal Type',
        table_headers=['Meal Type', 'Total Revenue', 'Total Charges', 'Avg Charge', 'Unique Customers', '% of Total F&B']
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
