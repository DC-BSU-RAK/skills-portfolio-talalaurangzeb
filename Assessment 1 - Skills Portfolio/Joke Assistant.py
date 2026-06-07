import tkinter as tk
from tkinter import messagebox
import random


class SimpleJokesApp:
    def __init__(self, window):
        # Main window reference
        self.window = window

        # Set window title
        self.window.title("Daily Joke Box")

        # Set window size
        self.window.geometry("500x350")

        # Set background color
        self.window.config(bg="#1f1f1f")

        # Load jokes from file or fallback list
        self.jokes = self.get_jokes()

        # Stores the currently selected joke (question, answer)
        self.current = None

        # Build the UI
        self.create_ui()

    def get_jokes(self):
        """
        Loads jokes from a text file.
        If file is missing, uses default jokes.
        """
        jokes = []

        try:
            # Try opening external joke file
            with open("randomJokes.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()

                    # Each joke is assumed to have a '?' separating Q and A
                    if "?" in line:
                        question, answer = line.split("?", 1)

                        # Store as tuple: (question, answer)
                        jokes.append((question + "?", answer.strip()))

        except FileNotFoundError:
            # Backup jokes if file is not found
            jokes = [
                ("Why did the computer get cold?", "Because it left its Windows open."),
                ("Why can't your nose be 12 inches long?", "Because then it would be a foot."),
                ("What do you call cheese that is not yours?", "Nacho cheese.")
            ]

        return jokes

    def create_ui(self):
        """
        Builds all UI components (labels, buttons, layout)
        """

        # App title label
        title = tk.Label(
            self.window,
            text="😂 Daily Joke Box",
            font=("Arial", 22, "bold"),
            bg="#1f1f1f",
            fg="white"
        )
        title.pack(pady=15)

        # Label that displays joke/question/answer
        self.joke_text = tk.Label(
            self.window,
            text="Press the button to get a joke",
            font=("Arial", 14),
            wraplength=420,     # Wrap text within width
            justify="center",   # Center align text
            bg="#2b2b2b",
            fg="white",
            width=40,
            height=6
        )
        self.joke_text.pack(pady=20)

        # Frame to hold buttons in one row
        buttons = tk.Frame(self.window, bg="#1f1f1f")
        buttons.pack()

        # Button to generate a new joke
        self.joke_btn = tk.Button(
            buttons,
            text="New Joke",
            font=("Arial", 11, "bold"),
            bg="#4caf50",
            fg="white",
            padx=15,
            command=self.show_joke  # Calls function when clicked
        )
        self.joke_btn.grid(row=0, column=0, padx=10)

        # Button to reveal answer (disabled initially)
        self.answer_btn = tk.Button(
            buttons,
            text="Reveal",
            font=("Arial", 11, "bold"),
            bg="#ff9800",
            fg="white",
            padx=15,
            state="disabled",       # Disabled until joke is shown
            command=self.show_answer
        )
        self.answer_btn.grid(row=0, column=1, padx=10)

        # Exit button
        exit_btn = tk.Button(
            buttons,
            text="Exit",
            font=("Arial", 11, "bold"),
            bg="#f44336",
            fg="white",
            padx=15,
            command=self.close_app
        )
        exit_btn.grid(row=0, column=2, padx=10)

    def show_joke(self):
        """
        Selects a random joke and displays the question part
        """

        # Pick random joke from list
        self.current = random.choice(self.jokes)

        # Show only the question part
        self.joke_text.config(
            text=self.current[0]
        )

        # Enable reveal button once joke is shown
        self.answer_btn.config(state="normal")

    def show_answer(self):
        """
        Displays the answer for the current joke
        """

        if self.current:
            self.joke_text.config(
                text=f"{self.current[0]}\n\n👉 {self.current[1]}"
            )

            # Disable button after revealing answer
            self.answer_btn.config(state="disabled")

    def close_app(self):
        """
        Asks user confirmation before closing the app
        """

        ask = messagebox.askyesno(
            "Exit",
            "Do you want to close the app?"
        )

        # Close window if user selects Yes
        if ask:
            self.window.destroy()


# Run the application
if __name__ == "__main__":
    root = tk.Tk()                  # Create main window
    app = SimpleJokesApp(root)      # Start app
    root.mainloop()                 # Keep window running