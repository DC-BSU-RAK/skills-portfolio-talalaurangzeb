import tkinter as tk
from tkinter import ttk, messagebox


# Class used to store student information
class Student:
    
    # Constructor to initialize student details
    def __init__(self, sid, name, cw1, cw2, cw3, exam):
        self.sid = sid
        self.name = name
        self.cw1 = cw1
        self.cw2 = cw2
        self.cw3 = cw3
        self.exam = exam

    # Function to calculate coursework total
    def total_coursework(self):
        return self.cw1 + self.cw2 + self.cw3

    # Function to calculate overall total
    def final_total(self):
        return self.total_coursework() + self.exam

    # Function to calculate percentage
    def percentage(self):
        return round((self.final_total() / 160) * 100, 1)

    # Function to determine grade
    def grade(self):
        score = self.percentage()

        if score >= 70:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 40:
            return "D"
        return "F"


# Main application class
class GradeTracker:

    # Constructor for the application
    def __init__(self, root):

        # Main window setup
        self.root = root
        self.root.title("Grade Tracker")
        self.root.geometry("850x500")
        self.root.config(bg="#f4f4f4")

        # List to store all student objects
        self.students = []

        # Text file used for saving records
        self.filename = "studentMarks.txt"

        # Load data from file
        self.load_file()

        # Create GUI layout
        self.make_layout()

        # Show records in table
        self.display_students()

    # Function to read student data from file
    def load_file(self):

        try:
            with open(self.filename, "r") as file:

                # Read all lines from file
                lines = file.readlines()

                # Skip first line because it stores number of students
                for line in lines[1:]:

                    # Split values using commas
                    parts = line.strip().split(",")

                    # Check if line has valid data
                    if len(parts) == 6:

                        # Create student object
                        student = Student(
                            int(parts[0]),
                            parts[1],
                            int(parts[2]),
                            int(parts[3]),
                            int(parts[4]),
                            int(parts[5])
                        )

                        # Add student to list
                        self.students.append(student)

        # If file is missing
        except FileNotFoundError:
            messagebox.showwarning(
                "Missing File",
                "studentMarks.txt was not found"
            )

    # Function to save records back into file
    def save_file(self):

        with open(self.filename, "w") as file:

            # First line stores total student count
            file.write(str(len(self.students)) + "\n")

            # Save each student's data
            for s in self.students:

                row = f"{s.sid},{s.name},{s.cw1},{s.cw2},{s.cw3},{s.exam}\n"

                file.write(row)

    # Function to create GUI layout
    def make_layout(self):

        # Title label
        heading = tk.Label(
            self.root,
            text="Student Grade Tracker",
            font=("Arial", 20, "bold"),
            bg="#f4f4f4"
        )
        heading.pack(pady=10)

        # Frame for buttons
        btn_frame = tk.Frame(self.root, bg="#f4f4f4")
        btn_frame.pack(pady=5)

        # Button to display all students
        tk.Button(
            btn_frame,
            text="Show All",
            width=12,
            command=self.display_students
        ).grid(row=0, column=0, padx=5)

        # Button to add new student
        tk.Button(
            btn_frame,
            text="Add Student",
            width=12,
            command=self.add_student_window
        ).grid(row=0, column=1, padx=5)

        # Button to delete selected student
        tk.Button(
            btn_frame,
            text="Delete",
            width=12,
            command=self.delete_student
        ).grid(row=0, column=2, padx=5)

        # Button to show top student
        tk.Button(
            btn_frame,
            text="Top Student",
            width=12,
            command=self.best_student
        ).grid(row=0, column=3, padx=5)

        # Table column names
        columns = (
            "ID",
            "Name",
            "Coursework",
            "Exam",
            "Percent",
            "Grade"
        )

        # Create Treeview table
        self.table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=15
        )

        # Add headings and widths
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=120)

        # Display table
        self.table.pack(fill="both", expand=True, padx=20, pady=15)

        # Bottom status label
        self.info = tk.Label(
            self.root,
            text="Loaded student records",
            bg="#f4f4f4",
            font=("Arial", 10)
        )

        self.info.pack(pady=5)

    # Function to clear table contents
    def clear_table(self):

        for item in self.table.get_children():
            self.table.delete(item)

    # Function to display students in table
    def display_students(self):

        # Clear previous data
        self.clear_table()

        # Insert each student into table
        for s in self.students:

            self.table.insert(
                "",
                "end",
                values=(
                    s.sid,
                    s.name,
                    s.total_coursework(),
                    s.exam,
                    f"{s.percentage()}%",
                    s.grade()
                )
            )

        # Update status label
        self.info.config(
            text=f"Total Students: {len(self.students)}"
        )

    # Function to open add student window
    def add_student_window(self):

        # Create new popup window
        win = tk.Toplevel(self.root)
        win.title("Add Student")
        win.geometry("300x350")

        # Labels for fields
        labels = [
            "Student ID",
            "Full Name",
            "CW1",
            "CW2",
            "CW3",
            "Exam"
        ]

        entries = []

        # Create labels and entry boxes
        for text in labels:

            tk.Label(win, text=text).pack(pady=3)

            entry = tk.Entry(win)
            entry.pack(pady=3)

            entries.append(entry)

        # Function to save student data
        def save_student():

            try:

                # Create new student object
                student = Student(
                    int(entries[0].get()),
                    entries[1].get(),
                    int(entries[2].get()),
                    int(entries[3].get()),
                    int(entries[4].get()),
                    int(entries[5].get())
                )

                # Add to student list
                self.students.append(student)

                # Save updated records
                self.save_file()

                # Refresh table
                self.display_students()

                # Success message
                messagebox.showinfo(
                    "Saved",
                    "Student added successfully"
                )

                # Close popup
                win.destroy()

            except:

                # Error if invalid input
                messagebox.showerror(
                    "Error",
                    "Please enter valid details"
                )

        # Save button
        tk.Button(
            win,
            text="Save Student",
            command=save_student
        ).pack(pady=15)

    # Function to delete selected student
    def delete_student(self):

        # Get selected row
        selected = self.table.selection()

        # Check if nothing selected
        if not selected:

            messagebox.showwarning(
                "Select",
                "Please select a student"
            )
            return

        # Get selected student's ID
        values = self.table.item(selected[0])["values"]
        sid = values[0]

        # Find and remove student
        for s in self.students:

            if s.sid == sid:
                self.students.remove(s)
                break

        # Save changes
        self.save_file()

        # Refresh display
        self.display_students()

        # Success message
        messagebox.showinfo(
            "Deleted",
            "Student record removed"
        )

    # Function to show highest scoring student
    def best_student(self):

        # Stop if list is empty
        if not self.students:
            return

        # Find student with highest percentage
        top = max(
            self.students,
            key=lambda x: x.percentage()
        )

        # Show result message
        messagebox.showinfo(
            "Top Student",
            f"{top.name}\n"
            f"Percentage: {top.percentage()}%\n"
            f"Grade: {top.grade()}"
        )


# Main program execution starts here
if __name__ == "__main__":

    # Create main tkinter window
    root = tk.Tk()

    # Create application object
    app = GradeTracker(root)

    # Run the GUI
    root.mainloop()