# API Documentation

## Authentication Endpoints

### 1. User Signup
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/signup/`
- Description: Creates a new user account with basic information and credentials

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/signup/`
- Method: POST
- Input: username, password, confirmPassword, firstName, lastName, emailID/contactNo
- Response: Returns user ID and username on success
- Security: Validates password match and requires either email or contact number
- Example: Visit `http://127.0.0.1:8000/api/signup/` and send POST request with body:
```json
{
    "username": "john",
    "password": "pass123",
    "confirmPassword": "pass123",
    "firstName": "John",
    "lastName": "Doe",
    "emailID": "john@example.com"
}
```

### 2. User Login
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/login/`
- Description: Authenticates user credentials and returns user information

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/login/`
- Method: POST
- Input: username and password
- Response: Returns user ID and username if credentials are valid
- Security: Validates password against stored hash
- Example: Visit `http://127.0.0.1:8000/api/login/` and send POST request with body:
```json
{
    "username": "john",
    "password": "pass123"
}
```

### 3. Admin Login
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/admin/login/`
- Description: Authenticates admin users using email and password

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/admin/login/`
- Method: POST
- Input: emailID and password
- Response: Returns admin ID, email, and role
- Security: Separate authentication system for admin users
- Example: Visit `http://127.0.0.1:8000/api/admin/login/` and send POST request with body:
```json
{
    "emailID": "admin@example.com",
    "password": "admin123"
}
```

### 4. Organizer Login
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/login/`
- Description: Authenticates event organizers with username and password

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/login/`
- Method: POST
- Input: username and password
- Response: Returns organizer ID and username
- Security: Separate authentication system for organizers
- Example: Visit `http://127.0.0.1:8000/api/organizer/login/` and send POST request with body:
```json
{
    "username": "event_org",
    "password": "org123"
}
```

### 5. Organizer Signup
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/signup/`
- Description: Creates a new organizer account with required information

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/signup/`
- Method: POST
- Input: username, password, confirm_password, firstName, lastName, emailID/contactNo
- Response: Returns organizer ID and username on success
- Security: Validates password match and requires contact information
- Example: Visit `http://127.0.0.1:8000/api/organizer/signup/` and send POST request with body:
```json
{
    "username": "event_org",
    "password": "org123",
    "confirm_password": "org123",
    "firstName": "Event",
    "lastName": "Organizer",
    "emailID": "org@example.com"
}
```

### 6. Event Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/event/<int:event_id>/`
- Description: Retrieves detailed information about a specific event

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/event/1/` (example with event_id=1)
- Method: GET
- Input: event_id in URL path
- Response: Returns complete event details
- Example: Visit `http://127.0.0.1:8000/api/event/1/` to get details of event with ID 1

### 7. Filtered Events
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/events/filtered/`
- Description: Retrieves upcoming events, optionally filtered by category

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/events/filtered/?filter=ea`
- Method: GET
- Input: filter parameter in query string (optional)
  - 'ea' = Entertainment/Art (Concert, Dance, Art)
  - 'bt' = Business/Tech
  - 'fl' = Food/Lifestyle (Food, Expo)
  - 'si' = Social Impact (Charity)
  - 'sf' = Sports/Fitness (Sports, Gaming)
