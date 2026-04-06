from datetime import datetime

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

    result = []
    today = datetime.today().date()
    for a in assignments:
        is_overdue = False
        # 🔍 Check if assignment is overdue
        if a.deadline:
            try:
                deadline_date = datetime.strptime(a.deadline, "%Y-%m-%d").date()
                is_overdue = deadline_date < today and not a.completed
            except ValueError:
                is_overdue = False  # Invalid date format, treat as not overdue
        
        result.append({
            "id": a.id,
            "title": a.title,
            "deadline": a.deadline,
            "completed": a.completed,
            "is_overdue": is_overdue
        })  
        
    return jsonify(result), 200

# ✅ Mark Assignment as Complete/Incomplete
@assignment_bp.route("/<int:assignment_id>", methods=["PATCH"])
@jwt_required()
def mark_complete(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)

    assignment.completed = not assignment.completed
    db.session.commit()

    return jsonify({"message": "Assignment updated"}), 200

# ✅ Delete Assignment
@assignment_bp.route("/<int:assignment_id>", methods=["DELETE"])
@jwt_required()
def delete_assignment(assignment_id):
    user_id = int(get_jwt_identity())

    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"message": "Assignment not found"}), 404

    # 🔐 Check course ownership
    course = Course.query.filter_by(id=assignment.course_id, user_id=user_id).first()
    if not course:
        return jsonify({"message": "Unauthorized"}), 403

    db.session.delete(assignment)
    db.session.commit()

    return jsonify({"message": "Assignment deleted"}), 200  

