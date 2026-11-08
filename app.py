from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

def get_db():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        database='taskmanager',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return '<html><body><h2>Task Manager</h2><form method="POST" action="/tasks"><input type="text" name="title" placeholder="Enter task" required><button type="submit">Add Task</button></form><br><a href="/tasks">View all tasks</a></body></html>'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            tasks = cursor.fetchall()
        return jsonify(tasks)
    finally:
        conn.close()

@app.route('/tasks', methods=['POST'])
def add_task():
    title = request.form.get('title')
    conn = get_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        return '<html><body><p>Task added.</p><a href="/">Go back</a></body></html>'
    finally:
        conn.close()

if __name__ == '__main__':
    app.run()
