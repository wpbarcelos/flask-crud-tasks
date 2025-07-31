from flask import Flask, request, jsonify
from models.task import Task
app = Flask(__name__)

tasks = []

task_id_control = 1


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control,
                    title=data.get("title"),
                    description=data.get("description"))
    task_id_control += 1
    tasks.append(new_task)
    return jsonify({"message": "Task was created successfully"}), 201


@app.route('/tasks', methods=["GET"])
def list_tasks():
    tasks_list = [task.to_dict() for task in tasks]
    tasks_completed = [task for task in tasks if task.completed]
    return jsonify({"tasks": tasks_list, "total_tasks": len(tasks_list), "tasks_completed": len(tasks_completed)})


@app.route('/tasks/<int:task_id>', methods=["GET"])
def read_task(task_id):

    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict())

    return jsonify({"message": "tasks not found"}), 404


@app.route('/tasks/<int:task_id>/update', methods=['PUT'])
def update_task(task_id):

    task = None
    for i in tasks:
        if i.id == task_id:
            task = i
            break

    if task is None:
        return jsonify({"message": "tasks not found"}), 404

    data = request.get_json()
    task.title = data.get('title')
    task.description = data.get('description')
    task.completed = data.get('completed')
    return jsonify({"message": "Task as been updated successfully"})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):

    task = None

    for i in tasks:
        if i.id == task_id:
            task = i
            break

    if task is None:
        return jsonify({"message": "Task not found"}), 404

    tasks.remove(task)

    return jsonify({"message": "task as been deleted successfully"}), 200


@app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    task = None

    for i in tasks:
        if i.id == task_id:
            task = i
    if task is None:
        return jsonify({"message": "Task not found"}), 404

    task.completed = True

    return jsonify({"message": "Task completed with successfully"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
