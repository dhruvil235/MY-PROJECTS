import tkinter as tk
import threading
import speech_recognition as sr
import math
from alu import ALU  

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice-Activated Calculator by dhruvil_dave")
        self.root.geometry("450x650")
        self.root.resizable(False, False)
        self.root.config(bg="#ffffff")

        self.language = "en"  
        self.languages = {"en": "English", "gu": "Gujarati", "hi": "Hindi"}

        # Create an instance of alu by dhruvil_dave
        self.alu = ALU()

        # Display Frame
        self.display = tk.Entry(self.root, font=("Arial", 24), bg="#ffffff", fg="#0d3562", bd="0", justify="right")
        self.display.pack(expand=True, fill="both")

        # Language selection buttons
        self.language_buttons_frame = tk.Frame(self.root)
        self.language_buttons_frame.pack(fill="x", pady=10)

        self.lang_en_button = tk.Button(self.language_buttons_frame, text="English", command=lambda: self.change_language("en"))
        self.lang_en_button.pack(side="left", fill="x", expand=True)

        self.lang_gu_button = tk.Button(self.language_buttons_frame, text="ગુજરાતી", command=lambda: self.change_language("gu"))
        self.lang_gu_button.pack(side="left", fill="x", expand=True)

        self.lang_hi_button = tk.Button(self.language_buttons_frame, text="हिंदी", command=lambda: self.change_language("hi"))
        self.lang_hi_button.pack(side="left", fill="x", expand=True)

        # History Frame (initially hidden)
        self.history_frame = tk.Frame(self.root, bg="#14539a", padx=10, pady=10)
        self.history_frame.pack_forget()  # Hide history initially

        # History Button
        self.history_button = tk.Button(self.root, text=self.get_text("History"), font=("Arial", 18), bg="#14539a", fg="#fff8ff", command=self.toggle_history)
        self.history_button.pack(fill="x")

        # Voice Input Button
        self.voice_button = tk.Button(self.root, text=self.get_text("🎙 Voice Input"), font=("Arial", 18), bg="#28a745", fg="#fff8ff", command=self.start_voice_input)
        self.voice_button.pack(fill="x")

        # History List (stores the history of calculations)
        self.history_list = []

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root, bg="#214a7a")
        self.buttons_frame.pack(expand=True, fill="both")

        # Buttons Layout
        self.create_buttons()

    def get_text(self, key):
        # Return the corresponding text based on the current language
        translations = {
            "History": {"en": "History", "gu": "ઇતિહાસ", "hi": "इतिहास"},
            "🎙 Voice Input": {"en": "🎙 Voice Input", "gu": "🎙 અવાજ દાખિલ કરે", "hi": "🎙 आवाज दाखिल करे"},
        }
        return translations.get(key, {}).get(self.language, key)

    def change_language(self, lang_code):
        self.language = lang_code
        self.history_button.config(text=self.get_text("History"))
        self.voice_button.config(text=self.get_text("🎙 Voice Input"))
        self.create_buttons()  

    def create_buttons(self):
        buttons = [
            (self.get_text("sqrt"), self.get_text("x²"), self.get_text("log"), self.get_text("ln")),
            (self.get_text("sin"), self.get_text("cos"), self.get_text("tan"), self.get_text("fact")),
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
                # Directly evaluate the expression
                result = self.evaluate_expression(expression)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
                self.add_to_history(f"{expression} = {result}")  # Save the expression and result to history
            except Exception:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, current + button)


    def evaluate_expression(self, expression):
        try:
            # Evaluate the expression directly and handle exceptions
            result = eval(expression)
            return result
        except Exception as e:
            # If the expression is invalid -> error
            return "Error"


    def add_to_history(self, entry):
        if entry not in self.history_list:
            self.history_list.append(entry)
            self.update_history_display()

    def update_history_display(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        for entry in self.history_list:
            history_button = tk.Button(self.history_frame, text=entry, font=("Arial", 16), bg="#3c3c3c", fg="#fff8ff", command=lambda res=entry: self.on_history_click(res))
            history_button.pack(fill="x", pady=2)

    def toggle_history(self):
        if self.history_frame.winfo_ismapped():
            self.history_frame.pack_forget()  # Hide history
        else:
            self.history_frame.pack(expand=True, fill="both")
            self.update_history_display()  # Update the history display when opened

    def on_history_click(self, result):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, result)

    def start_voice_input(self):
        # Start a thread for voice input to avoid blocking the GUI
        threading.Thread(target=self.voice_input, daemon=True).start()

    def voice_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Listening...")
            try:
                # Listen to the user's speech and convert it to text
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                command = recognizer.recognize_google(audio).lower()  # Convert to lowercase
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, command)

                # Normalize the voice command
                command = self.normalize_command(command)

                # Debugging: print the normalized command
                print(f"Normalized Command: {command}")

                try:
                    result = self.alu.convert_command(command)  # Use ALU to calculate the result

                    # Debugging: print the result
                    print(f"Result: {result}")

                    # Display the result in the GUI
                    self.display.insert(tk.END, f" = {result}")
                    self.add_to_history(f"{command} = {result}")
                except Exception as e:
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, "Error")
                    print(f"Error evaluating command: {e}")
            except sr.UnknownValueError:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Could not understand")
            except sr.RequestError:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Service error")

    def normalize_command(self, command):
        if self.language == "gu":
            command = self.normalize_gujarati(command)
        elif self.language == "hi":
            command = self.normalize_hindi(command)
        else:
            command = self.normalize_english(command)

        # Handle trigonometric and logarithmic functions
        command = self.convert_function_format(command)

        # Remove extra spaces
        command = " ".join(command.split())

        return command

    def normalize_english(self, command):
        command = command.replace("times", "*")
        command = command.replace("x", "*")
        command = command.replace("divid by", "/")
        command = command.replace("plus", "+")
        command = command.replace("minus", "-")
        command = command.replace("sine", "sin")
        command = command.replace("cosine", "cos")
        command = command.replace("tangent", "tan")
        command = command.replace("logarithm", "log")
        command = command.replace("natural log", "ln")
        return command

    def normalize_gujarati(self, command):
        command = command.replace("સમણો", "*")
        command = command.replace("x", "*")
        command = command.replace("વાડું", "/")
        command = command.replace("પ્લસ", "+")
        command = command.replace("માઇનસ", "-")
        command = command.replace("સાઇન", "sin")
        command = command.replace("કોસાઇન", "cos")
        command = command.replace("ટાંજન્ટ", "tan")
        command = command.replace("લોગ", "log")
        command = command.replace("પ્રાકૃતિક લોગ", "ln")
        return command

    def normalize_hindi(self, command):
        command = command.replace("गुणा", "*")
        command = command.replace("x", "*")
        command = command.replace("बाँट", "/")
        command = command.replace("जोड़", "+")
        command = command.replace("घटाना", "-")
        command = command.replace("साइन", "sin")
        command = command.replace("कोसाइन", "cos")
        command = command.replace("टैन्जेंट", "tan")
        command = command.replace("लॉग", "log")
        command = command.replace("प्राकृतिक लॉग", "ln")
        return command

    def convert_function_format(self, command):
            # Check if a function like sin, cos, tan, log, ln is followed by a number
            functions = ["sin", "cos", "tan", "log", "ln"]
            for func in functions:
                
                if func in command:
                    
                    start = command.find(func) + len(func)

                    # Check if the character after the function is numeric or space
                    if start < len(command):
                        if command[start].isdigit():  
                            # Create the proper format with parentheses
                            command = command[:start] + "(" + command[start:] + ")"
                        elif command[start] == ' ' and start + 1 < len(command) and command[start + 1].isdigit():
                            # If there is a space 
                            command = command[:start + 1] + "(" + command[start + 1:] + ")"
            
            return command



    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()  # Create the Tkinter window
    calc = Calculator(root)  # Initialize the Calculator class with the root window
    calc.run()  # Run the Tkinter main loop
