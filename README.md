# HappenIn-Website-Testing

Event Management System API Documentation
=======================================

This document provides detailed information about all API endpoints available in the system, including query variations and their effects.

1. Authentication Endpoints
-------------------------

1.1 User Authentication
- URL: /signup/
- Method: POST
- Description: Creates a new user account
- Required Fields: username, password, confirmPassword, firstName, lastName, emailID/contactNo
- Query Variations:
  * Must provide either emailID or contactNo (at least one is required)
  * lastName is optional
- Returns: User ID and username on success

1.2 User Login
- URL: /login/
- Method: POST
- Description: Authenticates a user
- Required Fields: username, password
- Returns: User ID and username on success

1.3 Admin Login
- URL: /admin/login/
- Method: POST
- Description: Authenticates an admin
- Required Fields: emailID, password
- Returns: Admin ID, emailID, and role on success

1.4 Organizer Login
- URL: /organizer/login/
- Method: POST
- Description: Authenticates an organizer
- Required Fields: username, password
- Returns: Organizer ID and username on success

1.5 Organizer Signup
- URL: /organizer/signup/
- Method: POST
- Description: Creates a new organizer account
- Required Fields: username, password, confirm_password, firstName, lastName, emailID/contactNo
- Query Variations:
  * Must provide either emailID or contactNo (at least one is required)
  * lastName is optional
  * organization is optional
- Returns: Organizer ID and username on success

2. Event Management Endpoints
---------------------------

2.1 Event Details
- URL: /event/<int:event_id>/
- Method: GET
- Description: Retrieves details of a specific event
- Returns: Complete event information including:
  * Event name, price, category
  * Start/end dates and times
  * Venue details
  * Organizer information
  * Tickets sold and max attendees

2.2 Filtered Events
- URL: /events/filtered/
- Method: GET
- Description: Retrieves filtered events based on category
- Query Parameters: 
  * filter (optional): 
    - 'ea' = Entertainment & Arts (Concert, Dance, Art)
    - 'bt' = Business & Tech
    - 'fl' = Food & Lifestyle
    - 'si' = Social Impact
    - 'sf' = Sports & Fitness
  * If no filter provided: returns all upcoming events
- Returns: List of filtered events

2.3 Events by Organizer
- URL: /events/organizer/<int:organizer_id>/
- Method: GET
- Description: Retrieves events organized by a specific organizer
- Query Parameters: 
  * filter (optional):
    - '0' = upcoming events
    - '1' = past events
  * If no filter provided: returns all events
- Returns: List of organizer's events

2.4 Create Event
- URL: /create-event/<int:organizer_id>/
- Method: POST
- Description: Creates a new event
- Required Fields: eventName, ticketPrice, category, maxAttendees, startDate, startTime, endDate, endTime, venue
- Query Variations:
  * maxAttendees can be null (no limit)
  * venue can be null (virtual event)
- Returns: Created event details

2.5 Event Revenue
- URL: /event/<int:event_id>/revenue/
- Method: GET
- Description: Retrieves revenue information for a specific event
- Returns: Event revenue details including:
  * Ticket price
  * Number of tickets sold
  * Total revenue generated
 
2.6 Update Event Details
- URL: /event/<int:event_id>/update/
- Method: PUT
- Description: Updates details of a specific event
- Required Fields: At least one of the following:
  * eventName, ticketPrice, category, maxAttendees, startDate, startTime, endDate, endTime, venue
- Query Variations:
  * Allows partial updates
  * maxAttendees can be set to null for unlimited capacity
  * venue can be null for virtual events
  * Validates if the event date and time have passed
  * Ensures that startDate, startTime, endDate, and endTime are correct and have not passed
- Returns: Updated event information

3. Organizer Management Endpoints
------------------------------

3.1 Organizer Verification
- URL: /verify-organizer/<int:staff_id>/<int:organizer_id>/
- Method: POST
- Description: Verifies an organizer account
- Query Variations:
  * Can only verify unverified organizers
  * Sets verification date to current date
- Returns: Updated organizer details

3.2 Organizer Average Rating
- URL: /organizer/<int:organizer_id>/average-rating/
- Method: GET
- Description: Retrieves average rating for an organizer
- Query Variations:
  * Returns 0.0 if no ratings exist
  * Rounds to 2 decimal places
- Returns: Organizer's average rating

3.3 Organizer Complaints
- URL: /organizer/<int:organizer_id>/complaints/
- Method: GET
- Description: Retrieves complaint count for an organizer
- Query Parameters: 
  * event_id (optional):
    - If provided: returns complaints for specific event
    - If not provided: returns total complaints for all events
- Returns: Complaint count