- Response: Returns list of upcoming events (optionally filtered by category)
- Note: This endpoint only returns upcoming events (events with future dates or today's events with future times)
- Example: Visit `http://127.0.0.1:8000/api/events/filtered/?filter=ea` to get upcoming entertainment and art events

### 8. Events by Organizer
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/events/organizer/<int:organizer_id>/`
- Description: Lists all events organized by a specific organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/events/organizer/1/` (example with organizer_id=1)
- Method: GET
- Input: organizer_id in URL path, optional filter parameter (0=upcoming, 1=past)
- Response: Returns list of events for the organizer
- Example: Visit `http://127.0.0.1:8000/api/events/organizer/1/?filter=0` to get upcoming events for organizer 1

### 9. Organizers by Admin
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizers/admin/<int:staff_id>/`
- Description: Lists all organizers managed by a specific admin staff member

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizers/admin/1/` (example with staff_id=1)
- Method: GET
- Input: staff_id in URL path
- Response: Returns list of organizers with basic information
- Example: Visit `http://127.0.0.1:8000/api/organizers/admin/1/` to get organizers managed by admin staff 1

### 10. Organizer Average Rating
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<int:organizer_id>/average-rating/`
- Description: Calculates and returns the average rating for an organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/1/average-rating/` (example with organizer_id=1)
- Method: GET
- Input: organizer_id in URL path
- Response: Returns organizer's average rating and details
- Example: Visit `http://127.0.0.1:8000/api/organizer/1/average-rating/` to get average rating for organizer 1

### 11. Organizer Complaints
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<int:organizer_id>/complaints/`
- Description: Retrieves complaint count for an organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/1/complaints/?event_id=1` (example with organizer_id=1 and optional event_id=1)
- Method: GET
- Input: organizer_id in URL path, optional event_id in query parameters
- Response: Returns complaint count for organizer or specific event
- Example: Visit `http://127.0.0.1:8000/api/organizer/1/complaints/` to get total complaints for organizer 1

### 12. User Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/user/<int:id>/`
- Description: Retrieves detailed information about a specific user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/user/1/` (example with user_id=1)
- Method: GET
- Input: user_id in URL path
- Response: Returns user details (excluding ID)
- Example: Visit `http://127.0.0.1:8000/api/user/1/` to get details of user with ID 1

### 13. Admin Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/admin/<int:id>/`
- Description: Retrieves detailed information about a specific admin

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/admin/1/` (example with admin_id=1)
- Method: GET
- Input: admin_id in URL path
- Response: Returns admin details (excluding ID)
- Example: Visit `http://127.0.0.1:8000/api/admin/1/` to get details of admin with ID 1

### 14. Organizer Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<int:id>/`
- Description: Retrieves detailed information about a specific organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/1/` (example with organizer_id=1)
- Method: GET
- Input: organizer_id in URL path
- Response: Returns organizer details (excluding ID)
- Example: Visit `http://127.0.0.1:8000/api/organizer/1/` to get details of organizer with ID 1

### 15. Unverified Organizers
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/admin/unverified-organizers/`
- Description: Lists all organizers that are pending verification

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/admin/unverified-organizers/`
- Method: GET
- Input: None
- Response: Returns list of all unverified organizers with their details
- Example: Visit `http://127.0.0.1:8000/api/admin/unverified-organizers/` to get list of unverified organizers

### 16. Organizer Event Feedback
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<int:organizer_id>/feedbacks/`
- Description: Retrieves feedback for events organized by a specific organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/1/feedbacks/?event_id=1` (example with organizer_id=1 and optional event_id=1)
- Method: GET
- Input: 
  - organizer_id (required): ID of the organizer in URL path
  - event_id (optional): ID of specific event to get feedback for
- Response: Returns feedback details including event name, rating, comments, and creation date
- Example: 
  - Basic: Visit `http://127.0.0.1:8000/api/organizer/1/feedbacks/` to get all feedback for organizer 1
  - With Event: Visit `http://127.0.0.1:8000/api/organizer/1/feedbacks/?event_id=1` to get feedback for specific event

### 17. User Registration Transactions
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/user/<int:user_id>/registrations/`
- Description: Retrieves registration and transaction details for a specific user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/user/1/registrations/` (example with user_id=1)
- Method: GET
- Input: user_id in URL path
- Response: Returns list of registrations with event and transaction details
- Example: Visit `http://127.0.0.1:8000/api/user/1/registrations/` to get registration history for user 1

### 18. User Events
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/user/<int:user_id>/events/`
- Description: Lists all events registered by a specific user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/user/1/events/?filter=1` (example with user_id=1 and optional filter)
- Method: GET
- Input: 
  - user_id (required): ID of the user in URL path
  - filter (optional): 
    - '1' = upcoming events
    - '2' = past events
- Response: Returns list of events with basic details (id, name, category, dates)
- Example: 
  - Basic: Visit `http://127.0.0.1:8000/api/user/1/events/` to get all events for user 1
  - With Filter: Visit `http://127.0.0.1:8000/api/user/1/events/?filter=1` to get upcoming events

### 19. Complaint Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/complaint/<int:complaint_id>/`
- Description: Retrieves detailed information about a specific complaint

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/complaint/1/` (example with complaint_id=1)
- Method: GET
- Input: complaint_id in URL path
- Response: Returns complete complaint details including user and event information
- Example: Visit `http://127.0.0.1:8000/api/complaint/1/` to get details of complaint with ID 1

### 20. Feedback Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/feedback/<int:feedback_id>/`
- Description: Retrieves detailed information about a specific feedback

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/feedback/1/` (example with feedback_id=1)
- Method: GET
- Input: feedback_id in URL path
- Response: Returns complete feedback details including user and event information
- Example: Visit `http://127.0.0.1:8000/api/feedback/1/` to get details of feedback with ID 1

### 21. Transaction Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/transaction/<int:transaction_id>/`
- Description: Retrieves detailed information about a specific transaction

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/transaction/1/` (example with transaction_id=1)
- Method: GET
- Input: transaction_id in URL path
- Response: Returns complete transaction details including user and event information
- Example: Visit `http://127.0.0.1:8000/api/transaction/1/` to get details of transaction with ID 1

### 22. Registration Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/registration/<int:registration_id>/`
- Description: Retrieves detailed information about a specific registration

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/registration/1/` (example with registration_id=1)
- Method: GET
- Input: registration_id in URL path
- Response: Returns complete registration details including user, event, and transaction information
- Example: Visit `http://127.0.0.1:8000/api/registration/1/` to get details of registration with ID 1

### 23. Create Event
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/create-event/<int:organizer_id>/`
- Description: Creates a new event for a specific organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/create-event/1/` (example with organizer_id=1)
- Method: POST
- Input: 
  - organizer_id (required): ID of the organizer in URL path
  - Request Body:
    - eventName (required)
    - category (required)
    - description (required)
    - startDate (required)
    - startTime (required)
    - endDate (required)
    - endTime (required)
    - venue (required)
    - ticketPrice (required)
    - maxAttendees (required)
- Response: Returns created event details
- Note: Event start time must be in the future, end time must be after start time
- Example: Visit `http://127.0.0.1:8000/api/create-event/1/` and send POST request with body:
```json
{
    "eventName": "Tech Conference",
    "category": "Business/Tech",
    "description": "Annual tech conference",
    "startDate": "2024-04-01",
    "startTime": "09:00:00",
    "endDate": "2024-04-02",
    "endTime": "17:00:00",
    "venue": "Convention Center",
    "ticketPrice": 1000,
    "maxAttendees": 500
}
```

### 24. Verify Organizer
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/verify-organizer/<int:staff_id>/<int:organizer_id>/<str:verification_status>/`
- Description: Verifies or unverifies an organizer's account by an admin staff member

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/verify-organizer/1/2/true/` (example with staff_id=1, organizer_id=2, verification_status=true)
- Method: GET
- Input: 
  - staff_id (required): ID of the admin staff in URL path
  - organizer_id (required): ID of the organizer to verify in URL path
  - verification_status (required): Verification status ('true' or 'false') in URL path
- Response: Returns updated organizer details with verification status
- Note: 
  - Sets the verification date to today's date if status is 'true'
  - Removes verification date if status is 'false'
  - Updates the staff member who performed the verification
- Example: Visit `http://127.0.0.1:8000/api/verify-organizer/1/2/true/` to verify organizer 2 by staff 1

### 25. Submit Feedback
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/feedback/<int:user_id>/<int:event_id>/`
- Description: Submits feedback for an event by a user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/feedback/1/2/` (example with user_id=1, event_id=2)
- Method: POST
- Input: 
  - user_id (required): ID of the user in URL path
  - event_id (required): ID of the event in URL path
  - Request Body:
    - Rating (required): Numeric rating
    - Comments (optional): Text feedback
- Response: Returns created feedback details
- Example: Visit `http://127.0.0.1:8000/api/feedback/1/2/` and send POST request with body:
```json
{
    "Rating": 4.5,
    "Comments": "Great event, well organized!"
}
```

### 26. Create Complaint
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/complaints/create/`
- Description: Creates a new complaint for an event

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/complaints/create/`
- Method: POST
- Input: 
  - Request Body:
    - event_id (required): ID of the event
    - user_id (required): ID of the user
    - Description (required): Complaint details
    - Category (required): Type of complaint
- Response: Returns created complaint details
- Example: Visit `http://127.0.0.1:8000/api/complaints/create/` and send POST request with body:
```json
{
    "event_id": 1,
    "user_id": 2,
    "Description": "Event started late",
    "Category": "Timing"
}
```

### 27. Register Event
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/register-event/`
- Description: Registers a user for an event and creates a transaction

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/register-event/`
- Method: POST
- Input: 
  - Request Body:
    - user_id (required): ID of the user
    - event_id (required): ID of the event
    - payment_method (required): Payment method (e.g., 'Wallet', 'Card')
    - number_of_tickets (required): Number of tickets to purchase
- Response: Returns registration and transaction details
- Note: Checks wallet balance if using wallet payment
- Example: Visit `http://127.0.0.1:8000/api/register-event/` and send POST request with body:
```json
{
    "user_id": 1,
    "event_id": 2,
    "payment_method": "Wallet",
    "number_of_tickets": 2
}
```

### 28. Event Revenue
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/event/<int:event_id>/revenue/`
- Description: Retrieves revenue details for a specific event

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/event/1/revenue/` (example with event_id=1)
- Method: GET
- Input: event_id in URL path
- Response: Returns event revenue details including:
  - event_name
  - ticket_price
  - tickets_sold
  - total_revenue
- Example: Visit `http://127.0.0.1:8000/api/event/1/revenue/` to get revenue details for event 1

### 29. User Transaction History
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/user/<int:user_id>/transactions/`
- Description: Retrieves transaction history for a specific user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/user/1/transactions/` (example with user_id=1)
- Method: GET
- Input: user_id in URL path
- Response: Returns list of all transactions made by the user including:
  - Transaction ID
  - Event details
  - Payment method
  - Amount
  - Transaction date
- Example: Visit `http://127.0.0.1:8000/api/user/1/transactions/` to get transaction history for user 1

### 30. User Complaint History
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/user/<int:user_id>/complaints/`
- Description: Retrieves complaint history for a specific user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/user/1/complaints/` (example with user_id=1)
- Method: GET
- Input: user_id in URL path
- Response: Returns list of all complaints made by the user including:
  - Complaint ID
  - Event details
  - Description
  - Category
  - Status
  - Creation date
- Example: Visit `http://127.0.0.1:8000/api/user/1/complaints/` to get complaint history for user 1

### 31. Organizer Revenue Stats
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<int:organizer_id>/revenue-stats/`
- Description: Retrieves revenue statistics for all events organized by a specific organizer

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/1/revenue-stats/` (example with organizer_id=1)
- Method: GET
- Input: organizer_id in URL path
- Response: Returns revenue statistics including:
  - organizer_id
  - total_revenue (sum of all event revenues)
  - total_attendees (sum of all tickets sold)
- Note: Returns zero values if organizer has no events
- Example: Visit `http://127.0.0.1:8000/api/organizer/1/revenue-stats/` to get revenue statistics for organizer 1

### 32. Update User
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/users/<int:user_id>/update/`
- Description: Updates user information

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/users/1/update/` (example with user_id=1)
- Method: PUT
- Input: 
  - user_id (required): ID of the user in URL path
  - Request Body (all fields optional):
    - username
    - firstName
    - lastName
    - emailID
    - contactNo
    - wallet_balance
- Response: Returns updated user details
- Example: Visit `http://127.0.0.1:8000/api/users/1/update/` and send PUT request with body:
```json
{
    "firstName": "Updated",
    "lastName": "Name",
    "emailID": "updated@example.com"
}
```

### 33. Update Organizer
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/update/<int:organizer_id>/`
- Description: Updates organizer information

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/update/1/` (example with organizer_id=1)
- Method: PUT
- Input: 
  - organizer_id (required): ID of the organizer in URL path
  - Request Body (all fields optional):
    - username
    - firstName
    - lastName
    - emailID
    - contactNo
    - organization
    - verification_status
- Response: Returns updated organizer details
- Example: Visit `http://127.0.0.1:8000/api/organizer/update/1/` and send PUT request with body:
```json
{
    "organization": "New Organization Name",
    "emailID": "updated@example.com"
}
```

### 34. Update Event
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/events/<int:event_id>/update/`
- Description: Updates event information

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/events/1/update/` (example with event_id=1)
- Method: PUT
- Input: 
  - event_id (required): ID of the event in URL path
  - Request Body (all fields optional):
    - eventName
    - category
    - description
    - startDate
    - startTime
    - endDate
    - endTime
    - venue
    - ticketPrice
    - maxAttendees
- Response: Returns updated event details
- Example: Visit `http://127.0.0.1:8000/api/events/1/update/` and send PUT request with body:
```json
{
    "eventName": "Updated Event Name",
    "ticketPrice": 1500,
    "venue": "New Venue Location"
}
```

### 35. Event Registrations
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/event/<int:event_id>/registrations/`
- Description: Retrieves all registrations for a specific event

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/event/1/registrations/` (example with event_id=1)
- Method: GET
- Input: event_id in URL path
- Response: Returns event registration details including:
  - event_name
  - total_registrations (count)
  - registrations list with:
    - registration_id
    - username
    - email
    - contact
- Example: Visit `http://127.0.0.1:8000/api/event/1/registrations/` to get all registrations for event 1


### 36. Organizer Event Statistics
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<organiser_id>/event-stats/`
- Description: Retrieves statistics about past events organized by a specific organizer.

**Detailed View:**
- Complete URL: `http://127.0.0.1:8000/api/organizer/1/event-stats/`
- Method: GET
- Input Parameters:
  - `organiser_id` (path parameter): ID of the organizer
- Response: Returns the average percentage of tickets sold for past events
  ```json
  {
    "organizer_id": 1,
    "average_percentage_sold": 75.5
  }
  ```
- Example Usage:
  - Visit: `http://127.0.0.1:8000/api/organizer/1/event-stats/`
  - Response will show the average percentage of tickets sold for all past events organized by the specified organizer


### 37. Event Rating
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/event/<int:event_id>/rating/`
- Description: Retrieves the average rating for a specific event

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/event/1/rating/` (example with event_id=1)
- Method: GET
- Input: event_id in URL path
- Response: Returns event rating details including:
  - event name
  - average rating (rounded to 2 decimal places)
- Note: Returns "No ratings yet" if no ratings are available
- Example: Visit `http://127.0.0.1:8000/api/event/1/rating/` to get average rating for event 1


### 38. Complaints Under Admin
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/admin/<int:admin_id>/organizer-complaints/`
- Description: Retrieves all complaints related to events managed by organizers under a specific admin

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/admin/1/organizer-complaints/` (example with admin_id=1)
- Method: GET
- Input: admin_id in URL path
- Response: Returns complaint details including:
  - admin email
  - total number of complaints
  - list of complaints with:
    - event name
    - user name
    - organizer name
    - complaint category
    - status
    - description
    - creation date
- Note: Returns empty list if no organizers or complaints are found under the admin
- Example: Visit `http://127.0.0.1:8000/api/admin/1/organizer-complaints/` to get all complaints under admin with ID 1

### 39. Top Attendees
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/top-attendees/<int:staff_id>/`
- Description: Retrieves a list of top attendees who have registered for more than 2 events

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/top-attendees/1/` (example with staff_id=1)
- Method: GET
- Input: 
  - staff_id (required): ID of the admin staff in URL path
- Response: Returns list of top 5 users with their registration counts
  ```json
  {
    "users": [
      {
        "user_id": 1,
        "username": "user1",
        "events_registered": 5
      },
      {
        "user_id": 2,
        "username": "user2",
        "events_registered": 4
      }
      // ... up to 5 users
    ]
  }
  ```
- Note: 
  - Only returns users who have registered for more than 2 events
  - Results are ordered by number of registrations (descending)
  - Limited to top 5 users
- Example: Visit `http://127.0.0.1:8000/api/top-attendees/1/` to get top attendees list


### 40. Event Attendees
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/event/<int:event_id>/attendees/`
- Description: Retrieves detailed information about all attendees for a specific event

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/event/1/attendees/` (example with event_id=1)
- Method: GET
- Input: event_id in URL path
- Response: Returns event attendees information including:
  - event_id
  - list of attendees with:
    - user_id
    - username
    - full_name (first name + last name)
    - number of tickets purchased
- Note: For free events (ticket price = 0), number of tickets defaults to 1
- Example: Visit `http://127.0.0.1:8000/api/event/1/attendees/` to get attendee list for event 1


### 41. Filtered Event List
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/events/filter/<int:filter_type>/`
- Description: Retrieves events filtered by different time periods

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/events/filter/1/` (example with filter_type=1)
- Method: GET
- Input: filter_type in URL path
  - 1 = Today's events
  - 2 = Events in next 7 days
  - 3 = Events in next 30 days
- Response: Returns list of events matching the filter criteria
- Note: Returns error for invalid filter types
- Example: Visit `http://127.0.0.1:8000/api/events/filter/2/` to get events happening in the next 7 days


### 42. Low Performance Events
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/organizer/<int:organizer_id>/low-performance-events/`
- Description: Retrieves past events that had low attendance (less than 33% of capacity)

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/organizer/1/low-performance-events/` (example with organizer_id=1)
- Method: GET
- Input: organizer_id in URL path
- Response: Returns list of low performance events with:
  - event details
  - tickets sold
  - maximum capacity
  - attendance ratio
- Note: Only returns past events with attendance ratio less than 33%
- Example: Visit `http://127.0.0.1:8000/api/organizer/1/low-performance-events/` to get low performance events for organizer 1


### 43. Create Venue
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/create-venue/`
- Description: Creates a new venue with complete address and contact details

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/create-venue/`
- Method: POST
- Input: Request body with venue details:
  - name (required)
  - street (required)
  - city (required)
  - state (required)
  - pincode (required, 5-10 digits)
  - contactNo (required)
- Response: Returns created venue ID
- Note: Validates pincode format and checks for duplicate venues
- Example: Visit `http://127.0.0.1:8000/api/create-venue/` and send POST request with body:
```json
{
    "name": "Grand Ballroom",
    "street": "123 Main Street",
    "city": "New York",
    "state": "NY",
    "pincode": "10001",
    "contactNo": "1234567890"
}

### 44. Event Detail
**Simplified View:**
- URL: `http://127.0.0.1:8000/api/complaint_event-detail/<int:user_id>/<int:event_id>/`
- Description: Retrieves detailed information about a specific event for a user

**Detailed View:**
- URL: `http://127.0.0.1:8000/api/complaint_event-detail/1/2/` (example with user_id=1, event_id=2)
- Method: GET
- Input: 
  - user_id (required): ID of the user in URL path
  - event_id (required): ID of the event in URL path
- Response: Returns complete event details including:
  - eventName
  - ticketPrice
  - category
  - maxAttendees
  - created_at
  - startDate
  - startTime
  - endDate
  - endTime
  - venue details
  - organizer details
  - ticketsSold
  - status
- Error Response: Returns 404 if event not found
- Example: Visit `http://127.0.0.1:8000/api/complaint_event-detail/1/2/` to get details of event with ID 2 for user with ID 1

