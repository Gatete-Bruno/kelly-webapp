from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def authenticate():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return db_url

db = SQLAlchemy(app)

# Define SQLAlchemy models
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

class Task(db.Model):
    __tablename__ = 'Task'
    TaskID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text)
    DueDate = db.Column(db.Date)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Category.CategoryID'))
    PriorityID = db.Column(db.Integer, db.ForeignKey('Priority.PriorityID'))
    StatusID = db.Column(db.Integer, db.ForeignKey('Status.StatusID'))
    
    category = db.relationship('Category', backref=db.backref('tasks'))
    priority = db.relationship('Priority', backref=db.backref('tasks'))
    status = db.relationship('Status', backref=db.backref('tasks'))

class TaskComment(db.Model):
    __tablename__ = 'TaskComment'
    CommentID = db.Column(db.Integer, primary_key=True)
    TaskID = db.Column(db.Integer, db.ForeignKey('Task.TaskID'))
    Comment = db.Column(db.Text)
    Timestamp = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    task = db.relationship('Task', backref=db.backref('comments'))

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_task', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        task_name = request.form['task_name']
        task_description = request.form['task_description']
        task_due_date = request.form['task_due_date']
        category_name = request.form['category']
        priority_name = request.form['priority']
        status_name = request.form['status']
        
        # Fetch category, priority, and status objects
        category = Category.query.filter_by(Name=category_name).first()
        priority = Priority.query.filter_by(Name=priority_name).first()
        status = Status.query.filter_by(Name=status_name).first()
        
        # Create new task object
        new_task = Task(Title=task_name, Description=task_description, DueDate=task_due_date,
                        Category=category, Priority=priority, Status=status)
        
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        categories = Category.query.all()
        priorities = Priority.query.all()
        statuses = Status.query.all()
        return render_template('create_task.html', categories=categories, priorities=priorities, statuses=statuses)

@app.route('/view_task/<task_id>')
def view_task(task_id):
    task = Task.query.get(task_id)
    return render_template('view_task.html', task=task)

if __name__ == '__main__':
    db_url = authenticate()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.run(debug=True)
