from flask import Blueprint, jsonify
from extensions import db
from models.course import Course
from models.assignment import Assignment
from flask_jwt_extended import jwt_required, get_jwt_identity

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/", methods=["GET"])
@jwt_required()
def get_dashboard():
    user_id = int(get_jwt_identity())

    # Get user's courses
    courses = Course.query.filter_by(user_id=user_id).all()
    course_ids = [c.id for c in courses]

    # Get assignments linked to those courses
    assignments = Assignment.query.filter(Assignment.course_id.in_(course_ids)).all()

    total_courses = len(courses)
    total_assignments = len(assignments)
    completed = len([a for a in assignments if a.completed])
    pending = total_assignments - completed

    return jsonify({
        "total_courses": total_courses,
        "total_assignments": total_assignments,
        "completed": completed,
        "pending": pending
    })