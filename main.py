import tkinter as tk
from tkinter import ttk
from student_gui import StudentApp
from admin_gui import AdminApp
from database import Database


class ModeSelector:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel System - Select Mode")
        self.root.geometry("300x200")
        self.db = Database("hostel.db")

        # Mode selection
        ttk.Label(self.root, text="Select User Mode:", font=("Helvetica", 12, "bold")).pack(pady=20)
        ttk.Button(self.root, text="Student Mode", command=self.launch_student).pack(pady=10)
        ttk.Button(self.root, text="Admin Mode", command=self.launch_admin).pack(pady=10)

    def launch_student(self):
        self.root.destroy()
        root = tk.Tk()
        app = StudentApp(root, self.db)
        app.on_logout = self.restart  # Pass restart callback
        root.mainloop()

    def launch_admin(self):
        self.root.destroy()
        root = tk.Tk()
        app = AdminApp(root, self.db)
        app.on_logout = self.restart  # Pass restart callback
        root.mainloop()

    def restart(self):
        root = tk.Tk()
        app = ModeSelector(root)
        root.mainloop()


def main():
    root = tk.Tk()
    app = ModeSelector(root)
    root.mainloop()


if __name__ == "__main__":
    main()