## VIP Event Manager API
# Flask + MySQL API to manage VIP members, events, and registrations with membership tiers and event capacity rules.
# Tables: member, event, registration (with cascade deletes and uniqueness constraints).
# Run: python api.py → server at http://127.0.0.1:5000.
# Endpoints: /members, /events, /registrations (supports CRUD, JSON requests).
# Used AI to walkthrough the process of setting up postman and the connection between the api and the database itself since it wouldnt work for a bit. Used for understanding some of the execute functions and understanding why some of the checks were breaking before I got it to work on postman requests.