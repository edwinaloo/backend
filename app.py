from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db, bcrypt, jwt

app = Flask(__name__)
app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

CORS(app)

db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Import routes AFTER app is created
from routes.auth import auth_bp
from routes.course import course_bp
from routes.assignment import assignment_bp
from routes.dashboard import dashboard_bp

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(course_bp, url_prefix="/courses")
app.register_blueprint(assignment_bp, url_prefix="/assignments")
app.register_blueprint(dashboard_bp, url_prefix="/dashboard")


@app.route("/")
def home():
    return {"message": "StudyFlow API running"}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)