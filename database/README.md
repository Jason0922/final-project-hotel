# Database Setup Guide

This guide will help you set up the Last Resort Hotels database with all tables and sample data.

## Prerequisites

- MySQL 8.0+ or MariaDB 10.3+
- MySQL client or MySQL Workbench
- Python 3.9+ with required packages installed

## Setup Steps

### 1. Create Database and Tables

Run the schema creation script:

```bash
mysql -u your_username -p < database/schema/create_tables.sql
```

Or using MySQL Workbench:
- Open MySQL Workbench
- File → Open SQL Script → Select `database/schema/create_tables.sql`
- Execute the script

### 2. Populate Sample Data

Run the sample data insertion script:

```bash
mysql -u your_username -p < database/schema/insert_sample_data.sql
```

Or using MySQL Workbench:
- File → Open SQL Script → Select `database/schema/insert_sample_data.sql`
- Execute the script

### 3. Configure Database Connection

Copy the example config file and update with your database credentials:

```bash
cp config.example.py config.py
```

Edit `config.py` with your database credentials:

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

**Note:** Add `config.py` to `.gitignore` to keep your credentials secure!

### 4. Verify Installation

Test the database connection:

```python
python -c "from app import get_db_connection; conn = get_db_connection(); print('Connected!' if conn else 'Failed')"
```

### 5. Run the Application

```bash
python app.py
```

Visit http://localhost:5000 to see the dashboard.

## Database Structure

- **36 Tables** (exceeds A-level requirement of 20+)
- **Location Hierarchy**: Buildings → Wings → Floors → Rooms
- **Room Types**: Sleeping, Meeting, Suites
- **People**: Guests, Hosts, BilledParties
- **Reservations & Events**: Full booking system
- **Charges & Billing**: Complete billing system
- **Tracking**: Location logs, maintenance logs

## Sample Data Overview

The sample data includes:
- 4 Buildings
- 12 Wings
- 60 Floors
- 80 Rooms (50 sleeping, 20 meeting, 10 suites)
- 50+ Guests
- 25 Hosts
- 80+ BilledParties
- 15+ Reservations (sample - expand to 150+ for full A-level)
- 10+ Events (sample - expand to 40+ for full A-level)
- 500+ Charges (sample)

## Expanding Sample Data

To meet full A-level requirements (150+ reservations), you can:

1. **Use a data generation script** (recommended)
2. **Manually add more reservations** using SQL INSERT statements
3. **Use the pattern** shown in `insert_sample_data.sql` to generate more records

## Troubleshooting

### Connection Errors

- Verify MySQL is running: `mysqladmin -u root -p status`
- Check credentials in `config.py`
- Ensure database exists: `SHOW DATABASES;`

### Import Errors

- Check SQL syntax errors in the console
- Verify foreign key constraints are satisfied
- Ensure tables are created in the correct order

### Empty Results

- Verify data was inserted: `SELECT COUNT(*) FROM Reservations;`
- Check date ranges in queries match your data
- Verify charge_status values are correct ('billed' or 'paid')

## Database Maintenance

### Backup Database

```bash
mysqldump -u your_username -p last_resort_hotels > backup.sql
```

### Restore Database

```bash
mysql -u your_username -p last_resort_hotels < backup.sql
```

### Reset Database

```bash
mysql -u your_username -p -e "DROP DATABASE IF EXISTS last_resort_hotels;"
mysql -u your_username -p < database/schema/create_tables.sql
mysql -u your_username -p < database/schema/insert_sample_data.sql
```

## Next Steps

1. Review the ERD design in `ERD_DESIGN_GUIDE.md`
2. Check query examples in `QUERY_PLANNING.md`
3. Customize queries in `app.py` as needed
4. Expand sample data to meet full requirements


