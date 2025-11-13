# ERD Design Guide - Last Resort Hotels

## Entity Relationship Diagram Structure

### Core Entities (20+ Tables)

#### Location Hierarchy (4 tables)

**1. Buildings**
- building_id (PK)
- building_name (UNIQUE)
- address
- city
- state
- zip_code
- total_floors

**2. Wings**
- wing_id (PK)
- building_id (FK → Buildings)
- wing_designation (e.g., "A", "North", "Poolside")
- proximity_to_pool (BOOLEAN)
- proximity_to_parking (BOOLEAN)
- handicapped_access (BOOLEAN)
- UNIQUE(building_id, wing_designation)

**3. Floors**
- floor_id (PK)
- wing_id (FK → Wings)
- floor_number
- smoking_designation (ENUM: 'smoking', 'nonsmoking', 'mixed')
- UNIQUE(wing_id, floor_number)

**4. Rooms**
- room_id (PK)
- floor_id (FK → Floors)
- room_number (e.g., "1201" = floor 12, room 01)
- base_daily_rate (DECIMAL)
- room_status (ENUM: 'available', 'occupied', 'maintenance', 'renovation', 'cleaning')
- can_be_sleeping (BOOLEAN)
- can_be_meeting (BOOLEAN)
- has_toilet_facilities (BOOLEAN)
- has_foldable_bed (BOOLEAN)
- UNIQUE(floor_id, room_number)

#### Room Types & Features (6 tables)

**5. RoomTypes**
- room_type_id (PK)
- type_name (ENUM: 'sleeping', 'suite', 'meeting', 'mixed')
- description

**6. SleepingRooms**
- sleeping_room_id (PK)
- room_id (FK → Rooms, UNIQUE)
- capacity (INT) - number of adults
- smoking_preference (ENUM: 'smoking', 'nonsmoking')
- has_extra_space (BOOLEAN)
- extra_space_type (VARCHAR) - 'meeting', 'rollaway', NULL

**7. MeetingRooms**
- meeting_room_id (PK)
- room_id (FK → Rooms, UNIQUE)
- seating_capacity (INT)
- has_toilet (BOOLEAN)
- can_use_as_sleeping (BOOLEAN) - if has toilet

**8. Suites**
- suite_id (PK)
- room_id (FK → Rooms, UNIQUE)
- has_separate_meeting_room (BOOLEAN)
- meeting_room_id (FK → MeetingRooms, NULLABLE)

**9. Beds**
- bed_id (PK)
- bed_type (ENUM: 'regular', 'extra_long', 'queen', 'king')
- bed_size (ENUM: 'double', 'queen', 'king')

**10. RoomBeds** (Junction Table)
- room_bed_id (PK)
- room_id (FK → Rooms)
- bed_id (FK → Beds)
- quantity (INT)
- UNIQUE(room_id, bed_id)

#### Room Relationships (2 tables)

**11. RoomAdjacency**
- adjacency_id (PK)
- room1_id (FK → Rooms)
- room2_id (FK → Rooms)
- door_type (ENUM: 'private_access', 'hallway', 'movable_wall')
- CHECK(room1_id != room2_id)

**12. MovableWalls**
- wall_id (PK)
- parent_room_id (FK → Rooms) - large meeting room
- divided_room_designation (VARCHAR) - e.g., "Ballroom A", "Ballroom B"
- seating_capacity (INT)
- has_door (BOOLEAN)

#### People & Organizations (4 tables)

**13. Guests**
- guest_id (PK)
- first_name
- last_name
- email
- phone
- address
- city
- state
- zip_code
- pin_number (VARCHAR) - for card access
- card_number (VARCHAR, UNIQUE)
- organizational_affiliation (VARCHAR, NULLABLE)
- created_date (DATE)

**14. Hosts**
- host_id (PK)
- first_name
- last_name
- email
- phone
- organization_name (VARCHAR, NULLABLE)
- address
- city
- state
- zip_code

**15. BilledParties**
- billed_party_id (PK)
- party_type (ENUM: 'guest', 'host', 'organization', 'external')
- first_name (VARCHAR, NULLABLE)
- last_name (VARCHAR, NULLABLE)
- organization_name (VARCHAR, NULLABLE)
- contact_person_name (VARCHAR) - required for organizations
- email
- phone
- address
- city
- state
- zip_code
- CHECK(
  (party_type = 'organization' AND organization_name IS NOT NULL) OR
  (party_type != 'organization' AND first_name IS NOT NULL AND last_name IS NOT NULL)
)

