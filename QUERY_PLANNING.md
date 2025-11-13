# Management Query Planning Guide

## Query Requirements
- **B Level**: 5+ queries with GROUP BY, functions, multiple tables
- **A Level**: 8+ queries with complexity

## Query Categories & Examples

### 1. Revenue Analysis Queries

#### Query 1: Monthly Revenue Trend
```sql
SELECT 
    DATE_FORMAT(charge_date, '%Y-%m') AS month,
    SUM(amount) AS total_revenue,
    COUNT(DISTINCT billed_party_id) AS unique_customers,
    COUNT(charge_id) AS total_charges
FROM Charges
WHERE charge_status IN ('billed', 'paid')
GROUP BY DATE_FORMAT(charge_date, '%Y-%m')
ORDER BY month;
```
**Purpose**: Shows revenue growth/decline over time

#### Query 2: Revenue by Service Type
```sql
SELECT 
    st.service_name,
    COUNT(c.charge_id) AS number_of_charges,
    SUM(c.amount) AS total_revenue,
    AVG(c.amount) AS average_charge,
    SUM(c.amount) * 100.0 / (SELECT SUM(amount) FROM Charges WHERE charge_status IN ('billed', 'paid')) AS percentage_of_total
FROM Charges c
JOIN ServiceTypes st ON c.service_type_id = st.service_type_id
WHERE c.charge_status IN ('billed', 'paid')
GROUP BY st.service_name
ORDER BY total_revenue DESC;
```
**Purpose**: Identifies most profitable services

#### Query 3: Revenue by Building
```sql
SELECT 
    b.building_name,
    COUNT(DISTINCT r.room_id) AS total_rooms,
    SUM(c.amount) AS total_revenue,
    AVG(c.amount) AS avg_revenue_per_charge,
    SUM(c.amount) / COUNT(DISTINCT r.room_id) AS revenue_per_room
FROM Charges c
JOIN RoomAssignments ra ON c.room_assignment_id = ra.assignment_id
JOIN Rooms r ON ra.room_id = r.room_id
JOIN Floors f ON r.floor_id = f.floor_id
JOIN Wings w ON f.wing_id = w.wing_id
JOIN Buildings b ON w.building_id = b.building_id
WHERE c.charge_status IN ('billed', 'paid')
GROUP BY b.building_id, b.building_name
ORDER BY total_revenue DESC;
```
**Purpose**: Compares performance across buildings

### 2. Occupancy Analysis Queries

#### Query 4: Monthly Occupancy Rate
```sql
SELECT 
    DATE_FORMAT(ra.check_in_time, '%Y-%m') AS month,
    COUNT(DISTINCT ra.assignment_id) AS total_stays,
    COUNT(DISTINCT ra.room_id) AS unique_rooms_occupied,
    (SELECT COUNT(*) FROM Rooms WHERE room_status != 'renovation') AS total_available_rooms,
    (COUNT(DISTINCT ra.room_id) * 100.0 / 
     (SELECT COUNT(*) FROM Rooms WHERE room_status != 'renovation')) AS occupancy_rate
FROM RoomAssignments ra
WHERE ra.check_in_time IS NOT NULL
GROUP BY DATE_FORMAT(ra.check_in_time, '%Y-%m')
ORDER BY month;
```
**Purpose**: Tracks occupancy trends

#### Query 5: Occupancy by Room Type
```sql
SELECT 
    CASE 
        WHEN sr.sleeping_room_id IS NOT NULL THEN 'Sleeping Room'
        WHEN su.suite_id IS NOT NULL THEN 'Suite'
        WHEN mr.meeting_room_id IS NOT NULL THEN 'Meeting Room'
        ELSE 'Other'
    END AS room_type,
    COUNT(DISTINCT ra.assignment_id) AS total_assignments,
    SUM(DATEDIFF(COALESCE(ra.check_out_time, NOW()), ra.check_in_time)) AS total_nights,
    AVG(DATEDIFF(COALESCE(ra.check_out_time, NOW()), ra.check_in_time)) AS avg_nights_per_stay
FROM RoomAssignments ra
JOIN Rooms r ON ra.room_id = r.room_id
LEFT JOIN SleepingRooms sr ON r.room_id = sr.room_id
LEFT JOIN Suites su ON r.room_id = su.room_id
LEFT JOIN MeetingRooms mr ON r.room_id = mr.room_id
GROUP BY room_type
ORDER BY total_assignments DESC;
```
**Purpose**: Shows which room types are most popular

### 3. Customer Analysis Queries

#### Query 6: Top Revenue-Generating Customers
```sql
SELECT 
    bp.billed_party_id,
    COALESCE(bp.organization_name, CONCAT(bp.first_name, ' ', bp.last_name)) AS customer_name,
    bp.party_type,
    COUNT(DISTINCT c.charge_id) AS total_charges,
    SUM(c.amount) AS total_revenue,
    COUNT(DISTINCT res.reservation_id) AS total_reservations,
    MAX(res.check_in_date) AS last_visit_date
FROM BilledParties bp
JOIN Charges c ON bp.billed_party_id = c.billed_party_id
LEFT JOIN Reservations res ON bp.billed_party_id = res.billed_party_id
WHERE c.charge_status IN ('billed', 'paid')
GROUP BY bp.billed_party_id, customer_name, bp.party_type
ORDER BY total_revenue DESC
LIMIT 20;
```
**Purpose**: Identifies VIP customers

