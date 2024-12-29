import tkinter as tk
from math import sin, cos, tan, sqrt, pow, log10, log, factorial

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.config(bg="#ffffff")

        # Display Frame
        self.display = tk.Entry(self.root, font=("Arial", 24), bg="#ffffff", fg="#0d3562", bd="0", justify="right")
        self.display.pack(expand=True, fill="both")

        # History Frame (initially hidden)
        self.history_frame = tk.Frame(self.root, bg="#14539a", padx=10, pady=10)
        self.history_frame.pack_forget()  # Hide history initially

        # History Button
        self.history_button = tk.Button(self.root, text="History", font=("Arial", 18), bg="#14539a", fg="#fff8ff", command=self.toggle_history)
        self.history_button.pack(fill="x")

        # History List (stores the history of calculations)
        self.history_list = []

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg="#214a7a")
        self.buttons_frame.pack(expand=True, fill="both")

        # Buttons Layout
        self.create_buttons()

    def create_buttons(self):
        buttons = [
             ("sqrt", "x²", "log", "ln"),
            ("sin", "cos", "tan", "fact"),
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),