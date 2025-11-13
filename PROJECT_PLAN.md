# Last Resort Hotels - Database Project Plan

## Project Overview
Design and develop a comprehensive database system for Last Resort Hotels (LRH) with a web interface to help management understand business performance.

## Project Structure

### Directory Organization
```
groupproject/
├── database/
│   ├── schema/
│   │   ├── create_tables.sql
│   │   ├── insert_sample_data.sql
│   │   └── queries.sql
│   ├── exports/
│   │   └── database_export.sql
│   └── erd/
│       └── GroupName_ERD.pdf
├── web/
│   ├── app.py (Flask application)
│   ├── templates/
│   │   ├── index.html
│   │   └── dashboard.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── config.py
├── analysis/
│   └── GroupName_Analysis.docx
├── team/
│   └── GroupName_TeamEvaluation.docx
├── requirements.txt
├── README.md
└── .gitignore
```

## Phase 1: Database Design (ERD)

### Core Entity Categories

#### 1. Location Hierarchy (4 tables)
- **Buildings**: Building name, address, location details
- **Wings**: Wing designation, building reference, proximity features (pool, parking, handicapped access)
- **Floors**: Floor number, wing reference, smoking designation
- **Rooms**: Room number, floor reference, room type, base rate, status

#### 2. Room Types & Features (6 tables)
- **RoomTypes**: Type ID, name (sleeping, suite, meeting), description
- **SleepingRooms**: Room reference, capacity, bed configurations, smoking status
- **MeetingRooms**: Room reference, seating capacity, has_toilet, has_foldable_bed
- **Suites**: Room reference, has_separate_meeting_room
- **Beds**: Bed ID, type (regular, extra-long, queen, king), size
- **RoomBeds**: Junction table (room_id, bed_id, quantity)

#### 3. Room Relationships (2 tables)
- **RoomAdjacency**: Adjacent room pairs, door type (private access, hallway)
- **MovableWalls**: Meeting room divisions, wall configuration

#### 4. People & Organizations (4 tables)
- **Guests**: Guest ID, name, contact info, PIN, card_number, organizational_affiliation
- **Hosts**: Host ID, name, contact info, organization_name
- **BilledParties**: Billed party ID, name, contact, organization, individual_contact_name
- **GuestOrganizations**: Organization name, contact details

#### 5. Reservations & Events (4 tables)
- **Reservations**: Reservation ID, guest/host reference, reservation_date, check_in, check_out, status
- **ReservationRequirements**: Bed type, number of guests, location preferences, smoking preference
- **Events**: Event ID, host reference, name, duration, estimated_attendance, estimated_guests
- **EventRooms**: Junction table (event_id, room_id, usage_time_slot)

#### 6. Room Assignments (2 tables)
- **RoomAssignments**: Assignment ID, reservation_id, room_id, check_in_time, check_out_time, actual_guests
- **GuestRoomAssignments**: Junction table (guest_id, room_assignment_id)

#### 7. Services & Charges (5 tables)
- **ServiceTypes**: Service type ID, name (meal, phone, business, room_service, retail, health_club)
- **Charges**: Charge ID, billed_party_id, service_type_id, room_assignment_id, amount, charge_date, description
- **MealCharges**: Charge reference, meal_type, location (meeting_room, restaurant, room_service)
- **PhoneCharges**: Charge reference, phone_number, duration, call_type
- **BusinessServiceCharges**: Charge reference, service_type (photocopy, computer, printing, fax), quantity

#### 8. Location Tracking (2 tables)
- **CardReaders**: Reader ID, location (room_id, facility_type), reader_type (entry/exit)
- **LocationLogs**: Log ID, guest_id, card_reader_id, timestamp, direction (entering/leaving)

#### 9. Room Status & Maintenance (2 tables)
- **RoomStatus**: Room ID, status (available, occupied, maintenance, renovation, cleaning), status_date
- **MaintenanceLogs**: Log ID, room_id, staff_card_id, action_type, timestamp

