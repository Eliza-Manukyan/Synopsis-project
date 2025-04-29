class Allocator:
    def __init__(self, db):
        self.db = db

    def recommend_room(self, student_id):
        # Get student details
        self.db.cursor.execute("SELECT gender, faculty FROM students WHERE student_id = ?", (student_id,))
        student = self.db.cursor.fetchone()
        if not student:
            return None, "Student not found"

        gender, faculty = student
        # Get available rooms
        available_rooms = self.db.get_available_rooms(gender)
        if not available_rooms:
            return None, "No available rooms for this gender"

        # Rule-based AI: Prioritize rooms with same-faculty students
        best_room = None
        best_score = -1
        for room in available_rooms:
            room_number, capacity, occupants = room
            score = 0
            # Check if room has students from same faculty
            self.db.cursor.execute("""
                SELECT COUNT(*) FROM students
                WHERE room_number = ? AND faculty = ?
            """, (room_number, faculty))
            same_faculty_count = self.db.cursor.fetchone()[0]
            score += same_faculty_count * 10  # Weight for faculty compatibility
            score += (capacity - occupants)  # Prefer less occupied rooms
            if score > best_score:
                best_score = score
                best_room = room_number

        return best_room, "Recommendation successful"

    def allocate(self, student_id, room_number):
        # Validate allocation
        self.db.cursor.execute("SELECT gender FROM students WHERE student_id = ?", (student_id,))
        student = self.db.cursor.fetchone()
        if not student:
            return False, "Student not found"
        student_gender = student[0]
        self.db.cursor.execute("SELECT gender, capacity, occupants FROM rooms WHERE room_number = ?", (room_number,))
        room = self.db.cursor.fetchone()
        if not room:
            return False, "Room not found"
        room_gender, capacity, occupants = room
        if room_gender != student_gender:
            return False, "Gender mismatch"
        if occupants >= capacity:
            return False, "Room is full"

        # Perform allocation
        success = self.db.allocate_student(student_id, room_number)
        if success:
            return True, "Allocation successful"
        return False, "Allocation failed"

    def request_room(self, student_id, room_number):
        # Validate request
        self.db.cursor.execute("SELECT gender, room_number FROM students WHERE student_id = ?", (student_id,))
        student = self.db.cursor.fetchone()
        if not student:
            return False, "Student not found"
        student_gender, current_room = student
        if current_room:
            return False, "Student already allocated to a room"
        self.db.cursor.execute("SELECT gender, capacity, occupants FROM rooms WHERE room_number = ?", (room_number,))
        room = self.db.cursor.fetchone()
        if not room:
            return False, "Room not found"
        room_gender, capacity, occupants = room
        if room_gender != student_gender:
            return False, "Gender mismatch"
        if occupants >= capacity:
            return False, "Room is full"

        # Add request
        success = self.db.add_request(student_id, room_number)
        if success:
            return True, "Room request submitted"
        return False, "Request failed"