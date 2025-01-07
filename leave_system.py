import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


# Function to initialize the database and create tables
def init_db():
    conn = sqlite3.connect('leave_management.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    ''')

    # Create leave_requests table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        leave_dates TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()


# Initialize the database if needed
init_db()


class LeaveSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Leave Management System")
        self.root.geometry("400x300")

        # Login Form
        self.email_label = Label(self.root, text="Email")
        self.email_label.pack(pady=10)
        self.email_entry = Entry(self.root)
        self.email_entry.pack(pady=10)

        self.password_label = Label(self.root, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = Button(self.root, text="Register", command=self.register)
        self.register_button.pack(pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password!")
            return

        conn = sqlite3.connect('leave_management.db')
        cursor = conn.cursor()

        # Verify user credentials
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.root.withdraw()
            messagebox.showinfo("Login Successful", f"Welcome, {user[1]}!")
            self.open_dashboard(user[4])  # Pass user role to dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid email or password!")

    def open_dashboard(self, role):
        if role == "admin":
            admin_dashboard = AdminDashboard(Tk())
            admin_dashboard.mainloop()
        elif role == "user":
            user_dashboard = UserDashboard(Tk())
            user_dashboard.mainloop()
        else:
            messagebox.showerror("Error", "Invalid role!")

    def register(self):
        # Registration Form (similar to login form)
        self.register_window = Toplevel(self.root)
        self.register_window.title("Register User")
        self.register_window.geometry("400x300")

        self.name_label = Label(self.register_window, text="Name")
        self.name_label.pack(pady=10)
        self.name_entry = Entry(self.register_window)
        self.name_entry.pack(pady=10)

        self.email_label = Label(self.register_window, text="Email")
        self.email_label.pack(pady=10)
        self.email_entry = Entry(self.register_window)
        self.email_entry.pack(pady=10)

        self.password_label = Label(self.register_window, text="Password")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(self.register_window, show="*")
        self.password_entry.pack(pady=10)

        self.role_label = Label(self.register_window, text="Role (admin/user)")
        self.role_label.pack(pady=10)
        self.role_entry = Entry(self.register_window)
        self.role_entry.pack(pady=10)

        self.register_button = Button(self.register_window, text="Register", command=self.save_user)
        self.register_button.pack(pady=20)

    def save_user(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if not name or not email or not password or not role:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        conn = sqlite3.connect('leave_management.db')
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


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("600x400")

        self.tree = ttk.Treeview(self.root, columns=("ID", "User", "Leave Dates", "Status"))
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="User")
        self.tree.heading("#3", text="Leave Dates")
        self.tree.heading("#4", text="Status")
        self.tree.pack(pady=20)

        self.load_leave_requests()

        self.logout_button = Button(self.root, text="Logout", command=self.logout, bg="lightcoral")
        self.logout_button.pack(pady=20)

    def load_leave_requests(self):
        conn = sqlite3.connect('leave_management.db')
        cursor = conn.cursor()

        cursor.execute("SELECT lr.id, u.name, lr.leave_dates, lr.status FROM leave_requests lr "
                       "JOIN users u ON lr.user_id = u.id")
        leave_requests = cursor.fetchall()

        for request in leave_requests:
            self.tree.insert("", "end", values=request)

        conn.close()

    def logout(self):
        self.root.quit()


class UserDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("User Dashboard")
        self.root.geometry("600x400")

        self.leave_date_label = Label(self.root, text="Leave Dates (YYYY-MM-DD)")
        self.leave_date_label.pack(pady=10)
        self.leave_date_entry = Entry(self.root)
        self.leave_date_entry.pack(pady=10)

        self.submit_button = Button(self.root, text="Submit Leave Request", command=self.submit_leave_request,
                                    bg="#24a0ed")
        self.submit_button.pack(pady=20)

        self.logout_button = Button(self.root, text="Logout", command=self.logout, bg="lightcoral")
        self.logout_button.pack(pady=20)

    def submit_leave_request(self):
        leave_dates = self.leave_date_entry.get()

        if not leave_dates:
            messagebox.showerror("Error", "Please enter leave dates!")
            return

        user_id = 1  # Replace with the actual logged-in user's ID

        conn = sqlite3.connect('leave_management.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO leave_requests (user_id, leave_dates, status) VALUES (?, ?, ?)",
                       (user_id, leave_dates, "pending"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Leave request submitted successfully!")

    def logout(self):
        self.root.quit()


if __name__ == "__main__":
    root = Tk()
    app = LeaveSystem(root)
    root.mainloop()
