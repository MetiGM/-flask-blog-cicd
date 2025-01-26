import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'insecure-secret-key')  # Use environment variable
db = SQLAlchemy(app)

from app import routes, models