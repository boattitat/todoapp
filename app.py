"""
Flask API for Todo application with MongoDB Atlas.
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import dateutil.parser
import database as db

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Return API information."""
    return jsonify({
        "message": "Todo API is running",
        "version": "1.0.0",
        "endpoints": {
            "GET /todos": "Get all todos",
            "GET /todos/<id>": "Get a specific todo",
            "POST /todos": "Create a new todo",
            "PUT /todos/<id>": "Update a todo",
            "DELETE /todos/<id>": "Delete a todo"
        }
    })

@app.route('/todos', methods=['GET'])
def get_todos():
    """Get all todos."""
    todos = db.get_all_todos()
    return jsonify(todos)

@app.route('/todos/<todo_id>', methods=['GET'])
def get_todo(todo_id):
    """Get a specific todo by ID."""
    todo = db.get_todo_by_id(todo_id)
    if todo:
        return jsonify(todo)
    return jsonify({"error": "Todo not found"}), 404

@app.route('/todos', methods=['POST'])
def create_todo():
    """Create a new todo."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'due_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate due_date format
    try:
        due_date = dateutil.parser.parse(data['due_date']).isoformat()
    except ValueError:
        return jsonify({"error": "Invalid date format for due_date"}), 400
    
    # Create todo
    is_completed = data.get('is_completed', False)
    todo = db.create_todo(
        data['title'],
        data['description'],
        due_date,
        is_completed
    )
    
    return jsonify(todo), 201

@app.route('/todos/<todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Update a todo by ID."""
    data = request.get_json()
    
    # Validate that at least one field is being updated
    valid_fields = ['title', 'description', 'due_date', 'is_completed']
    updates = {k: v for k, v in data.items() if k in valid_fields}
    
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    
    # Validate due_date format if provided
    if 'due_date' in updates:
        try:
            updates['due_date'] = dateutil.parser.parse(updates['due_date']).isoformat()
        except ValueError:
            return jsonify({"error": "Invalid date format for due_date"}), 400
    
    # Update todo
    updated_todo = db.update_todo(todo_id, updates)
    
    if updated_todo:
        return jsonify(updated_todo)
    return jsonify({"error": "Todo not found or update failed"}), 404

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Delete a todo by ID."""
    success = db.delete_todo(todo_id)
    
    if success:
        return jsonify({"message": "Todo deleted successfully"}), 200
    return jsonify({"error": "Todo not found or delete failed"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
