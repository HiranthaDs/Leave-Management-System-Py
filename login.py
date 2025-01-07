import sqlite3
from tkinter import *
from tkinter import messagebox
import user
import admin


class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("400x300")

        # Create the login form
        self.email_label = Label(root, text="Email")
        self.email_label.pack(pady=10)
        self.email_entry = Entry(root)
        self.email_entry.pack(pady=10)

        self.password_label = Label(root, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(root, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = Button(root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = Button(root, text="Register", command=self.register)
        self.register_button.pack(pady=10)

        # Initialize the database
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect("leave_management.db")
        cursor = conn.cursor()

        # Create users table if it doesn't exist
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        # Create leave_requests table if it doesn't exist
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS leave_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                job_id TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                leave_dates TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        conn.close()

        # Insert default users if the table is empty
        self.insert_default_users()

    def insert_default_users(self):
        conn = sqlite3.connect("leave_management.db")
        cursor = conn.cursor()

        # Insert admin user if not already present
        cursor.execute("SELECT * FROM users WHERE email = ?", ("admin@email.com",))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                           ("Admin User", "admin@email.com", "admin", "admin"))

        # Insert regular user if not already present
        cursor.execute("SELECT * FROM users WHERE email = ?", ("user@email.com",))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                           ("User", "user@email.com", "user", "user"))

        conn.commit()
        conn.close()

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return

        conn = sqlite3.connect("leave_management.db")
        cursor = conn.cursor()

        # Check if the user exists in the database
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            # Successful login
            self.root.withdraw()
            messagebox.showinfo("Login Successful", f"Welcome, {user_data[1]}!")

            # Pass the user_id and role (either admin or user)
            self.open_dashboard(user_data[0], user_data[4])  # Pass user_id and role
        else:
            # Login failed
            messagebox.showerror("Login Failed", "Invalid email or password!")

    def register(self):
        self.register_window = Toplevel(self.root)
        self.register_window.title("Register User")
        self.register_window.geometry("400x300")

        self.register_name_label = Label(self.register_window, text="Name")
        self.register_name_label.pack(pady=10)
        self.register_name_entry = Entry(self.register_window)
        self.register_name_entry.pack(pady=10)

        self.register_email_label = Label(self.register_window, text="Email")
        self.register_email_label.pack(pady=10)
        self.register_email_entry = Entry(self.register_window)
        self.register_email_entry.pack(pady=10)

        self.register_password_label = Label(self.register_window, text="Password")
        self.register_password_label.pack(pady=10)
        self.register_password_entry = Entry(self.register_window, show="*")
        self.register_password_entry.pack(pady=10)

        self.register_role_label = Label(self.register_window, text="Role (admin/user)")
        self.register_role_label.pack(pady=10)
        self.register_role_entry = Entry(self.register_window)
        self.register_role_entry.pack(pady=10)

        self.register_button = Button(self.register_window, text="Register", command=self.save_user)
        self.register_button.pack(pady=20)

    def save_user(self):
        name = self.register_name_entry.get()
        email = self.register_email_entry.get()
        password = self.register_password_entry.get()
        role = self.register_role_entry.get()

        if not name or not email or not password or not role:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        conn = sqlite3.connect("leave_management.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                           (name, email, password, role))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
        finally:
            conn.close()

    def open_dashboard(self, user_id, role):
        if role == "admin":
            # Open the Admin Dashboard
            admin_root = Tk()
            admin_dashboard = admin.AdminDashboard(admin_root)
            admin_root.mainloop()
        elif role == "user":
            # Open the User Dashboard
            user_root = Tk()
            user_dashboard = user.UserDashboard(user_root, user_id)
            user_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid user role!")

if __name__ == "__main__":
    root = Tk()
    app = LoginSystem(root)
    root.mainloop()