3.4 Organizers by Admin
- URL: /organizers/admin/<int:staff_id>/
- Method: GET
- Description: Retrieves organizers managed by a specific admin
- Returns: List of organizers with:
  * Basic information
  * Verification status
  * Organization details
 
3.5 Update Organizer Details
- URL: /organizer/<int:organizer_id>/update/
- Method: PUT
- Description: Updates organizer's profile information
- Required Fields: Any of: firstName, lastName, emailID, contactNo, organization
- Query Variations:
  * At least one field is required
  * Email/contact must follow valid formats
- Returns: Updated organizer profile

4. User Management Endpoints
--------------------------

4.1 User Details
- URL: /user/<int:id>/
- Method: GET
- Description: Retrieves user details
- Returns: Complete user information including:
  * Personal details
  * Contact information
  * Wallet balance

4.2 User Registrations
- URL: /user/<int:user_id>/registrations/
- Method: GET
- Description: Retrieves user's event registrations
- Returns: List of registrations with:
  * Event details
  * Transaction information
  * Registration status

4.3 User Events
- URL: /user/<int:user_id>/events/
- Method: GET
- Description: Retrieves events registered by user
- Query Parameters:
  * filter (optional):
    - '1' = upcoming events
    - '2' = past events
  * If no filter provided: returns all events
- Returns: List of user's events

4.4 Update User Details
- URL: /user/<int:user_id>/update/
- Method: PUT
- Description: Updates the details of a user
- Required Fields: Any of: firstName, lastName, emailID, contactNo, walletBalance (at least one required)
- Query Variations:
  * All fields optional but must include at least one
  * walletBalance must be a non-negative decimal
- Returns: Updated user

5. Feedback and Complaints
------------------------

5.1 Submit Feedback
- URL: /feedback/<int:user_id>/<int:event_id>/
- Method: POST
- Description: Submits feedback for an event
- Required Fields: Rating, Comments
- Query Variations:
  * Rating must be between 1-5
  * Comments are optional
  * One feedback per user per event
- Returns: Success message

5.2 Create Complaint
- URL: /complaints/create/
- Method: POST
- Description: Creates a new complaint
- Required Fields: event_id, user_id, Description, Category
- Query Variations:
  * Category must be one of: Event Issues, Ticketing Problems, App & Tech Issues, Safety & Security, Service & Hospitality, Other
  * One complaint per category per event per user
- Returns: Created complaint details

5.3 Complaint Details
- URL: /complaint/<int:complaint_id>/
- Method: GET
- Description: Retrieves details of a specific complaint
- Returns: Complete complaint information including:
  * User details
  * Event details
  * Complaint description and category
  * Status and creation date

5.4 Feedback Details
- URL: /feedback/<int:feedback_id>/
- Method: GET
- Description: Retrieves details of a specific feedback
- Returns: Complete feedback information including:
  * User details
  * Event details
  * Rating and comments
  * Creation date

6. Transaction and Registration
----------------------------

6.1 Register for Event
- URL: /register-event/
- Method: POST
- Description: Registers a user for an event and creates transaction
- Required Fields: user_id, event_id, payment_method, number_of_tickets
- Query Variations:
  * payment_method must be one of: Credit Card, Debit Card, UPI, Net Banking, Wallet
  * If using Wallet: checks sufficient balance
  * Checks event capacity
  * Checks event status (must be upcoming)
- Returns: Registration ID

6.2 Transaction Details
- URL: /transaction/<int:transaction_id>/
- Method: GET
- Description: Retrieves details of a specific transaction
- Returns: Complete transaction information including:
  * Payment method
  * Amount
  * Status
  * Date and time
  * Associated event and user

6.3 Registration Details
- URL: /api/registration/<int:registration_id>/
- Method: GET
- Description: Retrieves details of a specific registration
- Returns: Complete registration information including:
  * User details
  * Event details
  * Transaction details

7. Admin Management Endpoints
--------------------------

7.1 Admin Details
- URL: /admin/<int:id>/
- Method: GET
- Description: Retrieves admin details
- Returns: Complete admin information including:
  * Personal details
  * Role
  * Contact information

7.2 Unverified Organizers
- URL: /admin/unverified-organizers/
- Method: GET
- Description: Retrieves list of unverified organizers
- Returns: List of unverified organizers with:
  * Basic information
  * Contact details
  * Organization information

Notes:
- All monetary values are in decimal format with 2 decimal places
- Dates should be in YYYY-MM-DD format
- Times should be in HH:MM:SS format
- All endpoints return appropriate HTTP status codes
- Authentication is required for most endpoints
- Error responses include detailed error messages
- Optional fields can be omitted from requests
- Query parameters are case-sensitive
- All IDs in URLs must be valid integers
