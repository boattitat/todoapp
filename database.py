"""
Database module for MongoDB Atlas connection and operations.
"""
import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

# Load environment variables
load_dotenv()

# MongoDB connection settings
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "todo_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "todos")

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
todos_collection = db[COLLECTION_NAME]

def create_todo(title, description, due_date, is_completed=False):
    """
    Create a new todo item in the database.
    
    Args:
        title (str): Title of the todo item
        description (str): Description of the todo item
        due_date (str): Due date of the todo item (ISO format)
        is_completed (bool, optional): Completion status. Defaults to False.
        
    Returns:
        dict: Created todo item with ID
    """
    todo = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "is_completed": is_completed,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat()
    }
    
    result = todos_collection.insert_one(todo)
    todo["_id"] = str(result.inserted_id)
    return todo

def get_all_todos():
    """
    Retrieve all todo items from the database.
    
    Returns:
        list: List of todo items
    """
    todos = list(todos_collection.find())
    # Convert ObjectId to string for JSON serialization
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return todos

def get_todo_by_id(todo_id):
    """
    Retrieve a specific todo item by ID.
    
    Args:
        todo_id (str): ID of the todo item
        
    Returns:
        dict: Todo item if found, None otherwise
    """
    try:
        todo = todos_collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            todo["_id"] = str(todo["_id"])
        return todo
    except Exception:
        return None

def update_todo(todo_id, updates):
    """
    Update a todo item in the database.
    
    Args:
        todo_id (str): ID of the todo item to update
        updates (dict): Fields to update
        
    Returns:
        dict: Updated todo item if successful, None otherwise
    """
    try:
        # Add updated_at timestamp
        updates["updated_at"] = datetime.utcnow().isoformat()
        
        # Perform the update
        result = todos_collection.update_one(
            {"_id": ObjectId(todo_id)},
            {"$set": updates}
        )
        
        if result.modified_count > 0:
            return get_todo_by_id(todo_id)
        return None
    except Exception:
        return None

def delete_todo(todo_id):
    """
    Delete a todo item from the database.
    
    Args:
        todo_id (str): ID of the todo item to delete
        
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    try:
        result = todos_collection.delete_one({"_id": ObjectId(todo_id)})
        return result.deleted_count > 0
    except Exception:
        return False
