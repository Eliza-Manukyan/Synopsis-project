import sqlite3
import logging


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_logging()
        self.create_tables()
        self.populate_sample_data()

    def setup_logging(self):
        logging.basicConfig(filename="hostel.log", level=logging.ERROR,
                            format="%(asctime)s - %(levelname)s - %(message)s")

    def create_tables(self):
        # Create students table with additional fields
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                email TEXT NOT NULL,
                gender TEXT NOT NULL,
                faculty TEXT NOT NULL,
                course TEXT NOT NULL,
                room_number TEXT
            )
        """)
        # Create rooms table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS rooms (
                room_number TEXT PRIMARY KEY,
                capacity INTEGER NOT NULL,
                gender TEXT,
                occupants INTEGER DEFAULT 0
            )
        """)
        # Create requests table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                room_number TEXT NOT NULL,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (student_id) REFERENCES students (student_id),
                FOREIGN KEY (room_number) REFERENCES rooms (room_number)
            )
        """)
        self.conn.commit()

    def populate_sample_data(self):
        # Check if tables are empty
        self.cursor.execute("SELECT COUNT(*) FROM rooms")
        if self.cursor.fetchone()[0] > 0:
            return  # Data already exists, skip population

        # Add sample rooms
        sample_rooms = [
            ("101", 3, "Male"),
            ("102", 2, "Male"),
            ("103", 4, "Female"),
            ("104", 2, "Female"),
            ("105", 3, "Male")
        ]
        for room_number, capacity, gender in sample_rooms:
            self.add_room(room_number, capacity, gender)

        # Add sample students
        sample_students = [
            # Room 101 (Male, 2/3 occupied)
            ("S001", "John", "Doe", "john.doe@example.com", "Male", "Engineering", "CS101", "101"),
            ("S002", "Mike", "Smith", "mike.smith@example.com", "Male", "Engineering", "CS102", "101"),
            # Room 102 (Male, 1/2 occupied)
            ("S003", "Alex", "Brown", "alex.brown@example.com", "Male", "Physics", "PHY101", "102"),
            # Room 103 (Female, 3/4 occupied)
            ("S004", "Sarah", "Johnson", "sarah.j@example.com", "Female", "Biology", "BIO101", "103"),
            ("S005", "Emily", "Davis", "emily.davis@example.com", "Female", "Biology", "BIO102", "103"),
            ("S006", "Lisa", "Wilson", "lisa.wilson@example.com", "Female", "Chemistry", "CHEM101", "103"),
            # Room 104 (Female, 0/2 occupied) - empty
            # Room 105 (Male, 0/3 occupied) - empty
            # Unallocated student (Female)
            ("S007", "Anna", "Taylor", "anna.taylor@example.com", "Female", "Math", "MATH101", None)
        ]
        for student in sample_students:
            student_id, name, surname, email, gender, faculty, course, room_number = student
            self.add_student(student_id, name, surname, email, gender, faculty, course)
            if room_number:
                self.allocate_student(student_id, room_number)

    def add_student(self, student_id, name, surname, email, gender, faculty, course):
        try:
            self.cursor.execute("""
                INSERT INTO students (student_id, name, surname, email, gender, faculty, course)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (student_id, name, surname, email, gender, faculty, course))
            self.conn.commit()
            return True, None
        except sqlite3.IntegrityError as e:
            error_msg = f"Duplicate student ID: {student_id} ({str(e)})"
            logging.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Error adding student: {str(e)}"
            logging.error(error_msg)
            return False, error_msg

    def add_room(self, room_number, capacity, gender):
        try:
            self.cursor.execute("""
                INSERT INTO rooms (room_number, capacity, gender)
                VALUES (?, ?, ?)
            """, (room_number, capacity, gender))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error adding room: {e}")
            return False

    def delete_student(self, student_id):
        try:
            # Remove allocation if any
            self.remove_allocation(student_id)
            # Delete requests
            self.cursor.execute("DELETE FROM requests WHERE student_id = ?", (student_id,))
            # Delete student
            self.cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting student: {e}")
            return False

    def delete_room(self, room_number):
        try:
            # Remove allocations for this room
            self.cursor.execute("UPDATE students SET room_number = NULL WHERE room_number = ?", (room_number,))
            # Update requests
            self.cursor.execute("DELETE FROM requests WHERE room_number = ?", (room_number,))
            # Delete room
            self.cursor.execute("DELETE FROM rooms WHERE room_number = ?", (room_number,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error deleting room: {e}")
            return False

    def allocate_student(self, student_id, room_number):
        try:
            # Update student
            self.cursor.execute("""
                UPDATE students SET room_number = ? WHERE student_id = ?
            """, (room_number, student_id))
            # Update room occupants
            self.cursor.execute("""
                UPDATE rooms SET occupants = occupants + 1
                WHERE room_number = ?
            """, (room_number,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error allocating student: {e}")
            return False

    def remove_allocation(self, student_id):
        try:
            # Get room number
            self.cursor.execute("SELECT room_number FROM students WHERE student_id = ?", (student_id,))
            room_number = self.cursor.fetchone()
            room_number = room_number[0] if room_number else None
            # Update student
            self.cursor.execute("""
                UPDATE students SET room_number = NULL WHERE student_id = ?
            """, (student_id,))
            # Update room occupants
            if room_number:
                self.cursor.execute("""
                    UPDATE rooms SET occupants = occupants - 1
                    WHERE room_number = ?
                """, (room_number,))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error removing allocation: {e}")
            return False

    def add_request(self, student_id, room_number):
        try:
            self.cursor.execute("""
                INSERT INTO requests (student_id, room_number, status)
                VALUES (?, ?, 'Pending')
            """, (student_id, room_number))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error adding request: {e}")
            return False

    def update_request_status(self, request_id, status):
        try:
            self.cursor.execute("""
                UPDATE requests SET status = ? WHERE request_id = ?
            """, (status, request_id))
            self.conn.commit()
            return True
        except Exception as e:
            logging.error(f"Error updating request: {e}")
            return False

    def get_student(self, student_id):
        self.cursor.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        return self.cursor.fetchone()

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def get_rooms(self):
        self.cursor.execute("SELECT * FROM rooms")
        return self.cursor.fetchall()

    def get_available_rooms(self, gender):
        self.cursor.execute("""
            SELECT room_number, capacity, occupants
            FROM rooms
            WHERE gender = ? AND occupants < capacity
        """, (gender,))
        return self.cursor.fetchall()

    def get_requests(self):
        self.cursor.execute("SELECT * FROM requests")
        return self.cursor.fetchall()

    def get_student_requests(self, student_id):
        self.cursor.execute("SELECT * FROM requests WHERE student_id = ?", (student_id,))
        return self.cursor.fetchall()

    def export_to_csv(self):
        import csv
        try:
            with open("allocations.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(
                    ["Student ID", "Name", "Surname", "Email", "Gender", "Faculty", "Course", "Room Number"])
                self.cursor.execute("SELECT * FROM students")
                writer.writerows(self.cursor.fetchall())
            return True
        except Exception as e:
            logging.error(f"Error exporting to CSV: {e}")
            return False

    def __del__(self):
        self.conn.close()