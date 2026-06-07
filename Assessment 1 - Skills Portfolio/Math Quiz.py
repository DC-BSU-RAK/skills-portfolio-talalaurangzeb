import tkinter as tk
from tkinter import messagebox
import random


class BrainTrainer:

    def __init__(self, root):

        # Main window setup
        self.root = root
        self.root.title("Brain Trainer")
        self.root.geometry("700x500")
        self.root.configure(bg="#1e1e2f")

        # Game state variables
        self.points = 0          # stores score
        self.question_count = 0  # tracks question number
        self.answer = 0          # correct answer for current question
        self.mode = ""          # difficulty mode (easy/medium/hard)

        # Show main menu first
        self.main_menu()

    # ---------------- MAIN MENU ---------------- #

    def main_menu(self):

        # Clear previous screen before loading menu
        self.clear_screen()

        # Title label
        title = tk.Label(
            self.root,
            text="BRAIN TRAINER",
            font=("Verdana", 28, "bold"),
            fg="#00ffd5",
            bg="#1e1e2f"
        )
        title.pack(pady=40)

        # Subtitle label
        subtitle = tk.Label(
            self.root,
            text="Sharpen your math skills",
            font=("Verdana", 12),
            fg="white",
            bg="#1e1e2f"
        )
        subtitle.pack(pady=5)

        # Container box for buttons
        menu_box = tk.Frame(
            self.root,
            bg="#2b2b40",
            padx=30,
            pady=30
        )
        menu_box.pack(pady=40)

        # EASY MODE button
        easy = tk.Button(
            menu_box,
            text="START EASY MODE",
            width=25,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#16a085",
            fg="white",
            relief="flat",
            command=lambda: self.start_game("easy")
        )
        easy.pack(pady=10)

        # MEDIUM MODE button
        medium = tk.Button(
            menu_box,
            text="START MEDIUM MODE",
            width=25,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#f39c12",
            fg="white",
            relief="flat",
            command=lambda: self.start_game("medium")
        )
        medium.pack(pady=10)

        # HARD MODE button
        hard = tk.Button(
            menu_box,
            text="START HARD MODE",
            width=25,
            height=2,
            font=("Arial", 11, "bold"),
            bg="#c0392b",
            fg="white",
            relief="flat",
            command=lambda: self.start_game("hard")
        )
        hard.pack(pady=10)

    # ---------------- START GAME ---------------- #

    def start_game(self, selected):

        # Set selected difficulty mode
        self.mode = selected

        # Reset score
        self.points = 0

        # Start from question 1
        self.question_count = 1

        # Load first question
        self.load_question()

    # ---------------- RANDOM NUMBER GENERATION ---------------- #

    def generate_values(self):

        # Easy mode: small numbers
        if self.mode == "easy":
            a = random.randint(1, 10)
            b = random.randint(1, 10)

        # Medium mode: medium range numbers
        elif self.mode == "medium":
            a = random.randint(20, 80)
            b = random.randint(20, 80)

        # Hard mode: large numbers
        else:
            a = random.randint(100, 999)
            b = random.randint(100, 999)

        return a, b

    # ---------------- LOAD QUESTION SCREEN ---------------- #

    def load_question(self):

        # If 10 questions are done, show final score screen
        if self.question_count > 10:
            self.show_score()
            return

        # Clear previous UI
        self.clear_screen()

        # Generate numbers for question
        num1, num2 = self.generate_values()

        # Randomly choose operator
        operator = random.choice(["+", "-"])

        # If subtraction, ensure no negative result
        if operator == "-":
            if num2 > num1:
                num1, num2 = num2, num1

            self.answer = num1 - num2

        else:
            self.answer = num1 + num2

        # ---------------- TOP BAR ---------------- #

        top_bar = tk.Frame(self.root, bg="#121220", height=60)
        top_bar.pack(fill="x")

        # Question counter display
        question_label = tk.Label(
            top_bar,
            text=f"Question {self.question_count}/10",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#121220"
        )
        question_label.place(x=20, y=18)

        # Score display
        score_label = tk.Label(
            top_bar,
            text=f"Points: {self.points}",
            font=("Arial", 12, "bold"),
            fg="#00ffd5",
            bg="#121220"
        )
        score_label.place(x=560, y=18)

        # ---------------- QUESTION CARD ---------------- #

        card = tk.Frame(
            self.root,
            bg="#2b2b40",
            width=500,
            height=260
        )
        card.pack(pady=60)

        # Prevent auto resizing
        card.pack_propagate(False)

        # Display math question
        math_text = tk.Label(
            card,
            text=f"{num1}  {operator}  {num2}",
            font=("Consolas", 34, "bold"),
            fg="#ffffff",
            bg="#2b2b40"
        )
        math_text.pack(pady=40)

        # Input box for user answer
        self.input_box = tk.Entry(
            card,
            font=("Arial", 20),
            justify="center",
            width=12,
            bg="#f4f4f4"
        )
        self.input_box.pack(pady=10)

        # Auto-focus input box
        self.input_box.focus()

        # Submit button
        submit = tk.Button(
            card,
            text="SUBMIT ANSWER",
            font=("Arial", 11, "bold"),
            bg="#00b894",
            fg="white",
            padx=15,
            pady=8,
            relief="flat",
            command=self.verify
        )
        submit.pack(pady=25)

        # Allow Enter key to submit answer
        self.input_box.bind("<Return>", lambda e: self.verify())

    # ---------------- ANSWER CHECK ---------------- #

    def verify(self):

        # Get user input
        value = self.input_box.get()

        try:
            value = int(value)

        except:
            # Handle invalid input
            messagebox.showwarning("Input Error", "Enter a valid number.")
            return

        # Check if answer is correct
        if value == self.answer:

            self.points += 10

            messagebox.showinfo(
                "Correct",
                "Nice! Your answer is correct."
            )

        else:

            messagebox.showerror(
                "Wrong",
                f"Wrong answer.\nCorrect answer was {self.answer}"
            )

        # Move to next question
        self.question_count += 1
        self.load_question()

    # ---------------- FINAL SCORE SCREEN ---------------- #

    def show_score(self):

        # Clear screen
        self.clear_screen()

        # Final container
        final_frame = tk.Frame(
            self.root,
            bg="#2b2b40",
            padx=50,
            pady=50
        )
        final_frame.pack(pady=80)

        # Game over title
        finish = tk.Label(
            final_frame,
            text="GAME OVER",
            font=("Verdana", 28, "bold"),
            fg="#00ffd5",
            bg="#2b2b40"
        )
        finish.pack(pady=20)

        # Final score display
        result = tk.Label(
            final_frame,
            text=f"Final Score: {self.points}/100",
            font=("Arial", 20),
            fg="white",
            bg="#2b2b40"
        )
        result.pack(pady=10)

        # Performance message based on score
        if self.points >= 80:
            text = "Excellent Performance"
        elif self.points >= 50:
            text = "Good Attempt"
        else:
            text = "Keep Practicing"

        comment = tk.Label(
            final_frame,
            text=text,
            font=("Arial", 14),
            fg="#dfe6e9",
            bg="#2b2b40"
        )
        comment.pack(pady=10)

        # Play again button
        again = tk.Button(
            final_frame,
            text="PLAY AGAIN",
            width=18,
            bg="#0984e3",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.main_menu
        )
        again.pack(pady=15)

        # Exit button
        exit_btn = tk.Button(
            final_frame,
            text="EXIT",
            width=18,
            bg="#d63031",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="flat",
            command=self.root.destroy
        )
        exit_btn.pack()

    # ---------------- UTILITY: CLEAR SCREEN ---------------- #

    def clear_screen(self):

        # Destroy all widgets before loading new screen
        for widget in self.root.winfo_children():
            widget.destroy()


# ---------------- RUN APPLICATION ---------------- #

root = tk.Tk()
game = BrainTrainer(root)
root.mainloop()