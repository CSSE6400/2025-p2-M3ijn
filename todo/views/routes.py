from flask import Blueprint, jsonify, request
from todo.models import db
from todo.models.todo import Todo
from datetime import datetime, timedelta

api = Blueprint('api', __name__, url_prefix='/api/v1')

@api.route('/health') 
def health(): 
   return jsonify({"status": "ok"})

@api.route('/todos', methods=['GET'])
def get_todos():
    completed_filter = request.args.get('completed')
    window_filter = request.args.get('window', type=int)

    query = Todo.query

    if completed_filter is not None:
        query = query.filter(Todo.completed == (completed_filter.lower() == 'true'))

    if window_filter is not None:
        query = query.filter(Todo.deadline_at <= datetime.now() + timedelta(days=window_filter))

    todos = query.all()
    
    result = [todo.to_dict() for todo in todos]
    return jsonify(result)

@api.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    return jsonify(todo.to_dict())

@api.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    allowed_fields = ['title', 'description', 'completed', 'deadline_at']
    if any(field not in allowed_fields for field in data):
        return jsonify({'error': 'Invalid field'}), 400
    
    todo = Todo(
        title=data.get('title'),
        description=data.get('description'),
        completed=data.get('completed', False),
    )
    if 'deadline_at' in data:
        try:
            todo.deadline_at = datetime.fromisoformat(request.json.get('deadline_at'))
        except ValueError:
            return jsonify({'error': 'Invalid deadline_at'}), 400

    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@api.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400

    if 'id' in data:
        return jsonify({'error': 'ID cannot be updated'}), 400
    
    allowed_fields = ['title', 'description', 'completed', 'deadline_at']
    if any(field not in allowed_fields for field in data):
        return jsonify({'error': 'Invalid field'}), 400

    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)
    todo.deadline_at = data.get('deadline_at', todo.deadline_at)

    if 'deadline_at' in data:
        try:
            todo.deadline_at = datetime.fromisoformat(request.json.get('deadline_at'))
        except ValueError:
            return jsonify({'error': 'Invalid deadline_at'}), 400

    db.session.commit()
    return jsonify(todo.to_dict())

@api.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    
    if todo is None:
        return jsonify({}), 200

    db.session.delete(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 200