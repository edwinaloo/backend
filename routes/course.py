from flask import Blueprint, request, jsonify
from extensions import db
from models.course import Course
from flask_jwt_extended import jwt_required, get_jwt_identity

course_bp = Blueprint("courses", __name__)

@course_bp.route("/", methods=["POST"])
@jwt_required()
def create_course():
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get("title")

    new_course = Course(title=title, user_id=user_id)
    db.session.add(new_course)
    db.session.commit()

    return jsonify({"message": "Course created"}), 201


@course_bp.route("/", methods=["GET"])
@jwt_required()
def get_courses():
    user_id = get_jwt_identity()

    courses = Course.query.filter_by(user_id=user_id).all()

    result = []
    for course in courses:
        result.append({
            "id": course.id,
            "title": course.title
        })

    return jsonify(result), 200