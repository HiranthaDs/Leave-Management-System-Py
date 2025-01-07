import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk  # Importing Pillow for handling images


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login App")
        self.root.geometry("300x200")

        # Load the background image using Pillow
        bg_image_path = r"C:\Users\Administrator\Desktop\Git Work\Python\Project\Image\background.png"  # Use the correct path
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((300, 200), Image.Resampling.LANCZOS)  # Correct resampling method

        # Convert the image to Tkinter compatible format
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas to hold the background image
        self.canvas = Canvas(self.root, width=300, height=200)
        self.canvas.pack(fill=BOTH, expand=True)

        # Add the background image to the canvas
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=NW)

        # Add other widgets over the background
        label_username = Label(self.root, text="Username:")
        label_username.place(x=80, y=50)  # Positioning the label
        self.entry_username = Entry(self.root)
        self.entry_username.place(x=150, y=50)  # Positioning the entry field

        label_password = Label(self.root, text="Password:")
        label_password.place(x=80, y=80)
        self.entry_password = Entry(self.root, show="*")
        self.entry_password.place(x=150, y=80)

        login_button = Button(self.root, text="Login", command=self.verify_login)
        login_button.place(x=120, y=120)

    def verify_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if both fields are filled
        if not username or not password:
            messagebox.showerror("Input Error", "Both username and password are required!")
            return

        # Access control based on username and password
        if username == "admin" and password == "admin123":
            self.open_admin_dashboard()
        elif username == "user" and password == "user123":
            self.open_user_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    def open_admin_dashboard(self):
        """Open the Admin Dashboard"""
        messagebox.showinfo("Login Successful", "Welcome, Admin!")
        self.root.withdraw()  # Hide the login window
        admin_window = Toplevel(self.root)
        AdminDashboard(admin_window)

    def open_user_dashboard(self):
        """Open the User Dashboard"""
        messagebox.showinfo("Login Successful", "Welcome, User!")
        self.root.withdraw()  # Hide the login window
        user_window = Toplevel(self.root)
        UserDashboard(user_window)


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect("leave_management.db")
        self.cursor = self.conn.cursor()

        # Admin dashboard widgets
        label = Label(self.root, text="Admin Dashboard", font=("Arial", 20))
        label.pack(pady=20)

        self.leave_table = Frame(self.root)
        self.leave_table.pack(pady=10)

        self.headers = ["ID", "User", "Leave Dates", "Status", "Actions"]
        for i, header in enumerate(self.headers):
            ttk.Label(self.leave_table, text=header).grid(row=0, column=i, padx=10, pady=5)

        self.refresh_leave_requests()

        logout_button = Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def refresh_leave_requests(self):
        """Populate leave requests table"""
        for widget in self.leave_table.winfo_children():
            widget.destroy()

        # Recreate headers
        for i, header in enumerate(self.headers):
            ttk.Label(self.leave_table, text=header).grid(row=0, column=i, padx=10, pady=5)

        # Fetch leave requests from the database
        self.cursor.execute("SELECT * FROM leave_requests")
        leave_requests = self.cursor.fetchall()

        # Display leave requests
        for idx, row in enumerate(leave_requests, 1):
            ttk.Label(self.leave_table, text=row[0]).grid(row=idx, column=0, padx=10, pady=5)
            ttk.Label(self.leave_table, text=row[1]).grid(row=idx, column=1, padx=10, pady=5)
            ttk.Label(self.leave_table, text=row[2]).grid(row=idx, column=2, padx=10, pady=5)
            ttk.Label(self.leave_table, text=row[3]).grid(row=idx, column=3, padx=10, pady=5)

            approve_button = Button(self.leave_table, text="Approve", command=lambda r=row: self.approve_leave(r))
            approve_button.grid(row=idx, column=4, padx=10, pady=5)

            reject_button = Button(self.leave_table, text="Reject", command=lambda r=row: self.reject_leave(r))
            reject_button.grid(row=idx, column=5, padx=10, pady=5)

    def approve_leave(self, row):
        self.cursor.execute("UPDATE leave_requests SET status = 'approved' WHERE id = ?", (row[0],))
        self.conn.commit()
        self.refresh_leave_requests()
        messagebox.showinfo("Leave Approved", f"Leave request for {row[1]} approved!")

    def reject_leave(self, row):
        self.cursor.execute("UPDATE leave_requests SET status = 'rejected' WHERE id = ?", (row[0],))
        self.conn.commit()
        self.refresh_leave_requests()
        messagebox.showinfo("Leave Rejected", f"Leave request for {row[1]} rejected!")

    def logout(self):
        self.root.quit()


class UserDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("User Dashboard")
        self.root.geometry("600x400")

        self.conn = sqlite3.connect("leave_management.db")
        self.cursor = self.conn.cursor()

        # User dashboard widgets
        label = Label(self.root, text="User Dashboard", font=("Arial", 20))
        label.pack(pady=20)

        self.leave_table = Frame(self.root)
        self.leave_table.pack(pady=10)

        self.headers = ["ID", "User", "Leave Dates", "Status", "Actions"]
        for i, header in enumerate(self.headers):
            ttk.Label(self.leave_table, text=header).grid(row=0, column=i, padx=10, pady=5)

        self.refresh_leave_requests()

        logout_button = Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(pady=20)

    def refresh_leave_requests(self):
        """Populate user leave requests table"""
        for widget in self.leave_table.winfo_children():
            widget.destroy()

        # Recreate headers
        for i, header in enumerate(self.headers):
            ttk.Label(self.leave_table, text=header).grid(row=0, column=i, padx=10, pady=5)

        # Fetch user leave requests from the database
        self.cursor.execute("SELECT * FROM leave_requests WHERE user_id = (SELECT id FROM users WHERE email = 'user@example.com')")
        leave_requests = self.cursor.fetchall()

        # Display leave requests
        for idx, row in enumerate(leave_requests, 1):
            ttk.Label(self.leave_table, text=row[0]).grid(row=idx, column=0, padx=10, pady=5)
            ttk.Label(self.leave_table, text=row[1]).grid(row=idx, column=1, padx=10, pady=5)
            ttk.Label(self.leave_table, text=row[2]).grid(row=idx, column=2, padx=10, pady=5)
            ttk.Label(self.leave_table, text=row[3]).grid(row=idx, column=3, padx=10, pady=5)

            cancel_button = Button(self.leave_table, text="Cancel", command=lambda r=row: self.cancel_leave(r))
            cancel_button.grid(row=idx, column=4, padx=10, pady=5)

    def cancel_leave(self, row):
        self.cursor.execute("DELETE FROM leave_requests WHERE id = ?", (row[0],))
        self.conn.commit()
        self.refresh_leave_requests()
        messagebox.showinfo("Leave Request Cancelled", f"Leave request for {row[1]} cancelled!")

    def logout(self):
        self.root.quit()


if __name__ == "__main__":
    root = Tk()
    obj = Login(root)
    root.mainloop()