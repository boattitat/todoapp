# Todo Application with MongoDB Atlas

A Python-based Todo application with MongoDB Atlas as the database. This application provides CRUD (Create, Read, Update, Delete) operations for managing todo items.

## Features

- Create new todo items with title, description, due date, and completion status
- Retrieve all todo items or a specific todo by ID
- Update todo items (title, description, due date, completion status)
- Delete todo items
- RESTful API with Flask
- Command-line interface for quick access

## Requirements

- Python 3.7+
- MongoDB Atlas account

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd todoapp
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure MongoDB Atlas:

   - Create a MongoDB Atlas account if you don't have one
   - Create a new cluster
   - Create a database user
   - Get your connection string
   - Copy `.env.example` to `.env` and update with your MongoDB Atlas connection string:

     ```bash
     cp .env.example .env
     ```

   - Edit `.env` with your MongoDB Atlas credentials

4. MongoDB Atlas CLI Setup:

   - Install the MongoDB Atlas CLI:

     ```bash
     # For macOS with Homebrew
     brew install mongodb-atlas-cli

     # For other platforms, see: https://www.mongodb.com/docs/atlas/cli/stable/install-atlas-cli/
     ```

   - Login to your Atlas account:

     ```bash
     atlas auth login
     ```

   - Use the CLI to manage your MongoDB Atlas resources:

     ```bash
     # List your projects
     atlas projects list

     # List clusters in your project
     atlas clusters list

     # Get connection string
     atlas clusters connectionStrings describe <cluster-name>
     ```

   - Update your `.env` file with the connection string obtained from the CLI:

     ```bash
     # Example command to update .env file
     atlas clusters connectionStrings describe <cluster-name> --output json | jq -r '.standardSrv' > .mongodb_uri
     echo "MONGODB_URI=$(cat .mongodb_uri)" > .env
     rm .mongodb_uri
     ```

## Usage

### API Server

Start the Flask API server:

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

- `GET /todos` - Get all todos
- `GET /todos/<id>` - Get a specific todo
- `POST /todos` - Create a new todo
- `PUT /todos/<id>` - Update a todo
- `DELETE /todos/<id>` - Delete a todo

### Command-line Interface

The application includes a command-line interface for quick access:

```bash
python cli.py list                        # List all todos
python cli.py get <id>                    # Get a specific todo
python cli.py create <title> <desc> <due_date> [completed]  # Create a new todo
python cli.py update <id> <field> <value> # Update a todo field
python cli.py complete <id>               # Mark a todo as completed
python cli.py delete <id>                 # Delete a todo
python cli.py help                        # Show help message

## Data Model

Each todo item contains:

- `_id`: Unique identifier (generated automatically)
- `title`: Title of the todo item
- `description`: Detailed description
- `due_date`: Due date in ISO format (YYYY-MM-DD)
- `is_completed`: Boolean indicating completion status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Project Structure

- `app.py` - Flask API server
- `cli.py` - Command-line interface
- `database.py` - MongoDB connection and CRUD operations
- `.env` - Environment variables (MongoDB connection string)
- `requirements.txt` - Python dependencies