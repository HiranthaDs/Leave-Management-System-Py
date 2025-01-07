import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("1600x500")

        # Header
        label = Label(self.root, text="Admin Dashboard", font=("Arial", 20))
        label.pack(pady=20)

        # Treeview to display leave requests
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Email", "Job ID", "Phone", "Leave Dates", "Status"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Job ID", text="Job ID")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Leave Dates", text="Leave Dates")
        self.tree.heading("Status", text="Status")
        self.tree['show'] = 'headings'  # Hide the first empty column

        self.tree.pack(fill=BOTH, expand=True)

        # Fetch leave requests from the database
        self.load_leave_requests()

        # CRUD Buttons (Create, Read, Update, Delete)
        self.view_button = Button(self.root, text="Refresh Data", command=self.load_leave_requests)
        self.view_button.pack(pady=10)

        self.update_button = Button(self.root, text="Update Status", command=self.update_status)
        self.update_button.pack(pady=10)

        self.delete_button = Button(self.root, text="Delete Leave Request", command=self.delete_request)
        self.delete_button.pack(pady=10)

        # Logout Button
        self.logout_button = Button(self.root, text="Logout", command=self.logout)
        self.logout_button.pack(pady=10)

    def load_leave_requests(self):
        # Clear the existing data in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch leave requests from the database
        conn = sqlite3.connect("leave_management.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM leave_requests")
        rows = cursor.fetchall()
        conn.close()

        # Populate the Treeview with data
        for row in rows:
            self.tree.insert("", "end", values=row)

    def update_status(self):
        # Get the selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a leave request to update!")
            return

        leave_id = self.tree.item(selected_item, 'values')[0]  # Get the ID of the selected leave request

        # Ask the admin for the new status
        new_status = simpledialog.askstring("Update Status", "Enter new status (approved/rejected):")
        if not new_status:
            messagebox.showerror("Error", "Status cannot be empty!")
            return

        # Update the status in the database
        conn = sqlite3.connect("leave_management.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE leave_requests SET status = ? WHERE id = ?", (new_status, leave_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Leave request status updated!")
        self.load_leave_requests()  # Refresh the data

    def delete_request(self):
        # Get the selected item
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a leave request to delete!")
            return

        leave_id = self.tree.item(selected_item, 'values')[0]  # Get the ID of the selected leave request

        # Confirm deletion
        if messagebox.askyesno("Delete", "Are you sure you want to delete this leave request?"):
            # Delete from the database
            conn = sqlite3.connect("leave_management.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM leave_requests WHERE id = ?", (leave_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Leave request deleted!")
            self.load_leave_requests()  # Refresh the data

    def logout(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    admin_dashboard = AdminDashboard(root)
    root.mainloop()