#### 10. Billing & Payments (3 tables)
- **Bills**: Bill ID, billed_party_id, total_amount, bill_date, status
- **BillCharges**: Junction table (bill_id, charge_id)
- **Payments**: Payment ID, bill_id, amount, payment_date, payment_method

#### 11. Deposits & Qualifications (2 tables)
- **Deposits**: Deposit ID, reservation_id, amount, deposit_date, refund_status
- **CustomerQualifications**: Billed party ID, past_history_score, cooperativeness, flexibility, payment_promptness

### Total: 20+ Tables (A Level Target)

### Key Relationships
- Buildings → Wings → Floors → Rooms (hierarchical)
- Rooms can be SleepingRooms, MeetingRooms, or Suites (subtypes)
- Reservations → RoomAssignments → Rooms
- Events → EventRooms → Rooms
- Guests/Hosts → Reservations
- BilledParties → Charges → Bills
- Guests → LocationLogs (tracking)

## Phase 2: Database Implementation

### Technology Stack
- **Database**: MySQL or PostgreSQL
- **Python**: 3.9+
- **ORM**: SQLAlchemy (optional, can use raw SQL)
- **Web Framework**: Flask (lightweight, good for this project)
- **Visualization**: Chart.js or Plotly for graphs

### Database Schema Implementation Steps

1. **Create Database**
   ```sql
   CREATE DATABASE last_resort_hotels;
   USE last_resort_hotels;
   ```

2. **Create Tables in Dependency Order**
   - Location hierarchy first (Buildings → Wings → Floors → Rooms)
   - Reference tables (RoomTypes, ServiceTypes, etc.)
   - People tables (Guests, Hosts, BilledParties)
   - Transaction tables (Reservations, Events)
   - Junction tables last

3. **Add Constraints**
   - Primary keys
   - Foreign keys
   - Check constraints (e.g., check_in < check_out)
   - Unique constraints where needed

4. **Normalization Verification**
   - Ensure all tables are in 3NF
   - No transitive dependencies
   - Proper foreign key relationships

### Data Population Strategy

#### Minimum Requirements (B Level)
- 50+ customers (mix of Guests, Hosts, BilledParties)
- 100+ reservations spanning 1 quarter (3 months)
- Multiple buildings, wings, floors
- Various room types
- Multiple events
- Diverse service charges

#### Enhanced Requirements (A Level)
- 75+ customers
- 150+ reservations spanning 1 quarter
- More complex scenarios:
  - Suite reservations
  - Multi-room events
  - Split billing
  - Room transfers during stay
  - Multiple events per guest

#### Sample Data Distribution
- 3-5 Buildings
- 10-15 Wings
- 50-100 Rooms (mix of types)
- 75-100 Guests
- 20-30 Hosts
- 150-200 Reservations
- 30-50 Events
- 500+ Charges (various types)
- Location logs for tracking

## Phase 3: Management Queries

### Query Categories (8+ queries for A level)

1. **Revenue Analysis**
   - Total revenue by month/quarter
   - Revenue by service type
   - Revenue by building/wing
   - Average revenue per reservation

2. **Occupancy Analysis**
   - Occupancy rate by month
   - Occupancy by room type
   - Peak occupancy periods
   - Room utilization efficiency

3. **Customer Analysis**
   - Top revenue-generating customers
   - Customer retention (repeat guests)
   - Average stay duration
   - Customer preferences (room types, locations)

4. **Event Analysis**
   - Events by month
   - Average event attendance
   - Meeting room utilization
   - Events generating most hotel stays

5. **Service Usage**
   - Most popular services
   - Service revenue trends
   - Average service charges per guest

6. **Room Performance**
   - Most booked rooms
   - Revenue per room type
   - Rooms requiring most maintenance

7. **Geographic/Location Analysis**
   - Performance by building
   - Wing popularity (pool proximity, etc.)
   - Floor-level analysis

8. **Time-based Trends**
   - Seasonal patterns
   - Day-of-week patterns
   - Growth trends over time

### Query Examples (Complexity Requirements)

