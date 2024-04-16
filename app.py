from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)

# Configure MySQL connection
DB_USERNAME = os.environ.get('DB_USERNAME', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'kelly')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'task_management_db')

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your models here
class Task(db.Model):
    __tablename__ = 'Task'
    TaskID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)
    DueDate = db.Column(db.Date)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Category.CategoryID'))
    PriorityID = db.Column(db.Integer, db.ForeignKey('Priority.PriorityID'))
    StatusID = db.Column(db.Integer, db.ForeignKey('Status.StatusID'))

    # Define relationships here
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))
    priority = db.relationship('Priority', backref=db.backref('tasks', lazy=True))
    status = db.relationship('Status', backref=db.backref('tasks', lazy=True))

class Category(db.Model):
    __tablename__ = 'Category'
    CategoryID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)

class Priority(db.Model):
    __tablename__ = 'Priority'
    PriorityID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)

class Status(db.Model):
    __tablename__ = 'Status'
    StatusID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)

# Define your routes here
@app.route('/')
def index():
    return 'Hello, World!'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
