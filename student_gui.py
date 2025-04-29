import tkinter as tk
from tkinter import ttk, messagebox
from allocation import Allocator


class StudentApp:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.allocator = Allocator(db)
        self.root.title("Student Hostel Portal")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.student_id = None
        self.on_logout = None  # Callback for logout

        # Top frame for logout
        self.top_frame = ttk.Frame(self.root)
        self.top_frame.pack(fill="x", padx=15, pady=5)
        ttk.Button(self.top_frame, text="Logout", command=self.logout).pack(side="right")

        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=15, padx=15, fill="both", expand=True)

        # Login/Registration
        self.login_frame = ttk.LabelFrame(self.main_frame, text="Student Login/Register", padding=10)
        self.login_frame.pack(fill="x", pady=10)

        ttk.Label(self.login_frame, text="Student ID:", font=("Helvetica", 10)).grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = ttk.Entry(self.login_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(row=1, column=0, pady=10)
        ttk.Button(self.login_frame, text="Register", command=self.show_register).grid(row=1, column=1, pady=10)

    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.root.destroy()
            if self.on_logout:
                self.on_logout()

    def show_register(self):
        # Registration window
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("400x500")

        frame = ttk.LabelFrame(register_window, text="Student Registration", padding=10)
        frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        student_id_entry = ttk.Entry(frame)
        student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = ttk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Surname:").grid(row=2, column=0, padx=5, pady=5)
        surname_entry = ttk.Entry(frame)
        surname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        email_entry = ttk.Entry(frame)
        email_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Gender:").grid(row=4, column=0, padx=5, pady=5)
        gender_combo = ttk.Combobox(frame, values=["Male", "Female"], state="readonly")
        gender_combo.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Faculty:").grid(row=5, column=0, padx=5, pady=5)
        faculty_entry = ttk.Entry(frame)
        faculty_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Course:").grid(row=6, column=0, padx=5, pady=5)
        course_entry = ttk.Entry(frame)
        course_entry.grid(row=6, column=1, padx=5, pady=5)

        def register():
            student_id = student_id_entry.get().strip()
            name = name_entry.get().strip()
            surname = surname_entry.get().strip()
            email = email_entry.get().strip()
            gender = gender_combo.get()
            faculty = faculty_entry.get().strip()
            course = course_entry.get().strip()

            if not all([student_id, name, surname, email, gender, faculty, course]):
                messagebox.showerror("Error", "All fields are required", parent=register_window)
                return

            # Check for duplicate student ID
            existing_student = self.db.get_student(student_id)
            if existing_student:
                messagebox.showerror("Error", f"Student ID '{student_id}' is already registered",
                                     parent=register_window)
                return

            success, error_msg = self.db.add_student(student_id, name, surname, email, gender, faculty, course)
            if success:
                messagebox.showinfo("Success", "Registration successful", parent=register_window)
                register_window.destroy()
            else:
                messagebox.showerror("Error", f"Registration failed: {error_msg}", parent=register_window)

        ttk.Button(frame, text="Submit", command=register).grid(row=7, column=0, columnspan=2, pady=10)

    def login(self):
        self.student_id = self.student_id_entry.get().strip()
        student = self.db.get_student(self.student_id)
        if not student:
            messagebox.showerror("Error", "Student ID not found")
            return

        # Clear login frame
        self.login_frame.destroy()

        # Profile frame
        self.profile_frame = ttk.LabelFrame(self.main_frame, text="Profile", padding=10)
        self.profile_frame.pack(fill="x", pady=10)

        student_data = student  # (student_id, name, surname, email, gender, faculty, course, room_number)
        ttk.Label(self.profile_frame, text=f"Name: {student_data[1]} {student_data[2]}", font=("Helvetica", 10)).grid(
            row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(self.profile_frame, text=f"Email: {student_data[3]}", font=("Helvetica", 10)).grid(row=1, column=0,
                                                                                                     sticky="w", padx=5,
                                                                                                     pady=2)
        ttk.Label(self.profile_frame, text=f"Gender: {student_data[4]}", font=("Helvetica", 10)).grid(row=2, column=0,
                                                                                                      sticky="w",
                                                                                                      padx=5, pady=2)
        ttk.Label(self.profile_frame, text=f"Faculty: {student_data[5]}", font=("Helvetica", 10)).grid(row=3, column=0,
                                                                                                       sticky="w",
                                                                                                       padx=5, pady=2)
        ttk.Label(self.profile_frame, text=f"Course: {student_data[6]}", font=("Helvetica", 10)).grid(row=4, column=0,
                                                                                                      sticky="w",
                                                                                                      padx=5, pady=2)
        ttk.Label(self.profile_frame, text=f"Room: {student_data[7] or 'Not allocated'}", font=("Helvetica", 10)).grid(
            row=5, column=0, sticky="w", padx=5, pady=2)

        # Room options
        self.room_frame = ttk.LabelFrame(self.main_frame, text="Room Options", padding=10)
        self.room_frame.pack(fill="x", pady=10)

        ttk.Button(self.room_frame, text="Request Room Suggestion", command=self.request_suggestion).grid(row=0,
                                                                                                          column=0,
                                                                                                          padx=5,
                                                                                                          pady=5)
        ttk.Button(self.room_frame, text="View Available Rooms", command=self.view_rooms).grid(row=0, column=1, padx=5,
                                                                                               pady=5)

        ttk.Label(self.room_frame, text="Request Specific Room:").grid(row=1, column=0, padx=5, pady=5)
        self.request_room_entry = ttk.Entry(self.room_frame)
        self.request_room_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.room_frame, text="Submit Request", command=self.submit_room_request).grid(row=1, column=2,
                                                                                                  padx=5, pady=5)

        # Requests status
        self.requests_frame = ttk.LabelFrame(self.main_frame, text="My Room Requests", padding=10)
        self.requests_frame.pack(fill="x", pady=10)

        self.requests_tree = ttk.Treeview(self.requests_frame, columns=("ID", "Room", "Status"), show="headings")
        self.requests_tree.heading("ID", text="Request ID")
        self.requests_tree.heading("Room", text="Room Number")
        self.requests_tree.heading("Status", text="Status")
        self.requests_tree.column("ID", width=80)
        self.requests_tree.column("Room", width=120)
        self.requests_tree.column("Status", width=100)
        self.requests_tree.pack(padx=5, pady=5, fill="x")

        ttk.Button(self.requests_frame, text="Refresh Requests", command=self.refresh_requests).pack(pady=5)

        self.refresh_requests()

    def request_suggestion(self):
        room, message = self.allocator.recommend_room(self.student_id)
        if room:
            messagebox.showinfo("Recommendation", f"Recommended room: {room}\nSubmit a request to reserve it.")
            self.request_room_entry.delete(0, tk.END)
            self.request_room_entry.insert(0, room)
        else:
            messagebox.showerror("Error", message)

    def view_rooms(self):
        student = self.db.get_student(self.student_id)
        gender = student[4]  # gender
        rooms = self.db.get_available_rooms(gender)

        rooms_window = tk.Toplevel(self.root)
        rooms_window.title("Available Rooms")
        rooms_window.geometry("400x300")

        tree = ttk.Treeview(rooms_window, columns=("Room", "Capacity", "Occupants"), show="headings")
        tree.heading("Room", text="Room Number")
        tree.heading("Capacity", text="Capacity")
        tree.heading("Occupants", text="Occupants")
        tree.column("Room", width=120)
        tree.column("Capacity", width=100)
        tree.column("Occupants", width=100)
        tree.pack(padx=10, pady=10, fill="both", expand=True)

        for room in rooms:
            tree.insert("", tk.END, values=room)

        def select_room():
            selected = tree.selection()
            if selected:
                room_number = tree.item(selected[0])["values"][0]
                self.request_room_entry.delete(0, tk.END)
                self.request_room_entry.insert(0, room_number)
                rooms_window.destroy()

        ttk.Button(rooms_window, text="Select Room", command=select_room).pack(pady=5)

    def submit_room_request(self):
        room_number = self.request_room_entry.get().strip()
        if not room_number:
            messagebox.showerror("Error", "Room number is required")
            return

        success, message = self.allocator.request_room(self.student_id, room_number)
        if success:
            messagebox.showinfo("Success", message)
            self.request_room_entry.delete(0, tk.END)
            self.refresh_requests()
        else:
            messagebox.showerror("Error", message)

    def refresh_requests(self):
        for item in self.requests_tree.get_children():
            self.requests_tree.delete(item)
        requests = self.db.get_student_requests(self.student_id)
        for req in requests:
            self.requests_tree.insert("", tk.END, values=(req[0], req[2], req[3]))