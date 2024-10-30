import sqlite3  # Importing SQLite3 library for database management


class Database:

    def __init__(self):
        # Initialize the database by creating tables if they don't exist
        self.create_db()

    # Function to create necessary database tables if they don't exist
    def create_db(self):
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Create 'users' table with unique email and login fields
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            login TEXT UNIQUE,
            password TEXT
        )
        ''')

        # Create 'notes' table, each note linked to a specific user
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            note TEXT,
            priority INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        conn.commit()  # Save changes to the database
        conn.close()  # Close the database connection

    # Check if an email is already registered
    def check_email(self, email):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Query to check if email already exists in the users table
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()  # Fetch the first matching result

        conn.close()
        return user is not None  # Return True if email exists, False if it doesn't

    # Check if a login is already taken
    def check_login(self, login):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Query to check if login already exists in the users table
        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = cursor.fetchone()  # Fetch the first matching result

        conn.close()
        return user is not None  # Return True if login exists, False if it doesn't

    # Register a new user by inserting their details into the users table
    def register_user(self, email, login, password):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Insert the user's email, login, and password into the users table
        cursor.execute('INSERT INTO users (email, login, password) VALUES (?, ?, ?)', (email, login, password))
        conn.commit()  # Save the new user to the database
        conn.close()

        return True

    # Authenticate a user by checking if email and password match a user record
    def login_user(self, email, password):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Query to check if provided email and password match a record in users
        cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()  # Fetch the first matching result
        conn.close()

        if user:
            return user[0]  # Return the user ID if login successful
        else:
            return None  # Return None if login failed

    # Create a new note for a user by inserting it into the notes table
    def create_note(self, user_id, note, priority):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Insert note content and priority linked to the user ID
        cursor.execute('INSERT INTO notes (user_id, note, priority) VALUES (?, ?, ?)', (user_id, note, priority))
        conn.commit()  # Save the new note to the database
        conn.close()

    # Retrieve all notes for a specific user
    def get_user_notes(self, user_id):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Select all notes for a given user ID
        cursor.execute('SELECT * FROM notes WHERE user_id=?', (user_id,))
        notes = cursor.fetchall()  # Fetch all matching notes
        conn.close()

        return notes

    # Delete a specific note by its note ID
    def delete_note(self, note_id):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Delete a note with the specified note ID
        cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))
        conn.commit()  # Commit changes to reflect deletion in the database
        conn.close()

    # Retrieve and sort user notes with optional search and sorting criteria
    def get_user_notes_sorted(self, search_query="", sort_by="priority"):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Query to search notes containing the search_query and sort by chosen column
        query = "SELECT * FROM notes WHERE note LIKE ? ORDER BY " + (sort_by if sort_by else "priority")
        cursor.execute(query, (f"%{search_query}%",))  # Execute query with search pattern
        notes = cursor.fetchall()  # Fetch all matching notes

        conn.close()
        return notes
