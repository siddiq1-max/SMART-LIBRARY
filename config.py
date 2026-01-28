import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-very-secret-smart-library'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///library.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
