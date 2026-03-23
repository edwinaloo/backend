import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///studyflow.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False