**16. GuestOrganizations**
- organization_id (PK)
- organization_name (UNIQUE)
- contact_person
- email
- phone
- address

#### Reservations & Events (4 tables)

**17. Reservations**
- reservation_id (PK)
- reservation_date (DATE)
- check_in_date (DATE)
- check_out_date (DATE)
- reservation_status (ENUM: 'pending', 'confirmed', 'checked_in', 'checked_out', 'cancelled')
- guest_id (FK → Guests, NULLABLE)
- host_id (FK → Hosts, NULLABLE)
- billed_party_id (FK → BilledParties)
- advance_deposit_required (BOOLEAN)
- deposit_amount (DECIMAL, NULLABLE)
- special_requests (TEXT)
- CHECK(check_in_date < check_out_date)

**18. ReservationRequirements**
- requirement_id (PK)
- reservation_id (FK → Reservations)
- bed_type_preference (ENUM: 'regular', 'extra_long', 'queen', 'king', NULL)
- number_of_guests (INT)
- location_preference (VARCHAR) - proximity requirements
- smoking_preference (ENUM: 'smoking', 'nonsmoking', 'no_preference')
- room_type_preference (ENUM: 'sleeping', 'suite', 'meeting', NULL)

**19. Events**
- event_id (PK)
- event_name
- host_id (FK → Hosts)
- billed_party_id (FK → BilledParties)
- start_date (DATE)
- end_date (DATE)
- start_time (TIME)
- end_time (TIME)
- estimated_attendance (INT)
- estimated_guests_staying (INT)
- event_type (VARCHAR)
- CHECK(start_date <= end_date)

**20. EventRooms** (Junction Table)
- event_room_id (PK)
- event_id (FK → Events)
- room_id (FK → Rooms)
- usage_time_slot (ENUM: 'breakfast', 'morning', 'lunch', 'afternoon', 'supper', 'evening', 'night')
- usage_date (DATE)
- is_eating_usage (BOOLEAN) - determines pricing
- actual_attendance (INT, NULLABLE)
- UNIQUE(event_id, room_id, usage_date, usage_time_slot)

#### Room Assignments (2 tables)

**21. RoomAssignments**
- assignment_id (PK)
- reservation_id (FK → Reservations)
- room_id (FK → Rooms)
- check_in_time (DATETIME)
- check_out_time (DATETIME, NULLABLE)
- actual_guests (INT)
- early_extension_hours (DECIMAL, DEFAULT 0)
- late_extension_hours (DECIMAL, DEFAULT 0)
- extension_surcharge (DECIMAL, DEFAULT 0)
- assignment_status (ENUM: 'assigned', 'checked_in', 'checked_out', 'transferred')
- CHECK(check_in_time < check_out_time OR check_out_time IS NULL)

**22. GuestRoomAssignments** (Junction Table)
- guest_assignment_id (PK)
- guest_id (FK → Guests)
- assignment_id (FK → RoomAssignments)
- is_primary_guest (BOOLEAN)
- UNIQUE(guest_id, assignment_id)

#### Services & Charges (5 tables)

**23. ServiceTypes**
- service_type_id (PK)
- service_name (ENUM: 'meal', 'phone', 'business_service', 'room_service', 'retail', 'health_club', 'other')
- description

**24. Charges**
- charge_id (PK)
- billed_party_id (FK → BilledParties)
- service_type_id (FK → ServiceTypes)
- room_assignment_id (FK → RoomAssignments, NULLABLE)
- event_id (FK → Events, NULLABLE)
- charge_date (DATETIME)
- amount (DECIMAL)
- description (TEXT)
- charge_status (ENUM: 'pending', 'billed', 'paid', 'cancelled')

**25. MealCharges**
- meal_charge_id (PK)
- charge_id (FK → Charges, UNIQUE)
- meal_type (ENUM: 'breakfast', 'lunch', 'dinner', 'snack', 'bar')
- location_type (ENUM: 'meeting_room', 'restaurant', 'room_service')
- room_id (FK → Rooms, NULLABLE)
- number_of_guests (INT)

**26. PhoneCharges**
- phone_charge_id (PK)
- charge_id (FK → Charges, UNIQUE)
- phone_number (VARCHAR)
- call_duration_minutes (INT)
- call_type (ENUM: 'local', 'long_distance', 'international')
- call_date (DATETIME)

**27. BusinessServiceCharges**
- business_charge_id (PK)
- charge_id (FK → Charges, UNIQUE)
- service_detail (ENUM: 'photocopy', 'computer_time', 'equipment_rental', 'printing', 'fax')
- quantity (INT)
- unit_price (DECIMAL)

