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
            ("1", "2", "3", "-"),
            ("C", "0", "=", "+"),
           
        ]

        for i, row in enumerate(buttons):
            for j, btn in enumerate(row):
                tk.Button(
                    self.buttons_frame,
                    text=btn,
                    font=("Arial", 18),
                    bg="#0d3562",
                    fg="#ffffff",
                    command=lambda btn=btn: self.on_button_click(btn),
                ).grid(row=i, column=j, sticky="nsew", padx=2, pady=2)

        # Configure grid layout
        for i in range(len(buttons)):
            self.buttons_frame.rowconfigure(i, weight=1)
        for j in range(len(buttons[0])):
            self.buttons_frame.columnconfigure(j, weight=1)

    def on_button_click(self, button):
        if button == "C":
            self.display.delete(0, tk.END)
        elif button == "=":
            try:
                expression = self.display.get()
                result = eval(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.add_to_history(str(result))  # Save the result to history
            except Exception as e:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif button in ["sqrt", "x²", "sin", "cos", "tan", "log", "ln", "fact"]:
            try:
                value = float(self.display.get())
                if button == "sqrt":
                    result = sqrt(value)
                elif button == "x²":
                    result = pow(value, 2)
                elif button == "sin":
                    result = sin(value)
                elif button == "cos":
                    result = cos(value)
                elif button == "tan":
                    result = tan(value)
                elif button == "log":
                    result = log10(value)
                elif button == "ln":
                    result = log(value)
                elif button == "fact":
                    result = factorial(int(self.display.get()))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.add_to_history(str(result))  # Save the result to history
            except ValueError:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, button)

    def add_to_history(self, result):
        # Add result to history list and display in history frame
        if result not in self.history_list:
            self.history_list.append(result)
            self.update_history_display()

    def update_history_display(self):
        # Clear previous history and re-add
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        for result in self.history_list:
            history_button = tk.Button(self.history_frame, text=result, font=("Arial", 16), bg="#3c3c3c", fg="#fff8ff", command=lambda res=result: self.on_history_click(res))
            history_button.pack(fill="x", pady=2)

    def toggle_history(self):
        # Toggle visibility of the history panel
        if self.history_frame.winfo_ismapped():
            self.history_frame.pack_forget()  # Hide history
        else:
            self.history_frame.pack(expand=True, fill="both")
            self.update_history_display()  # Update the history display when opened

    def on_history_click(self, result):
        # When a history entry is clicked, set the display to that result
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    Calculator(root)
    root.mainloop()
