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
```json
{
	"username": "aline",
	"password": "xyz"
}
```

### 2. Get Employees

- **URL**: `api/employees/list`
- **Method**: `GET`
- **Description**: Retrieves all employees, with data like name, job level, and department.
- **Authentication**: Requires a JWT token.
- **Permissions**: Restricted to managers, directors, and HR.
- **Response**:
```json
{
	"employees": [
		{
			"career_track": "Technical",
			"id": "emp001",
			"job_level": "Mid",
			"name": "João Silva",
			"time_in_company": 30,
			"time_in_current_role": 12
		},
		{
			"career_track": "Technical",
			"id": "emp002",
			"job_level": "Senior",
			"name": "Maria Oliveira",
			"time_in_company": 48,
			"time_in_current_role": 24
		},
		{
			"career_track": "Management",
			"id": "emp003",
			"job_level": "Director",
			"name": "Carlos Director",
			"time_in_company": 72,
			"time_in_current_role": 36
		},
		{
			"career_track": "Technical",
			"id": "emp004",
			"job_level": "Junior",
			"name": "Lucas Martins",
			"time_in_company": 12,
			"time_in_current_role": 6
		},
		{
			"career_track": "Menagement",
			"id": "emp005",
			"job_level": "Tech Lead",
			"name": "Aline Costa",
			"time_in_company": 60,
			"time_in_current_role": 18
		}
	],
	"total_of_employees": 5
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
	"employees": [
		{
			"career_track": "Technical",
			"id": "emp001",
			"job_level": "Mid",
			"name": "João Silva",
			"next_semester_projection": {
				"Teamwork": {
					"Collaborates with peers": "Always",
					"Shares knowledge": "Always"
				},
				"Technical Quality": {
					"Delivers with quality": "Always"
				}
			},
			"time_in_company": 30,
			"time_in_current_role": 12
		},
		{
			"career_track": "Technical",
			"id": "emp002",
			"job_level": "Senior",
			"name": "Maria Oliveira",
			"next_semester_projection": {
				"Leadership": {
					"Gives constructive feedback": "Always",
					"Provides clear direction": "Always"
				},
				"Teamwork": {
					"Fosters collaboration": "Always"
				}
			},
			"time_in_company": 48,
			"time_in_current_role": 24
		},
		{
			"career_track": "Management",
			"id": "emp003",
			"job_level": "Director",
			"name": "Carlos Director",
			"next_semester_projection": "Not yet evaluated",
			"time_in_company": 72,
			"time_in_current_role": 36
		},
		{
			"career_track": "Technical",
			"id": "emp004",
			"job_level": "Junior",
			"name": "Lucas Martins",
			"next_semester_projection": {
				"Teamwork": {
					"Collaborates with peers": "Almost always",
					"Shares knowledge": "Frequently"
				},
				"Technical Quality": {
					"Delivers with quality": "Almost always"
				}
			},
			"time_in_company": 12,
			"time_in_current_role": 6
		},
		{
			"career_track": "Menagement",
			"id": "emp005",
			"job_level": "Tech Lead",
			"name": "Aline Costa",
			"next_semester_projection": {
				"Leadership": {
					"Manages complexity": "Always",
					"Supports team growth": "Always"
				},
				"Teamwork": {
					"Shares knowledge": "Always"
				}
			},
			"time_in_company": 60,
			"time_in_current_role": 18
		}
	],
	"total_of_employees": 5
}
```

## Authentication

For endpoints that require authentication, you must include the JWT token in the request header:

```
Authorization: Bearer <your_jwt_token>
```

**Example using curl**:
```bash
curl -X GET http://127.0.0.1:5000/api/my-performance \
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
├── performance_utils.py    # Helper functions for performance calculations, such as calculating projections and handling metrics.
└── requirements.txt        # Project dependencies.
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
