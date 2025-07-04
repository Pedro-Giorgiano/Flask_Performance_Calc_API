from flask import Blueprint, jsonify, request
from auth import token_required
from dotenv import load_dotenv
import os

from services import get_all_employee_evaluations, get_employees_projections, get_basic_employee_data, \
    get_employee_profile, get_employee_performance, get_employee_projection

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

routes = Blueprint('routes', __name__)

# check the api state
@routes.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "API is working!"})


# Employee part

#return user projection by id from header
@routes.route('/api/my-projection', methods=['GET'])
@token_required
def get_my_projection():
    employee_id = request.user.get("user_id")

    projection_data = get_employee_projection(employee_id) # function from services
    if not projection_data:
        return jsonify({"error": "Employee not found"}), 404

    employee = projection_data["employee"]
    projection = projection_data["next_semester_projection"]

    return jsonify({
        "employee_id": employee.id,
        "name": employee.name,
        "job_level": employee.job_level,
        "career_track": employee.career_track,
        "next_semester_projection": projection
    })

#return user performance by id from header
@routes.route('/api/my-performance', methods=['GET'])
@token_required
def get_my_performance():
    user_id = request.user.get("user_id")

    performance_data = get_employee_performance(user_id)
    if not performance_data:
        return jsonify({"error": "Employee not found"}), 404

    employee = performance_data["employee"]
    history = performance_data["evaluation_history"]

    return jsonify({
        "employee_id": employee.id,
        "name": employee.name,
        "job_level": employee.job_level,
        "career_track": employee.career_track,
        "time_in_company": employee.time_in_company,
        "time_in_current_role": employee.time_in_current_role,
        "evaluation_history": history
    })


#get user data by id from header
@routes.route('/api/my-profile', methods=['GET'])
@token_required
def get_my_profile():
    user_id = request.user.get("user_id")

    employee = get_employee_profile(user_id)
    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "employee_id": employee.id,
        "name": employee.name,
        "job_level": employee.job_level,
        "career_track": employee.career_track,
        "time_in_company": employee.time_in_company,
        "time_in_current_role": employee.time_in_current_role
    })


# Manger part

# get all users using role
@routes.route('/api/employees/list', methods=['GET'])
@token_required
def get_all_basic_employee_data():
    user_role = request.user.get('role', '')

    if user_role not in ['manager', 'director', 'hr']:
        return jsonify({"error": "Access denied"}), 403

    result = get_basic_employee_data()

    return jsonify({
        "employees": result,
        "total_of_employees": len(result)
    })

# get all projections by role
@routes.route('/api/employees/projections', methods=['GET'])
@token_required
def get_all_projections_by_role():
    user_role = request.user.get('role', '')

    if user_role not in ['manager', 'director', 'hr']:
        return jsonify({"error": "Access denied"}), 403

    result = get_employees_projections()

    return jsonify({
        "employees": result,
        "total_of_employees": len(result)
    })

# get all user data and evaluations using role
@routes.route('/api/employees/evaluations', methods=['GET'])
@token_required
def get_all_evaluations_by_role():
    user_role = request.user.get('role', '')

    # Verify role
    if user_role not in ['manager', 'director', 'hr']:
        return jsonify({"error": "Access denied"}), 403

    employees_data = get_all_employee_evaluations()

    return jsonify({
        "employees": employees_data,
        "total of employees": len(employees_data)
    })

