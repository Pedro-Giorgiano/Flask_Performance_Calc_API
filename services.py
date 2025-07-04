from models import session, Employee, Evaluation
from performance_utils import calculate_projection


# Employee part


def get_employee_profile(user_id):
    employee = session.query(Employee).filter_by(id=user_id).first()
    if not employee:
        return None
    return employee


def get_employee_performance(user_id):
    employee = session.query(Employee).filter_by(id=user_id).first()
    if not employee:
        return None

    evaluations = (
        session.query(Evaluation)
        .filter_by(employee_id=user_id)
        .order_by(Evaluation.semester)
        .all()
    )

    history = []
    for ev in evaluations:
        history.append({
            "semester": ev.semester,
            "scores": ev.scores
        })

    return {
        "employee": employee,
        "evaluation_history": history
    }


def get_employee_projection(employee_id):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    if not employee:
        return None

    last_evaluation = (
        session.query(Evaluation)
        .filter_by(employee_id=employee_id)
        .order_by(Evaluation.semester.desc())
        .first()
    )

    if not last_evaluation:
        return {
            "employee": employee,
            "next_semester_projection": "Not yet evaluated"
        }

    projection = {}
    for category, items in last_evaluation.scores.items():
        projected_category = {}
        for item, freq in items.items():
            projected_category[item] = calculate_projection(freq)
        projection[category] = projected_category

    return {
        "employee": employee,
        "next_semester_projection": projection
    }


# Manger part


def get_all_employee_evaluations():
    employees = session.query(Employee).all()
    result = []

    for emp in employees:
        emp_data = {
            "id": emp.id,
            "name": emp.name,
            "job_level": emp.job_level,
            "career_track": emp.career_track,
            "time_in_company": emp.time_in_company,
            "time_in_current_role": emp.time_in_current_role,
            "evaluations": []
        }

        for ev in emp.evaluations:
            emp_data["evaluations"].append({
                "semester": ev.semester,
                "scores": ev.scores
            })

        result.append(emp_data)

    return result


def get_employees_projections():
    employees = session.query(Employee).all()
    result = []

    for emp in employees:
        last_evaluation = (
            session.query(Evaluation)
            .filter_by(employee_id=emp.id)
            .order_by(Evaluation.semester.desc())
            .first()
        )

        if last_evaluation:
            projection = {}
            for category, items in last_evaluation.scores.items():
                projected_category = {}
                for item, freq in items.items():
                    projected_category[item] = calculate_projection(freq)
                projection[category] = projected_category
        else:
            projection = "Not yet evaluated"

        emp_data = {
            "id": emp.id,
            "name": emp.name,
            "job_level": emp.job_level,
            "career_track": emp.career_track,
            "time_in_company": emp.time_in_company,
            "time_in_current_role": emp.time_in_current_role,
            "next_semester_projection": projection
        }

        result.append(emp_data)

    return result


def get_basic_employee_data():
    employees = session.query(Employee).all()
    result = []

    for emp in employees:
        emp_data = {
            "id": emp.id,
            "name": emp.name,
            "job_level": emp.job_level,
            "career_track": emp.career_track,
            "time_in_company": emp.time_in_company,
            "time_in_current_role": emp.time_in_current_role
        }
        result.append(emp_data)

    return result