#### Query 7: Customer Retention Analysis
```sql
SELECT 
    g.guest_id,
    CONCAT(g.first_name, ' ', g.last_name) AS guest_name,
    COUNT(DISTINCT res.reservation_id) AS total_visits,
    MIN(res.check_in_date) AS first_visit,
    MAX(res.check_in_date) AS last_visit,
    DATEDIFF(MAX(res.check_in_date), MIN(res.check_in_date)) AS days_between_first_last,
    SUM(DATEDIFF(res.check_out_date, res.check_in_date)) AS total_nights,
    AVG(DATEDIFF(res.check_out_date, res.check_in_date)) AS avg_nights_per_visit
FROM Guests g
JOIN Reservations res ON g.guest_id = res.guest_id
WHERE res.reservation_status IN ('checked_out', 'checked_in')
GROUP BY g.guest_id, guest_name
HAVING total_visits > 1
ORDER BY total_visits DESC, total_nights DESC;
```
**Purpose**: Identifies repeat customers and loyalty

### 4. Event Analysis Queries

#### Query 8: Event Performance Analysis
```sql
SELECT 
    e.event_id,
    e.event_name,
    h.organization_name AS host_organization,
    COUNT(DISTINCT er.room_id) AS rooms_used,
    COUNT(DISTINCT er.usage_time_slot) AS time_slots_used,
    e.estimated_attendance,
    SUM(CASE WHEN er.is_eating_usage THEN 1 ELSE 0 END) AS eating_slots,
    SUM(CASE WHEN NOT er.is_eating_usage THEN 1 ELSE 0 END) AS non_eating_slots,
    COUNT(DISTINCT res.reservation_id) AS guest_reservations_generated,
    SUM(c.amount) AS total_event_revenue
FROM Events e
JOIN Hosts h ON e.host_id = h.host_id
LEFT JOIN EventRooms er ON e.event_id = er.event_id
LEFT JOIN Reservations res ON res.check_in_date BETWEEN e.start_date AND e.end_date
LEFT JOIN Charges c ON c.event_id = e.event_id AND c.charge_status IN ('billed', 'paid')
GROUP BY e.event_id, e.event_name, h.organization_name, e.estimated_attendance
ORDER BY total_event_revenue DESC;
```
**Purpose**: Analyzes event profitability and guest generation

#### Query 9: Meeting Room Utilization
```sql
SELECT 
    r.room_id,
    r.room_number,
    mr.seating_capacity,
    COUNT(DISTINCT er.event_id) AS total_events,
    COUNT(er.usage_time_slot) AS total_time_slots_used,
    SUM(CASE WHEN er.is_eating_usage THEN 1 ELSE 0 END) AS eating_slots,
    SUM(CASE WHEN NOT er.is_eating_usage THEN 1 ELSE 0 END) AS non_eating_slots,
    SUM(c.amount) AS total_revenue
FROM Rooms r
JOIN MeetingRooms mr ON r.room_id = mr.room_id
LEFT JOIN EventRooms er ON r.room_id = er.room_id
LEFT JOIN Events e ON er.event_id = e.event_id
LEFT JOIN Charges c ON c.event_id = e.event_id AND c.charge_status IN ('billed', 'paid')
GROUP BY r.room_id, r.room_number, mr.seating_capacity
ORDER BY total_revenue DESC;
```
**Purpose**: Shows which meeting rooms are most utilized

### 5. Service Usage Analysis

#### Query 10: Service Usage Trends
```sql
SELECT 
    st.service_name,
    DATE_FORMAT(c.charge_date, '%Y-%m') AS month,
    COUNT(c.charge_id) AS usage_count,
    SUM(c.amount) AS total_revenue,
    AVG(c.amount) AS avg_charge_amount
FROM Charges c
JOIN ServiceTypes st ON c.service_type_id = st.service_type_id
WHERE c.charge_status IN ('billed', 'paid')
GROUP BY st.service_name, DATE_FORMAT(c.charge_date, '%Y-%m')
ORDER BY st.service_name, month;
```
**Purpose**: Tracks service usage trends over time

### 6. Room Performance Analysis

#### Query 11: Most Booked Rooms
```sql
SELECT 
    r.room_id,
    r.room_number,
    b.building_name,
    w.wing_designation,
    COUNT(DISTINCT ra.assignment_id) AS total_bookings,
    SUM(DATEDIFF(COALESCE(ra.check_out_time, NOW()), ra.check_in_time)) AS total_nights_booked,
    SUM(ra.extension_surcharge) AS total_extension_revenue,
    AVG(r.base_daily_rate) AS base_rate,
    SUM(c.amount) AS total_revenue_generated
FROM Rooms r
JOIN Floors f ON r.floor_id = f.floor_id
JOIN Wings w ON f.wing_id = w.wing_id
JOIN Buildings b ON w.building_id = b.building_id
LEFT JOIN RoomAssignments ra ON r.room_id = ra.room_id
LEFT JOIN Charges c ON c.room_assignment_id = ra.assignment_id AND c.charge_status IN ('billed', 'paid')
GROUP BY r.room_id, r.room_number, b.building_name, w.wing_designation
ORDER BY total_revenue_generated DESC
LIMIT 20;
```
**Purpose**: Identifies most profitable rooms

