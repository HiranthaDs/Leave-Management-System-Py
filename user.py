import sqlite3
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar


class UserDashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("User Dashboard")
        self.root.geometry("600x700")

        self.user_id = user_id  # Store user_id passed from login

        # Add title
        self.title_label = Label(self.root, text="Leave Request Form", font=("Arial", 18))
        self.title_label.pack(pady=20)

        # Name
        self.name_label = Label(self.root, text="Full Name:")
        self.name_label.pack(pady=5)
        self.name_entry = Entry(self.root)
        self.name_entry.pack(pady=5)

        # Email
        self.email_label = Label(self.root, text="Email:")
        self.email_label.pack(pady=5)
        self.email_entry = Entry(self.root)
        self.email_entry.pack(pady=5)

        # Job ID
        self.job_id_label = Label(self.root, text="Job ID:")
        self.job_id_label.pack(pady=5)
        self.job_id_entry = Entry(self.root)
        self.job_id_entry.pack(pady=5)

        # Phone Number
        self.phone_label = Label(self.root, text="Phone Number:")
        self.phone_label.pack(pady=5)
        self.phone_entry = Entry(self.root)
        self.phone_entry.pack(pady=5)

        # Leave Date Picker
        self.leave_date_label = Label(self.root, text="Select Leave Date:")
        self.leave_date_label.pack(pady=5)
        self.leave_calendar = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.leave_calendar.pack(pady=5)

        # Submit Button
        self.submit_button = Button(self.root, text="Submit Leave Request", command=self.request_leave)
        self.submit_button.pack(pady=20)

    def request_leave(self):
        # Collect the form data
        name = self.name_entry.get()
        email = self.email_entry.get()
        job_id = self.job_id_entry.get()
        phone = self.phone_entry.get()
        leave_date = self.leave_calendar.get_date()  # Get the selected date

        # Validate the fields
        if not name or not email or not job_id or not phone or not leave_date:
            messagebox.showerror("Error", "Please fill all fields!")
            return

        # Connect to the database
        conn = sqlite3.connect('leave_management.db')

        # Enable foreign key constraints
        conn.execute('PRAGMA foreign_keys = ON;')  # This ensures foreign keys are enforced

        cursor = conn.cursor()

        try:
            # Insert the leave request into the database
            cursor.execute(
                "INSERT INTO leave_requests (user_id, name, email, job_id, phone_number, leave_dates, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.user_id, name, email, job_id, phone, leave_date, "pending"))
            conn.commit()
            messagebox.showinfo("Success", "Leave request submitted successfully!")
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Integrity error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error submitting leave request: {e}")
        finally:
            conn.close()

        # Optionally, clear the form fields after submission
        self.clear_form()

    def clear_form(self):
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.job_id_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.leave_calendar.selection_clear()  # Clear the calendar selection
