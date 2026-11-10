# Insurance Policy Tracker

A REST API backend built with Python and Flask to manage insurance policy records.
Simulates a core data management use case in the insurance domain.

## Tech Stack
- Python + Flask
- MySQL
- Postman (for testing)
- Git + GitHub

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /addPolicy | Add a new policy |
| GET | /getAllPolicies | Retrieve all policies |
| GET | /getPolicy/<id> | Retrieve one policy by ID |

## Setup
1. Clone the repo
2. Create a virtual environment and activate it
3. Run `pip install flask flask-mysqldb`
4. Set up MySQL and create the database using the schema in schema.sql
5. Update the database credentials in app.py
6. Run `python app.py`