### 7. Geographic/Location Analysis

#### Query 12: Wing Performance Analysis
```sql
SELECT 
    w.wing_designation,
    b.building_name,
    w.proximity_to_pool,
    w.proximity_to_parking,
    w.handicapped_access,
    COUNT(DISTINCT r.room_id) AS total_rooms,
    COUNT(DISTINCT ra.assignment_id) AS total_bookings,
    AVG(r.base_daily_rate) AS avg_room_rate,
    SUM(c.amount) AS total_revenue
FROM Wings w
JOIN Buildings b ON w.building_id = b.building_id
JOIN Floors f ON w.wing_id = f.wing_id
JOIN Rooms r ON f.floor_id = r.floor_id
LEFT JOIN RoomAssignments ra ON r.room_id = ra.room_id
LEFT JOIN Charges c ON c.room_assignment_id = ra.assignment_id AND c.charge_status IN ('billed', 'paid')
GROUP BY w.wing_id, w.wing_designation, b.building_name, w.proximity_to_pool, w.proximity_to_parking, w.handicapped_access
ORDER BY total_revenue DESC;
```
**Purpose**: Analyzes wing popularity based on features

### 8. Time-based Pattern Analysis

#### Query 13: Day-of-Week Booking Patterns
```sql
SELECT 
    DAYNAME(ra.check_in_time) AS day_of_week,
    DAYOFWEEK(ra.check_in_time) AS day_number,
    COUNT(DISTINCT ra.assignment_id) AS total_check_ins,
    AVG(DATEDIFF(COALESCE(ra.check_out_time, NOW()), ra.check_in_time)) AS avg_stay_length,
    SUM(c.amount) AS total_revenue
FROM RoomAssignments ra
LEFT JOIN Charges c ON c.room_assignment_id = ra.assignment_id AND c.charge_status IN ('billed', 'paid')
WHERE ra.check_in_time IS NOT NULL
GROUP BY DAYNAME(ra.check_in_time), DAYOFWEEK(ra.check_in_time)
ORDER BY day_number;
```
**Purpose**: Identifies peak booking days

#### Query 14: Seasonal Revenue Analysis
```sql
SELECT 
    CASE 
        WHEN MONTH(charge_date) IN (12, 1, 2) THEN 'Winter'
        WHEN MONTH(charge_date) IN (3, 4, 5) THEN 'Spring'
        WHEN MONTH(charge_date) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END AS season,
    YEAR(charge_date) AS year,
    COUNT(charge_id) AS total_charges,
    SUM(amount) AS total_revenue,
    AVG(amount) AS avg_charge_amount,
    COUNT(DISTINCT billed_party_id) AS unique_customers
FROM Charges
WHERE charge_status IN ('billed', 'paid')
GROUP BY season, YEAR(charge_date)
ORDER BY year, season;
```
**Purpose**: Shows seasonal revenue patterns

## Query Implementation Notes

### Complexity Features Used
- Multiple JOINs across 3-7 tables
- Aggregate functions: COUNT, SUM, AVG, MAX, MIN
- GROUP BY with multiple columns
- Subqueries in SELECT and WHERE clauses
- CASE statements for conditional logic
- Date functions: DATE_FORMAT, DATEDIFF, DAYNAME
- Window functions (if needed): RANK(), DENSE_RANK()
- HAVING clauses for filtered aggregations

### Web Display Considerations
- Format currency values
- Format dates consistently
- Handle NULL values gracefully
- Add percentage calculations where relevant
- Include summary statistics
- Consider pagination for large result sets

### Performance Optimization
- Index on foreign keys
- Index on date columns used in WHERE/GROUP BY
- Index on charge_status for filtering
- Consider materialized views for complex queries (if database supports)

## Query Selection for Web Interface

### Recommended 8 Queries for A Level:
1. Monthly Revenue Trend (Chart: Line graph)
2. Revenue by Service Type (Chart: Pie or Bar chart)
3. Monthly Occupancy Rate (Chart: Line graph)
4. Top Revenue-Generating Customers (Table with top 10)
5. Customer Retention Analysis (Table with statistics)
6. Event Performance Analysis (Table with summary)
7. Most Booked Rooms (Table with top 15)
8. Seasonal Revenue Analysis (Chart: Bar chart grouped by season)

### Dashboard Layout Suggestion:
- **Top Row**: Key metrics (Total Revenue, Occupancy Rate, Active Customers)
- **Middle Row**: Charts (Revenue Trend, Occupancy Trend, Service Breakdown)
- **Bottom Row**: Tables (Top Customers, Top Rooms, Recent Events)



