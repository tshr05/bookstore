Bookstore API
This is a FastAPI-based Bookstore API that provides CRUD operations for managing books.
The API uses MongoDB as its database.
Project Setup
Prerequisites
Ensure you have the following installed:
● Python 3.12+
● MongoDB
● Virtual environment tools (venv)
Installation
1. Clone the repository:
git clone https://github.com/tshr05/bookstore.git
cd bookstore
2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt
4. Set up MongoDB connection in .env file:
MONGO_URI=mongodb://localhost:27017/bookstore
Running the API
Start the FastAPI application using Uvicorn:
uvicorn main:app --reload
The API will be available at: http://127.0.0.1:8000
Running Tests Locally
Unit &amp; Integration Tests

Ensure the virtual environment is activated, then run:
pytest -v --cov=bookstore tests/

To collect available tests:
pytest --collect-only

Troubleshooting Test Issues
● Ensure MongoDB is running before running integration tests.
● If tests are not discovered, ensure test files start with test_ and functions are prefixed
with test_.
● Use pytest --disable-warnings to suppress warnings during testing.
API Documentation
Once the server is running, access API docs:
● Swagger UI: http://127.0.0.1:8000/docs
● ReDoc: http://127.0.0.1:8000/redoc