Each query should:
- Use JOINs across multiple tables
- Include aggregate functions (SUM, AVG, COUNT)
- Use GROUP BY for summarization
- Include WHERE clauses for filtering
- Potentially use subqueries or CTEs

## Phase 4: Web Interface

### Technology Stack
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Charts**: Chart.js or Plotly
- **Database Connection**: mysql-connector-python or psycopg2

### Web Pages Structure

#### Option 1: Single Dashboard Page (B Level)
- One page showing all query results
- Simple tables and basic charts
- Static queries (pre-defined)

#### Option 2: Enhanced Dashboard (A Level)
- Multiple pages or tabs
- Interactive charts
- Better visualizations
- Additional features:
  - Date range selection (even if queries are static)
  - Export functionality
  - Print-friendly views
  - Responsive design

### Implementation Steps

1. **Setup Flask Application**
   ```python
   # app.py structure
   from flask import Flask, render_template
   import mysql.connector
   
   app = Flask(__name__)
   
   # Database connection
   def get_db_connection():
       # Connection logic
   
   @app.route('/')
   def dashboard():
       # Execute queries
       # Pass data to template
       return render_template('dashboard.html', data=query_results)
   ```

2. **Create Templates**
   - Base template with navigation
   - Dashboard with query results
   - Chart integration

3. **Query Execution**
   - Separate query functions
   - Error handling
   - Data formatting

4. **Visualization**
   - Tables for detailed data
   - Charts for trends (line, bar, pie)
   - Summary cards/statistics

## Phase 5: Analysis Report

### Report Sections

1. **Executive Summary**
   - Project overview
   - Key decisions made

2. **Business Requirements Analysis**
   - Requirements mapping to database design
   - Entity identification
   - Relationship analysis

3. **Design Decisions**
   - Conflicting information resolution
   - Missing information handling
   - Assumptions made
   - Deferred features (future phases)

4. **Database Design**
   - ERD explanation
   - Table descriptions
   - Relationship rationale
   - Normalization approach

5. **Implementation Details**
   - Technology choices
   - Data population strategy
   - Query design rationale

6. **Team Contributions**
   - Work allocation
   - Individual responsibilities
   - Collaboration approach

## Phase 6: Project Milestones

### Milestone 1 (October 16th)
- **Deliverables**:
  - ERD PDF (all tables and relationships)
  - Draft Analysis Report (business understanding, team assignments)

### Milestone 2 (November 11th)
- **Deliverables**:
  - Proposed management queries (list with descriptions)
  - Website wireframe/mockup

### Final Submission (December 4th)
- **Deliverables**:
  - ERD PDF
  - Database export
  - Analysis Report (Word document)
  - PyCharm project folder
  - Team Evaluation (optional)

## Technical Considerations

### Database Design Best Practices
- Use appropriate data types
- Index foreign keys
- Consider performance for queries
- Document constraints
- Handle NULL values appropriately

### Query Optimization
- Use indexes on frequently queried columns
- Optimize JOINs
- Consider query execution plans

### Web Interface Best Practices
- Secure database connections
- Input validation (even for static queries)
- Error handling
- User-friendly error messages
- Clean, readable code

## Risk Mitigation

### Potential Challenges
1. **Complex Room Relationships**
   - Solution: Clear adjacency table design
   
2. **Multiple Room Functions**
   - Solution: Flexible room type assignment
   
3. **Split Billing**
   - Solution: Separate BilledParties from Guests
   
4. **Time-based Queries**
   - Solution: Proper date handling and indexing

5. **Data Volume**
   - Solution: Efficient query design, proper indexing

## Success Criteria

### B Level Work
- 15+ tables
- 50+ customers, 100+ reservations
- 5 complex queries
- Functional web interface
- Complete analysis report

### A Level Work
- 20+ tables
- 75+ customers, 150+ reservations
- 8+ complex queries
- Enhanced web interface with graphics
- Thorough analysis report with all requirements addressed

## Next Steps

1. Review and finalize ERD design
2. Set up development environment
3. Create database schema
4. Populate with sample data
5. Develop and test queries
6. Build web interface
7. Write analysis report
8. Prepare final deliverables