#### Location Tracking (2 tables)

**28. CardReaders**
- reader_id (PK)
- location_type (ENUM: 'room', 'restaurant', 'health_club', 'meeting_room', 'other')
- room_id (FK → Rooms, NULLABLE)
- facility_name (VARCHAR)
- reader_direction (ENUM: 'entry', 'exit')

**29. LocationLogs**
- log_id (PK)
- guest_id (FK → Guests)
- card_reader_id (FK → CardReaders)
- timestamp (DATETIME)
- direction (ENUM: 'entering', 'leaving')
- INDEX(timestamp)

#### Room Status & Maintenance (2 tables)

**30. RoomStatusHistory**
- status_history_id (PK)
- room_id (FK → Rooms)
- status (ENUM: 'available', 'occupied', 'maintenance', 'renovation', 'cleaning')
- status_start (DATETIME)
- status_end (DATETIME, NULLABLE)
- staff_card_id (VARCHAR, NULLABLE)
- notes (TEXT)

**31. MaintenanceLogs**
- maintenance_log_id (PK)
- room_id (FK → Rooms)
- staff_card_id (VARCHAR)
- action_type (ENUM: 'cleaning_complete', 'repair_complete', 'inspection', 'renovation_start', 'renovation_complete')
- timestamp (DATETIME)
- notes (TEXT)

#### Billing & Payments (3 tables)

**32. Bills**
- bill_id (PK)
- billed_party_id (FK → BilledParties)
- total_amount (DECIMAL)
- bill_date (DATE)
- due_date (DATE)
- bill_status (ENUM: 'pending', 'sent', 'paid', 'overdue', 'cancelled')
- payment_terms (TEXT)

**33. BillCharges** (Junction Table)
- bill_charge_id (PK)
- bill_id (FK → Bills)
- charge_id (FK → Charges)
- UNIQUE(bill_id, charge_id)

**34. Payments**
- payment_id (PK)
- bill_id (FK → Bills)
- payment_amount (DECIMAL)
- payment_date (DATE)
- payment_method (ENUM: 'credit_card', 'debit_card', 'cash', 'check', 'wire_transfer')
- transaction_reference (VARCHAR, NULLABLE)

#### Deposits & Qualifications (2 tables)

**35. Deposits**
- deposit_id (PK)
- reservation_id (FK → Reservations)
- amount (DECIMAL)
- deposit_date (DATE)
- refund_status (ENUM: 'pending', 'applied', 'refunded', 'forfeited')
- refund_date (DATE, NULLABLE)
- refund_amount (DECIMAL, NULLABLE)

**36. CustomerQualifications**
- qualification_id (PK)
- billed_party_id (FK → BilledParties, UNIQUE)
- past_history_score (INT) - 0-100
- cooperativeness_score (INT) - 0-100
- flexibility_score (INT) - 0-100
- payment_promptness_score (INT) - 0-100
- overall_qualification_score (DECIMAL) - calculated
- last_updated (DATE)

### Total: 36 Tables (Exceeds A Level Requirement)

## Key Design Decisions

### 1. Room Type Flexibility
- Rooms can have multiple functions (sleeping/meeting)
- Separate tables for SleepingRooms, MeetingRooms, Suites
- Junction table for room functions

### 2. Billing Complexity
- Separate BilledParties from Guests/Hosts
- Supports split billing
- Organization billing with individual contact

### 3. Time-based Pricing
- Meeting rooms: time slots with different rates
- Sleeping rooms: daily basis with extension surcharges
- EventRooms tracks usage time slots

### 4. Location Tracking
- Card readers at various facilities
- Location logs track guest movements
- Supports contact location features

### 5. Room Status Management
- Status history tracks changes over time
- Maintenance logs for staff actions
- Supports renovation/cleaning tracking

## Relationships Summary

- **One-to-Many**: Buildings → Wings → Floors → Rooms
- **One-to-One**: Rooms → SleepingRooms/MeetingRooms/Suites
- **Many-to-Many**: Rooms ↔ Rooms (adjacency), Guests ↔ RoomAssignments, Events ↔ Rooms
- **Complex**: Reservations → RoomAssignments → Rooms (with guest assignments)

## Normalization Notes

- All tables in 3NF
- Junction tables for many-to-many relationships
- Separate tables for subtypes (SleepingRooms, MeetingRooms, Suites)
- No transitive dependencies
- Proper foreign key constraints



