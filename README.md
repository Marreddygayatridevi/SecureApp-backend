# 📝 Notes Application

A full-stack Notes application built with **React** (frontend) and **FastAPI** (backend), featuring **JWT Authentication** and **SQLite3** as the database.

---

## 🚀 Getting Started

Follow these steps to set up and run the app locally.

---
### Backend

📁 **Directory**: `Task`

1. Navigate to the your directory:
   ```bash
   cd /../../
   ```
2. Create and activate a virtual environment:
   - **Windows**:
     ```bash
     python -m venv env
     env\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python -m venv env
     source env/bin/activate
     ```
     3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI backend server:
   ```bash
   uvicorn main:app --reload
   ```
5. Alternatively, start the server on a custom port:
   ```bash
   uvicorn main:app --reload --port 8001
   ```
6. Access the API documentation at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---
### SQLite3 Database Access

📁 **File**: `notes.db`

1. Launch the SQLite CLI in the project directory:
   ```bash
   sqlite3 notesapp.db(-> Your database name)
   ```
2. Inside the SQLite CLI:
   - View tables:
     ```sql
     .tables
     ```
   - Change the output format:
     ```sql
     .mode box  -- Or use .mode table / .mode list
     ```
   - View users:
     ```sql
     SELECT * FROM users;
     ```
   - View notes:
     ```sql
     SELECT * FROM notes;
     ```
 📝 **Example Schema for Manual Table Creation**:
```sql
CREATE TABLE users (
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_name TEXT UNIQUE,
  email TEXT,
  hashed_password TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN
);

CREATE TABLE notes (
  note_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  title TEXT,
  content TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME,
  FOREIGN KEY(user_id) REFERENCES users(user_id)
);
```

---

## 🔐 Features

- User authentication with JWT .
- CRUD operations for notes .
- Secure API endpoints requiring authentication.
- Responsive design using Bootstrap.
- Backend with support for SQLite.

---
## 🗂 Directory Structure

- **Backend (`Task`)**:
  - `auth.py`: Authentication routes (Register & Login).
  - `notes.py`: CRUD APIs for managing notes.
  - `main.py`: Entry point for the FastAPI application.
  - `database.py`: SQLite database configuration and setup.
  - `models.py`: Database models defined using SQLAlchemy.
  - **alembic**:
    - `versions `: Contains individual migration scripts
    - `env.py`: Configuration file for Alembic
  - **test_auth**:
    - `test_auth.py`: Test cases for authentication routes
    - `conftest.py` : Common testing setup


---
## Testing:
```bash
   pip install pytest
   ```
---
## Database Migrations:
```bash
   alembic revision --autogenerate -m "Your message"
   ```
 ```bash
   alembic upgrade head
   ```
## API Endpoints

### Authentication

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/auth/`          | Register a new user     |
| POST   | `/auth/token/`    | Obtain access token     |

### Notes Management

| Method | Endpoint                  | Description                 |
| ------ | ------------------------- | -----------------------     |
| GET    | `/notes/notes/`           | Fetch all user notes        |
| GET    | `/notes/{id}/`            | Fetch all user By notes Id  |
| POST   | `/notes/notes/`           | Create a new note           |
| PUT    | `/notes/notes/{note_id}/` | Update a specific note      |
| DELETE | `/notes/notes/{note_id}/` | Delete a specific note      

---


## ✍ Author

by **Marreddy Gayatri Devi**.
---

## 📜 License

This project is available for free use in personal and educational contexts.

---
