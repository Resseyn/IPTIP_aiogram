from flask import jsonify

from loader import app


@app.route('/', methods=['GET'])
def get_tasks():
    tasks = [
        {"id": 1, "title": "Task 1"},
        {"id": 2, "title": "Task 2"}
    ]
    return jsonify({"tasks": tasks})
