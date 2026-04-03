from flask import Blueprint, request, jsonify
from extensions import db
from models.assignment import Assignment
from models.course import Course
from flask_jwt_extended import jwt_required, get_jwt_identity

assignment_bp = Blueprint("assignments", __name__)

# ✅ Create Assignment
@assignment_bp.route("/course/<int:course_id>", methods=["POST"])
@jwt_required()
def create_assignment(course_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    # 🔐 Check course ownership
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()
    if not course:
        return jsonify({"message": "Unauthorized"}), 403

    title = data.get("title")

    if not title:
        return jsonify({"message": "Title is required"}), 400

    new_assignment = Assignment(
        title=title,
        description=data.get("description"),
        deadline=data.get("deadline"),
        course_id=course_id,
        completed=False
    )

    db.session.add(new_assignment)
    db.session.commit()

    return jsonify({"message": "Assignment created"}), 201


# ✅ Get Assignments for a Course
@assignment_bp.route("/course/<int:course_id>", methods=["GET"])
@jwt_required()
def get_assignments(course_id):
    assignments = Assignment.query.filter_by(course_id=course_id).all()

    result = [
        {
            "id": a.id,
            "title": a.title,
            "deadline": a.deadline,
            "completed": a.completed
        }
        for a in assignments
    ]

    return jsonify(result), 200