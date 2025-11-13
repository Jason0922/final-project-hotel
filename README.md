# Last Resort Hotels - Database Project

## Project Overview
This project involves designing and implementing a comprehensive database system for Last Resort Hotels (LRH) with a web interface to help management understand business performance.

## Project Structure

### Planning Documents
- **PROJECT_PLAN.md** - Complete project overview, phases, and milestones
- **ERD_DESIGN_GUIDE.md** - Detailed database schema with 36 tables
- **QUERY_PLANNING.md** - 14+ management queries with SQL examples
- **WEB_INTERFACE_GUIDE.md** - Flask web application implementation guide

## Key Requirements Summary

### Database Design
- **Minimum (B Level)**: 15+ tables
- **Target (A Level)**: 20+ tables
- **Our Design**: 36 tables (exceeds A level)
- All tables normalized to 3NF

### Data Population
- **Minimum (B Level)**: 50+ customers, 100+ reservations (1 quarter)
- **Target (A Level)**: 75+ customers, 150+ reservations (1 quarter)

### Management Queries
- **Minimum (B Level)**: 5 complex queries
- **Target (A Level)**: 8+ complex queries
- **Our Plan**: 14 queries covering all business aspects

### Web Interface
- **Minimum (B Level)**: Functional interface with minimal graphics
- **Target (A Level)**: Enhanced interface with sophisticated graphics
- **Our Plan**: Dashboard with charts, tables, and interactive elements

## Technology Stack

### Database
- MySQL or PostgreSQL
- SQLAlchemy (optional)

### Backend
- Python 3.9+
- Flask web framework
- mysql-connector-python or psycopg2

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5 (styling)
- Chart.js (visualizations)

## Project Milestones

### Milestone 1 (October 16th)
- [ ] ERD PDF (all tables and relationships)
- [ ] Draft Analysis Report (business understanding, team assignments)

### Milestone 2 (November 11th)
- [ ] Proposed management queries (list with descriptions)
- [ ] Website wireframe/mockup

### Final Submission (December 4th)
- [ ] ERD PDF (GroupName_ERD.pdf)
- [ ] Database export (GroupName_export.sql)
- [ ] Analysis Report (GroupName_Analysis.docx)
- [ ] PyCharm project folder
- [ ] Team Evaluation (GroupName_TeamEvaluation.docx) - optional

## Quick Start Guide

### 1. Database Setup
1. Create database: `CREATE DATABASE last_resort_hotels;`
2. Review ERD_DESIGN_GUIDE.md for table structure
3. Create tables using SQL scripts
4. Populate with sample data

### 2. Web Interface Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Configure database in `config.py`
3. Review WEB_INTERFACE_GUIDE.md for implementation
4. Run application: `python app.py`
5. Access at `http://localhost:5000`

### 3. Query Development
1. Review QUERY_PLANNING.md for query examples
2. Test queries in database
3. Integrate into web interface

## Database Schema Highlights

### Core Entities
- **Location Hierarchy**: Buildings → Wings → Floors → Rooms
- **Room Types**: SleepingRooms, MeetingRooms, Suites
- **People**: Guests, Hosts, BilledParties
- **Transactions**: Reservations, Events, Charges, Bills
- **Tracking**: LocationLogs, RoomStatusHistory

### Key Features
- Supports complex room relationships (adjacency, movable walls)
- Flexible billing (split billing, organization billing)
- Time-based pricing (meeting room time slots)
- Location tracking (card readers, guest movements)
- Room status management (maintenance, renovation)

## Query Categories

1. **Revenue Analysis** - Monthly trends, service breakdown, building performance
2. **Occupancy Analysis** - Rates, room type utilization, peak periods
3. **Customer Analysis** - Top customers, retention, preferences
4. **Event Analysis** - Performance, room utilization, guest generation
5. **Service Usage** - Trends, popularity, revenue by service
6. **Room Performance** - Most booked, revenue per room
7. **Geographic Analysis** - Building/wing/floor performance
8. **Time Patterns** - Day-of-week, seasonal trends

## Web Interface Features

### Dashboard Components
- Summary cards (Total Revenue, Occupancy Rate, Active Customers)
- Revenue trend chart (line graph)
- Occupancy rate chart (line graph)
- Service revenue breakdown (pie chart)
- Seasonal revenue analysis (bar chart)
- Top customers table
- Most booked rooms table
- Event performance table

### Enhanced Features (A Level)
- Interactive date range selection
- Export functionality (CSV)
- Responsive design
- Additional visualizations
- Print-friendly views

## Analysis Report Sections

1. Executive Summary
2. Business Requirements Analysis
3. Design Decisions (conflicts, assumptions, deferred features)
4. Database Design Explanation
5. Implementation Details
6. Team Contributions

## Grading Rubric

- **ERD**: 25%
- **Database Implementation**: 25%
- **Queries**: 25%
- **Web Page(s)**: 15%
- **Analysis Report**: 10%

### B Level Work (80-92%)
- 15+ tables
- 50+ customers, 100+ reservations
- 5 complex queries
- Functional web interface
- Complete analysis report

### A Level Work (92-100%)
- 20+ tables
- 75+ customers, 150+ reservations
- 8+ complex queries
- Enhanced web interface
- Thorough analysis report

## Next Steps

1. **Review Planning Documents**
   - Read PROJECT_PLAN.md for overall structure
   - Study ERD_DESIGN_GUIDE.md for database design
   - Review QUERY_PLANNING.md for query examples
   - Check WEB_INTERFACE_GUIDE.md for implementation

2. **Team Coordination**
   - Assign team member roles
   - Set up GitHub repository
   - Create project timeline

3. **Begin Implementation**
   - Start with ERD design
   - Create database schema
   - Populate with sample data
   - Develop queries
   - Build web interface

## Important Notes

- All requirements from business description must be accounted for (either in ERD or analysis report)
- Document any conflicting/missing information and your decisions
- Ensure all tables are normalized to 3NF
- Queries should provide management insights, not just lists
- Web interface should be functional and user-friendly

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Bootstrap Documentation](https://getbootstrap.com/)
- [MySQL Documentation](https://dev.mysql.com/doc/)

## Support

For questions or clarifications:
- Review the planning documents
- Check the GitHub repository: https://github.com/markr-nyu/Hotel_Last_Resort
- Consult with instructor during office hours

---

**Good luck with your project!**



