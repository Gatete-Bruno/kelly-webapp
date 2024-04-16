from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

# Initialize Flask application
app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'db'  # Docker Compose service name for MySQL container
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'kelly'
app.config['MYSQL_DB'] = 'task_management_db'

# Initialize MySQL
mysql = MySQL(app)

# Define routes

# Route to retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Task")
    tasks = cur.fetchall()
    cur.close()
    return jsonify(tasks)

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    title = data['title']
    description = data['description']
    due_date = data['due_date']
    category_id = data['category_id']
    priority_id = data['priority_id']
    status_id = data['status_id']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Task (Title, Description, DueDate, CategoryID, PriorityID, StatusID) VALUES (%s, %s, %s, %s, %s, %s)", (title, description, due_date, category_id, priority_id, status_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task created successfully"})

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
