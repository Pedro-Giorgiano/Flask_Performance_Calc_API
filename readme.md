# Flask Performance Calc API

This project implements a Flask API to centralize and calculate employee performance data, including career growth projections based on semi-annual evaluations. The API is designed to be used by different user roles, including managers, directors, employees, and HR. JWT authentication is used to secure access to the endpoints.

## Features

- **JWT Authentication**: Secures the endpoints and allows safe communication.
- **Employee Growth Projection**: Calculates the projected improvement in frequency per semester, based on previous employee evaluations.
- **Role-Based Access Control**: Different roles (manager, director, HR) have different levels of access to employee data.
- **Evaluation History**: Allows retrieving and projecting employee growth based on their past evaluations.
- **Password Security**: Uses bcrypt for secure password hashing and storage.

## Technologies Used

- **Flask**: Web framework for building the API.
- **Flask-CORS**: CORS support to allow cross-origin requests.
- **SQLAlchemy**: ORM for interacting with the database.
- **JWT (JSON Web Tokens)**: Authentication and authorization.
- **SQLite**: Relational database used for data persistence (ideal for local testing).
- **bcrypt**: Library for secure password hashing.

## API Endpoints

### 1. Login

- **URL**: `/api/login`
- **Method**: `POST`
- **Description**: Authenticates the user and returns a JWT token.
- **Parameters**:
  - `username` (string) - User's username.
  - `password` (string) - User's password.
- **Response**:
  - Success: `{"token": "<JWT>"}`
  - Error: `{"error": "Invalid credentials"}`

### 2. Get Employees

- **URL**: `/api/employees`
- **Method**: `GET`
- **Description**: Retrieves all employees, with data like name, job level, and department.
- **Authentication**: Requires a JWT token.
- **Permissions**: Restricted to managers, directors, and HR.
- **Response**:
```json
{
  "user_role": "manager",
  "employees": [
    {
      "id": "1",
      "name": "John",
      "job_level": "Senior",
      "department": "Technology"
    }
  ],
  "total": 10
}
```

### 3. Growth Projections

- **URL**: `/api/employees/projections`
- **Method**: `GET`
- **Description**: Retrieves the growth projections of employees based on semi-annual evaluations.
- **Authentication**: Requires a JWT token.
- **Permissions**: Restricted to managers, directors, and HR.
- **Response**:
```json
{
  "id": "1",
  "name": "John",
  "projections": {
    "Teamwork": {
      "Never": 2,
      "Rarely": 3
    }
  }
}
```

### 4. Add Employee

- **URL**: `/api/employees`
- **Method**: `POST`
- **Description**: Adds a new employee to the database.
- **Authentication**: Requires a JWT token.
- **Permissions**: Restricted to managers and HR.
- **Parameters**:
  - `name` (string) - Employee's name.
  - `job_level` (string) - Job level (e.g., Junior, Senior).
  - `department` (string) - Employee's department.
- **Response**:
  - Success: `{"message": "Employee added successfully"}`
  - Error: `{"error": "Failed to add employee"}`

## Authentication

For endpoints that require authentication, you must include the JWT token in the request header:

```
Authorization: Bearer <your_jwt_token>
```

**Example using curl**:
```bash
curl -X GET http://127.0.0.1:5000/api/employees \
  -H "Authorization: Bearer your_jwt_token_here"
```

**Example using Postman**:
1. Go to the Headers tab
2. Add a new header with:
   - Key: `Authorization`
   - Value: `Bearer your_jwt_token_here`

## Project Structure

```
Flask_Performance_Calc_API/
│
├── app.py                  # Main file that initializes the Flask application.
├── auth.py                 # Contains functions related to authentication and authorization.
├── models.py               # Defines data models (SQLAlchemy).
├── routes.py               # Defines the API routes.
├── services.py             # Contains functions for projections and other business logic.
├── requirements.txt        # Project dependencies.
└── config.py               # Application configuration.
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Pedro-Giorgiano/Flask_Performance_Calc_API.git
```

2. Navigate to the project directory:
```bash
cd Flask_Performance_Calc_API
```

3. Create a virtual environment:
```bash
python3 -m venv venv
```

4. Activate the virtual environment:
   - **On Windows**:
   ```bash
   venv\Scripts\activate
   ```
   - **On macOS/Linux**:
   ```bash
   source venv/bin/activate
   ```

5. Install the dependencies:
```bash
pip install -r requirements.txt
```

6. Run the Flask server:
```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000/`.

## Testing the API

1. **First**, make a POST request to `/api/login` with valid credentials to obtain a JWT token.
2. **Then**, use the returned token in the `Authorization: Bearer <token>` header for all subsequent requests to protected endpoints.
3. **Remember** that different user roles have different access levels to the API endpoints.

## Security Features

- **Password Hashing**: All user passwords are securely hashed using bcrypt before being stored in the database.
- **JWT Authentication**: Stateless authentication using JSON Web Tokens.
- **Role-Based Access Control**: Different user roles have different permissions within the system.