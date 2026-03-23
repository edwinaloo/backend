from flask import Blueprint, request, jsonify
from extensions import db
from models.assignment import Assignment
from flask_jwt_extended import jwt_required, get_jwt_identity

assignment_bp = Blueprint("assignments", __name__)

from models.course import Course

@assignment_bp.route("/", methods=["POST"])
@jwt_required()
def create_assignment():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    course_id = data.get("course_id")

    # 🔐 Check ownership
    course = Course.query.filter_by(id=course_id, user_id=user_id).first()

    if not course:
        return jsonify({"message": "Unauthorized"}), 403

    new_assignment = Assignment(
        title=data.get("title"),
        description=data.get("description"),
        deadline=data.get("deadline"),
        course_id=course_id
    )

    db.session.add(new_assignment)
    db.session.commit()

    return jsonify({"message": "Assignment created"}), 201


@assignment_bp.route("/<int:course_id>", methods=["GET"])
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