import tkinter as tk
from tkinter import ttk, messagebox
from allocation import Allocator


class AdminApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.allocator = Allocator(db)
        self.root.title("Admin Hostel Management")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        self.on_logout = None  # Callback for logout

        # Top frame for logout
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=15, pady=5)
        ttk.Button(self.top_frame, text="Logout", command=self.logout).pack(side="right")

        # Sorting states
        self.student_sort_column = None
        self.student_sort_reverse = False
        self.room_sort_column = None
        self.room_sort_reverse = False
        self.request_sort_column = None
        self.request_sort_reverse = False

        # Notebook
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=15, padx=15, fill="both", expand=True)

        # Tabs
        self.student_frame = ttk.Frame(self.notebook)
        self.room_frame = ttk.Frame(self.notebook)
        self.allocation_frame = ttk.Frame(self.notebook)
        self.request_frame = ttk.Frame(self.notebook)
        self.report_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.student_frame, text="Manage Students")
        self.notebook.add(self.room_frame, text="Manage Rooms")
        self.notebook.add(self.allocation_frame, text="Allocate Rooms")
        self.notebook.add(self.request_frame, text="Room Requests")
        self.notebook.add(self.report_frame, text="Reports")

        self.setup_student_tab()
        self.setup_room_tab()
        self.setup_allocation_tab()
        self.setup_request_tab()
        self.setup_report_tab()

        # Treeview style
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Helvetica", 9))
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))

    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.root.destroy()
            if self.on_logout:
                self.on_logout()

    def setup_student_tab(self):
        input_frame = ttk.LabelFrame(self.student_frame, text="Manage Student", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = ttk.Entry(input_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        self.name_entry = ttk.Entry(input_frame)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Surname:").grid(row=2, column=0, padx=5, pady=5)
        self.surname_entry = ttk.Entry(input_frame)
        self.surname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.email_entry = ttk.Entry(input_frame)
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Gender:").grid(row=4, column=0, padx=5, pady=5)
        self.gender_combo = ttk.Combobox(input_frame, values=["Male", "Female"], state="readonly")
        self.gender_combo.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Faculty:").grid(row=5, column=0, padx=5, pady=5)
        self.faculty_entry = ttk.Entry(input_frame)
        self.faculty_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Course:").grid(row=6, column=0, padx=5, pady=5)
        self.course_entry = ttk.Entry(input_frame)
        self.course_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Student", command=self.add_student).grid(row=7, column=0, pady=10)
        ttk.Button(input_frame, text="Delete Selected Student", command=self.delete_student).grid(row=7, column=1,
                                                                                                  pady=10)

        self.student_tree = ttk.Treeview(self.student_frame, columns=(
        "ID", "Name", "Surname", "Email", "Gender", "Faculty", "Course", "Room"), show="headings")
        self.student_tree.heading("ID", text="Student ID", command=lambda: self.sort_students("ID"))
        self.student_tree.heading("Name", text="Name", command=lambda: self.sort_students("Name"))
        self.student_tree.heading("Surname", text="Surname", command=lambda: self.sort_students("Surname"))
        self.student_tree.heading("Email", text="Email", command=lambda: self.sort_students("Email"))
        self.student_tree.heading("Gender", text="Gender", command=lambda: self.sort_students("Gender"))
        self.student_tree.heading("Faculty", text="Faculty", command=lambda: self.sort_students("Faculty"))
        self.student_tree.heading("Course", text="Course", command=lambda: self.sort_students("Course"))
        self.student_tree.heading("Room", text="Room", command=lambda: self.sort_students("Room"))
        self.student_tree.column("ID", width=80)
        self.student_tree.column("Name", width=100)
        self.student_tree.column("Surname", width=100)
        self.student_tree.column("Email", width=150)
        self.student_tree.column("Gender", width=80)
        self.student_tree.column("Faculty", width=100)
        self.student_tree.column("Course", width=100)
        self.student_tree.column("Room", width=80)
        self.student_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.student_frame, orient="vertical", command=self.student_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.student_tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.student_frame, text="Refresh Students", command=self.refresh_students).grid(row=2, column=0,
                                                                                                    pady=5)

        self.student_frame.columnconfigure(0, weight=1)
        self.student_frame.rowconfigure(1, weight=1)
        self.refresh_students()

    def setup_room_tab(self):
        input_frame = ttk.LabelFrame(self.room_frame, text="Manage Room", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Room Number:").grid(row=0, column=0, padx=5, pady=5)
        self.room_number_entry = ttk.Entry(input_frame)
        self.room_number_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Capacity:").grid(row=1, column=0, padx=5, pady=5)
        self.capacity_entry = ttk.Entry(input_frame)
        self.capacity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=5)
        self.room_gender_combo = ttk.Combobox(input_frame, values=["Male", "Female"], state="readonly")
        self.room_gender_combo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Add Room", command=self.add_room).grid(row=3, column=0, pady=10)
        ttk.Button(input_frame, text="Delete Selected Room", command=self.delete_room).grid(row=3, column=1, pady=10)

        self.room_tree = ttk.Treeview(self.room_frame, columns=("Number", "Capacity", "Gender", "Occupants"),
                                      show="headings")
        self.room_tree.heading("Number", text="Room Number", command=lambda: self.sort_rooms("Number"))
        self.room_tree.heading("Capacity", text="Capacity", command=lambda: self.sort_rooms("Capacity"))
        self.room_tree.heading("Gender", text="Gender", command=lambda: self.sort_rooms("Gender"))
        self.room_tree.heading("Occupants", text="Occupants", command=lambda: self.sort_rooms("Occupants"))
        self.room_tree.column("Number", width=120)
        self.room_tree.column("Capacity", width=100)
        self.room_tree.column("Gender", width=80)
        self.room_tree.column("Occupants", width=100)
        self.room_tree.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.room_frame, orient="vertical", command=self.room_tree.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.room_tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.room_frame, text="Refresh Rooms", command=self.refresh_rooms).grid(row=2, column=0, pady=5)

        self.room_frame.columnconfigure(0, weight=1)
        self.room_frame.rowconfigure(1, weight=1)
        self.refresh_rooms()

    def setup_allocation_tab(self):
        input_frame = ttk.LabelFrame(self.allocation_frame, text="Room Allocation", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        self.alloc_student_id_entry = ttk.Entry(input_frame)
        self.alloc_student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Room Number:").grid(row=1, column=0, padx=5, pady=5)
        self.alloc_room_entry = ttk.Entry(input_frame)
        self.alloc_room_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Recommend Room", command=self.recommend_room).grid(row=2, column=0, columnspan=2,
                                                                                         pady=5)
        ttk.Button(input_frame, text="Allocate", command=self.allocate_room).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(input_frame, text="Remove Allocation", command=self.remove_allocation).grid(row=4, column=0,
                                                                                               columnspan=2, pady=5)

    def setup_request_tab(self):
        self.request_tree = ttk.Treeview(self.request_frame, columns=("ID", "Student ID", "Room", "Status"),
                                         show="headings")
        self.request_tree.heading("ID", text="Request ID", command=lambda: self.sort_requests("ID"))
        self.request_tree.heading("Student ID", text="Student ID", command=lambda: self.sort_requests("Student ID"))
        self.request_tree.heading("Room", text="Room Number", command=lambda: self.sort_requests("Room"))
        self.request_tree.heading("Status", text="Status", command=lambda: self.sort_requests("Status"))
        self.request_tree.column("ID", width=80)
        self.request_tree.column("Student ID", width=120)
        self.request_tree.column("Room", width=120)
        self.request_tree.column("Status", width=100)
        self.request_tree.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.request_frame, orient="vertical", command=self.request_tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.request_tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(self.request_frame, text="Approve Selected Request", command=self.approve_request).grid(row=1,
                                                                                                           column=0,
                                                                                                           pady=5)
        ttk.Button(self.request_frame, text="Deny Selected Request", command=self.deny_request).grid(row=2, column=0,
                                                                                                     pady=5)
        ttk.Button(self.request_frame, text="Refresh Requests", command=self.refresh_requests).grid(row=3, column=0,
                                                                                                    pady=5)

        self.request_frame.columnconfigure(0, weight=1)
        self.request_frame.rowconfigure(0, weight=1)
        self.refresh_requests()

    def setup_report_tab(self):
        report_frame = ttk.LabelFrame(self.report_frame, text="Reports", padding=10)
        report_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Button(report_frame, text="Export Allocations to CSV", command=self.export_csv).grid(row=0, column=0,
                                                                                                 pady=10)

        ttk.Label(report_frame, text="Room Status:", font=("Helvetica", 10, "bold")).grid(row=1, column=0, pady=5)
        self.status_text = tk.Text(report_frame, height=12, width=60, font=("Helvetica", 9))
        self.status_text.grid(row=2, column=0, padx=5, pady=5)

        ttk.Button(report_frame, text="Refresh Status", command=self.refresh_status).grid(row=3, column=0, pady=5)

        self.report_frame.columnconfigure(0, weight=1)
        self.report_frame.rowconfigure(2, weight=1)
        self.refresh_status()

    def sort_students(self, column):
        if self.student_sort_column == column:
            self.student_sort_reverse = not self.student_sort_reverse
        else:
            self.student_sort_column = column
            self.student_sort_reverse = False

        columns = {"ID": 0, "Name": 1, "Surname": 2, "Email": 3, "Gender": 4, "Faculty": 5, "Course": 6, "Room": 7}
        col_idx = columns[column]

        data = [(self.student_tree.item(item)["values"], item) for item in self.student_tree.get_children()]

        def sort_key(x):
            val = x[0][col_idx]
            # All columns are strings in the students table
            return (val is None, str(val) if val is not None else "")

        data.sort(key=sort_key, reverse=self.student_sort_reverse)

        for index, (_, item) in enumerate(data):
            self.student_tree.move(item, "", index)

    def sort_rooms(self, column):
        if self.room_sort_column == column:
            self.room_sort_reverse = not self.room_sort_reverse
        else:
            self.room_sort_column = column
            self.room_sort_reverse = False

        columns = {"Number": 0, "Capacity": 1, "Gender": 2, "Occupants": 3}
        col_idx = columns[column]

        data = [(self.room_tree.item(item)["values"], item) for item in self.room_tree.get_children()]

        def sort_key(x):
            val = x[0][col_idx]
            if col_idx in (1, 3):  # Capacity and Occupants are integers
                return (val is None, int(val) if val is not None else 0)
            return (val is None, str(val) if val is not None else "")

        data.sort(key=sort_key, reverse=self.student_sort_reverse)

        for index, (_, item) in enumerate(data):
            self.room_tree.move(item, "", index)

    def sort_requests(self, column):
        if self.request_sort_column == column:
            self.request_sort_reverse = not self.request_sort_reverse
        else:
            self.request_sort_column = column
            self.request_sort_reverse = False

        columns = {"ID": 0, "Student ID": 1, "Room": 2, "Status": 3}
        col_idx = columns[column]

        data = [(self.request_tree.item(item)["values"], item) for item in self.request_tree.get_children()]

        def sort_key(x):
            val = x[0][col_idx]
            if col_idx == 0:  # Request ID is an integer
                return (val is None, int(val) if val is not None else 0)
            return (val is None, str(val) if val is not None else "")

        data.sort(key=sort_key, reverse=self.request_sort_reverse)

        for index, (_, item) in enumerate(data):
            self.request_tree.move(item, "", index)

    def add_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        email = self.email_entry.get().strip()
        gender = self.gender_combo.get()
        faculty = self.faculty_entry.get().strip()
        course = self.course_entry.get().strip()

        if not all([student_id, name, surname, email, gender, faculty, course]):
            messagebox.showerror("Error", "All fields are required")
            return

        if self.db.add_student(student_id, name, surname, email, gender, faculty, course):
            messagebox.showinfo("Success", "Student added")
            self.clear_student_entries()
            self.refresh_students()
        else:
            messagebox.showerror("Error", "Failed to add student (duplicate ID or database error)")

    def delete_student(self):
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete")
            return

        student_id = self.student_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete student {student_id}?"):
            if self.db.delete_student(student_id):
                messagebox.showinfo("Success", "Student deleted")
                self.refresh_students()
                self.refresh_rooms()
                self.refresh_requests()
            else:
                messagebox.showerror("Error", "Failed to delete student")

    def add_room(self):
        room_number = self.room_number_entry.get().strip()
        capacity = self.capacity_entry.get().strip()
        gender = self.room_gender_combo.get()

        if not all([room_number, capacity, gender]):
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a positive integer")
            return

        if self.db.add_room(room_number, capacity, gender):
            messagebox.showinfo("Success", "Room added")
            self.clear_room_entries()
            self.refresh_rooms()
        else:
            messagebox.showerror("Error", "Failed to add room (duplicate number or database error)")

    def delete_room(self):
        selected = self.room_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a room to delete")
            return

        room_number = self.room_tree.item(selected[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete room {room_number}?"):
            if self.db.delete_room(room_number):
                messagebox.showinfo("Success", "Room deleted")
                self.refresh_rooms()
                self.refresh_students()
                self.refresh_requests()
            else:
                messagebox.showerror("Error", "Failed to delete room")

    def recommend_room(self):
        student_id = self.alloc_student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required")
            return

        room, message = self.allocator.recommend_room(student_id)
        if room:
            self.alloc_room_entry.delete(0, tk.END)
            self.alloc_room_entry.insert(0, room)
            messagebox.showinfo("Recommendation", f"Recommended room: {room}")
        else:
            messagebox.showerror("Error", message)

    def allocate_room(self):
        student_id = self.alloc_student_id_entry.get().strip()
        room_number = self.alloc_room_entry.get().strip()

        if not all([student_id, room_number]):
            messagebox.showerror("Error", "All fields are required")
            return

        success, message = self.allocator.allocate(student_id, room_number)
        if success:
            messagebox.showinfo("Success", message)
            self.clear_allocation_entries()
            self.refresh_students()
            self.refresh_rooms()
            self.refresh_requests()
        else:
            messagebox.showerror("Error", message)

    def remove_allocation(self):
        student_id = self.alloc_student_id_entry.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required")
            return

        if messagebox.askyesno("Confirm", "Remove allocation for this student?"):
            if self.db.remove_allocation(student_id):
                messagebox.showinfo("Success", "Allocation removed")
                self.clear_allocation_entries()
                self.refresh_students()
                self.refresh_rooms()
                self.refresh_requests()
            else:
                messagebox.showerror("Error", "Failed to remove allocation")

    def approve_request(self):
        selected = self.request_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a request")
            return

        request_id = self.request_tree.item(selected[0])["values"][0]
        student_id = self.request_tree.item(selected[0])["values"][1]
        room_number = self.request_tree.item(selected[0])["values"][2]

        if messagebox.askyesno("Confirm", f"Approve request for student {student_id} to room {room_number}?"):
            success, message = self.allocator.allocate(student_id, room_number)
            if success:
                self.db.update_request_status(request_id, "Approved")
                messagebox.showinfo("Success", "Request approved and room allocated")
                self.refresh_requests()
                self.refresh_students()
                self.refresh_rooms()
            else:
                messagebox.showerror("Error", message)

    def deny_request(self):
        selected = self.request_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a request")
            return

        request_id = self.request_tree.item(selected[0])["values"][0]
        student_id = self.request_tree.item(selected[0])["values"][1]
        room_number = self.request_tree.item(selected[0])["values"][2]

        if messagebox.askyesno("Confirm", f"Deny request for student {student_id} to room {room_number}?"):
            if self.db.update_request_status(request_id, "Denied"):
                messagebox.showinfo("Success", "Request denied")
                self.refresh_requests()
            else:
                messagebox.showerror("Error", "Failed to deny request")

    def refresh_students(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for student in self.db.get_students():
            self.student_tree.insert("", tk.END, values=student)
        for i, item in enumerate(self.student_tree.get_children()):
            self.student_tree.item(item, tags=("even" if i % 2 == 0 else "odd",))
        self.student_tree.tag_configure("even", background="#f0f0f0")
        self.student_tree.tag_configure("odd", background="#ffffff")

    def refresh_rooms(self):
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
        for room in self.db.get_rooms():
            self.room_tree.insert("", tk.END, values=room)
        for i, item in enumerate(self.room_tree.get_children()):
            self.room_tree.item(item, tags=("even" if i % 2 == 0 else "odd",))
        self.room_tree.tag_configure("even", background="#f0f0f0")
        self.room_tree.tag_configure("odd", background="#ffffff")

    def refresh_requests(self):
        for item in self.request_tree.get_children():
            self.request_tree.delete(item)
        for req in self.db.get_requests():
            self.request_tree.insert("", tk.END, values=req)
        for i, item in enumerate(self.request_tree.get_children()):
            self.request_tree.item(item, tags=("even" if i % 2 == 0 else "odd",))
        self.request_tree.tag_configure("even", background="#f0f0f0")
        self.request_tree.tag_configure("odd", background="#ffffff")

    def refresh_status(self):
        self.status_text.delete(1.0, tk.END)
        rooms = self.db.get_rooms()
        for room in rooms:
            number, capacity, gender, occupants = room
            status = f"Room {number}: {occupants}/{capacity} occupied, {gender}\n"
            self.status_text.insert(tk.END, status)

    def export_csv(self):
        if self.db.export_to_csv():
            messagebox.showinfo("Success", "Allocations exported to allocations.csv")
        else:
            messagebox.showerror("Error", "Failed to export allocations")

    def clear_student_entries(self):
        self.student_id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.gender_combo.set("")
        self.faculty_entry.delete(0, tk.END)
        self.course_entry.delete(0, tk.END)

    def clear_room_entries(self):
        self.room_number_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.room_gender_combo.set("")

    def clear_allocation_entries(self):
        self.alloc_student_id_entry.delete(0, tk.END)
        self.alloc_room_entry.delete(0, tk.END)