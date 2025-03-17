"""
Command-line interface for Todo application.
"""
import sys
from datetime import datetime
import database as db

def display_todo(todo):
    """Format and display a todo item."""
    print(f"\nID: {todo['_id']}")
    print(f"Title: {todo['title']}")
    print(f"Description: {todo['description']}")
    print(f"Due Date: {todo['due_date']}")
    print(f"Completed: {todo['is_completed']}")
    print(f"Created: {todo.get('created_at', 'N/A')}")
    print(f"Updated: {todo.get('updated_at', 'N/A')}")
    print("-" * 40)

def display_help():
    """Display help information."""
    print("\nTodo Application CLI")
    print("=" * 20)
    print("Commands:")
    print("  list                       - List all todos")
    print("  get <id>                   - Get a specific todo")
    print("  create <title> <desc> <due_date> [completed] - Create a new todo")
    print("  update <id> <field> <value> - Update a todo field")
    print("  complete <id>              - Mark a todo as completed")
    print("  delete <id>                - Delete a todo")
    print("  help                       - Show this help message")
    print("  exit                       - Exit the application")
    print("\nExamples:")
    print("  create 'Buy groceries' 'Milk, eggs, bread' '2023-12-31'")
    print("  update 5f8d0d55b54764b1c86e869a title 'New title'")
    print("  complete 5f8d0d55b54764b1c86e869a")
    print("-" * 40)

def main():
    """Main CLI function."""
    if len(sys.argv) < 2:
        display_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        todos = db.get_all_todos()
        print(f"\nFound {len(todos)} todos:")
        for todo in todos:
            display_todo(todo)

    elif command == "get" and len(sys.argv) >= 3:
        todo_id = sys.argv[2]
        todo = db.get_todo_by_id(todo_id)
        if todo:
            display_todo(todo)
        else:
            print(f"Todo with ID {todo_id} not found.")

    elif command == "create" and len(sys.argv) >= 5:
        title = sys.argv[2]
        description = sys.argv[3]
        due_date = sys.argv[4]
        is_completed = False
        if len(sys.argv) >= 6 and sys.argv[5].lower() in ["true", "yes", "1"]:
            is_completed = True
        
        try:
            # Validate date format
            datetime.fromisoformat(due_date)
            todo = db.create_todo(title, description, due_date, is_completed)
            print("Todo created successfully:")
            display_todo(todo)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")

    elif command == "update" and len(sys.argv) >= 5:
        todo_id = sys.argv[2]
        field = sys.argv[3]
        value = sys.argv[4]
        
        valid_fields = ["title", "description", "due_date", "is_completed"]
        if field not in valid_fields:
            print(f"Error: Invalid field. Valid fields are: {', '.join(valid_fields)}")
            return
        
        updates = {field: value}
        
        # Convert is_completed to boolean
        if field == "is_completed":
            updates[field] = value.lower() in ["true", "yes", "1"]
        
        # Validate date format for due_date
        if field == "due_date":
            try:
                datetime.fromisoformat(value)
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                return
        
        updated_todo = db.update_todo(todo_id, updates)
        if updated_todo:
            print("Todo updated successfully:")
            display_todo(updated_todo)
        else:
            print(f"Todo with ID {todo_id} not found or update failed.")

    elif command == "complete" and len(sys.argv) >= 3:
        todo_id = sys.argv[2]
        updated_todo = db.update_todo(todo_id, {"is_completed": True})
        if updated_todo:
            print("Todo marked as completed:")
            display_todo(updated_todo)
        else:
            print(f"Todo with ID {todo_id} not found or update failed.")

    elif command == "delete" and len(sys.argv) >= 3:
        todo_id = sys.argv[2]
        success = db.delete_todo(todo_id)
        if success:
            print(f"Todo with ID {todo_id} deleted successfully.")
        else:
            print(f"Todo with ID {todo_id} not found or delete failed.")

    elif command == "help":
        display_help()

    elif command == "exit":
        print("Exiting Todo application.")
        sys.exit(0)

    else:
        print("Invalid command or missing arguments.")
        display_help()

if __name__ == "__main__":
    main()
