import math

class ALU:
    def __init__(self):
        pass

    # Basic arithmetic operations
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b != 0:
            return (a / b)
        else:
            return "Error: Division by zero"

    def power(self, a, b):
        return math.pow(a, b)

    def square_root(self, a):
        return math.sqrt(a)

    def factorial(self, a):
        if a < 0:
            return "Error: Factorial of negative number"
        return math.factorial(int(a))

    def logarithm(self, a):
        if a <= 0:
            return "Error: Logarithm undefined for non-positive numbers"
        return math.log10(a)

    def natural_log(self, a):
        if a <= 0:
            return "Error: Natural logarithm undefined for non-positive numbers"
        return math.log(a)

    # Trigonometric functions (input in degrees)
    def sin(self, angle):
        return math.sin(math.radians(angle))

    def cos(self, angle):
        return math.cos(math.radians(angle))

    def tan(self, angle):
        try:
            return math.tan(math.radians(angle))
        except Exception as e:
            return f"Error: {e}"

    # Conversion for operations from the main program
    def convert_command(self, command):
        try:
            # Check for arithmetic operations and handle them
            if "plus" in command or "+" in command:
                return self._process_arithmetic(command, '+')
            elif "minus" in command or "-" in command:
                return self._process_arithmetic(command, '-')
            elif "times" in command or "x" in command or "*" in command:
                return self._process_arithmetic(command, '*')
            elif "divided by" in command or "/" in command:
                return self._process_arithmetic(command, '/')

            # Handle trigonometric and other functions
            elif '(' in command and ')' in command:
                function, args = self.extract_function_and_arguments(command)
                if function == "sin":
                    return self.sin(args[0])
                elif function == "cos":
                    return self.cos(args[0])
                elif function == "tan":
                    return self.tan(args[0])
                else:
                    return "Unknown function"

            elif "sqrt" in command:
                return self.square_root(*self._parse_arguments(command))
            elif "factorial" in command:
                return self.factorial(*self._parse_arguments(command))
            elif "logarithm" in command or "log" in command:
                return self.logarithm(*self._parse_arguments(command))
            elif "natural log" in command:
                return self.natural_log(*self._parse_arguments(command))

            else:
                return "Unknown command"
        except Exception as e:
            return f"Error: {e}"

    def _process_arithmetic(self, command, operator):
       # split and expand 
        parts = self._parse_arguments(command)

        if len(parts) == 2:
            a, b = parts
            if operator == '+':
                return self.add(a, b)
            elif operator == '-':
                return self.subtract(a, b)
            elif operator == '*':
                return self.multiply(a, b)
            elif operator == '/':
                return self.divide(a, b)
        else:
            return "Error: Invalid arithmetic expression"

    def _parse_arguments(self, command):
        
        parts = command.split()

        # Filter and convert -> float
        args = []
        for part in parts:
            try:
                args.append(float(part))
            except ValueError:
                continue  

        return args

    def extract_function_and_arguments(self, command):
        """
        'tan(45)' -> ('tan', [45])
        """
        # Find the function (sin, cos, tan) and the argument inside parentheses
        for func in ["sin", "cos", "tan"]:
            if func in command:
                start_index = command.index('(') + 1
                end_index = command.index(')')
                argument_str = command[start_index:end_index]
                argument = float(argument_str)  # Convert the argument -> float
                return func, [argument]

        return None, None
    