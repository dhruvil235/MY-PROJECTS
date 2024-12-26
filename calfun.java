import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;

public class calfun extends JFrame implements ActionListener {

    private JTextField inputField;
    private String operation = "";
    private double firstOperand = 0;

    public calfun() {
        setTitle("Advanced Calculator");
        setSize(400, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Create components
        inputField = new JTextField();
        inputField.setFont(new Font("Arial", Font.BOLD, 20));
        inputField.setHorizontalAlignment(JTextField.RIGHT);
        inputField.setEditable(false);

        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(5, 6, 6, 6));

        // Add buttons
        String[] buttons = {
                "7", "8", "9", "/", "√",
                "4", "5", "6", "*", "^",
                "1", "2", "3", "-", "sin",
                "0", ".", "=", "+", "cos",
                "tan", "C", "Exit"
        };

        for (String text : buttons) {
            JButton button = new JButton(text);
            button.setFont(new Font("Arial", Font.BOLD, 18));
            button.addActionListener(this);
            buttonPanel.add(button);
        }

        // Layout
        setLayout(new BorderLayout());
        add(inputField, BorderLayout.NORTH);
        add(buttonPanel, BorderLayout.CENTER);
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();

        try {
            if ("0123456789.".contains(command)) {
                // Append number or decimal point to input
                inputField.setText(inputField.getText() + command);
            } else if ("+-*/".contains(command)) {
                // Store the first operand and the operation
                if (!inputField.getText().isEmpty()) {
                    firstOperand = Double.parseDouble(inputField.getText());
                    operation = command;
                    inputField.setText("");
                }
            } else if (command.equals("^")) {
                // Handle exponentiation separately
                if (!inputField.getText().isEmpty()) {
                    firstOperand = Double.parseDouble(inputField.getText());
                    operation = "^";
                    inputField.setText("");
                }
            } else if (command.equals("=")) {
                // Perform the calculation based on the selected operation
                if (!inputField.getText().isEmpty() && !operation.isEmpty()) {
                    double secondOperand = Double.parseDouble(inputField.getText());
                    double result = switch (operation) {
                        case "+" -> add(firstOperand, secondOperand);
                        case "-" -> sub(firstOperand, secondOperand);
                        case "*" -> mul(firstOperand, secondOperand);
                        case "/" -> div(firstOperand, secondOperand);
                        case "^" -> power(firstOperand, secondOperand);
                        default -> 0;
                    };
                    inputField.setText(String.valueOf(result));
                    operation = ""; // Clear the operation after calculation
                }
            } else if (command.equals("√")) {
                // Perform square root
                if (!inputField.getText().isEmpty()) {
                    double value = Double.parseDouble(inputField.getText());
                    inputField.setText(String.valueOf(sqrt(value)));
                }
            } else if (command.equals("sin")) {
                // Perform sine calculation
                if (!inputField.getText().isEmpty()) {
                    double angle = Double.parseDouble(inputField.getText());
                    inputField.setText(String.valueOf(sin(angle)));
                }
            } else if (command.equals("cos")) {
                // Perform cosine calculation
                if (!inputField.getText().isEmpty()) {
                    double angle = Double.parseDouble(inputField.getText());
                    inputField.setText(String.valueOf(cos(angle)));
                }
            } else if (command.equals("tan")) {
                // Perform tangent calculation
                if (!inputField.getText().isEmpty()) {
                    double angle = Double.parseDouble(inputField.getText());
                    inputField.setText(String.valueOf(tan(angle)));
                }
            } else if (command.equals("C")) {
                // Clear the input and reset state
                inputField.setText("");
                firstOperand = 0;
                operation = "";
            } else if (command.equals("Exit")) {
                // Exit the application
                System.exit(0);
            }
        } catch (Exception ex) {
            // Handle errors gracefully
            inputField.setText("Error");
        }
    }

    // Helper methods for mathematical operations
    public static double add(double a, double b) {
        return a + b;
    }

    public static double sub(double a, double b) {
        return a - b;
    }

    public static double mul(double a, double b) {
        return a * b;
    }

    public static double div(double a, double b) {
        if (b == 0) {
            throw new ArithmeticException("Division by zero is not allowed.");
        }
        return a / b;
    }

    public static double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }

    public static double sqrt(double value) {
        if (value < 0) {
            throw new ArithmeticException("Square root of a negative number is not allowed.");
        }
        return Math.sqrt(value);
    }

    public static double sin(double angle) {
        return Math.sin(Math.toRadians(angle));
    }

    public static double cos(double angle) {
        return Math.cos(Math.toRadians(angle));
    }

    public static double tan(double angle) {
        return Math.tan(Math.toRadians(angle));
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            calfun calculator = new calfun();
            calculator.setVisible(true);
        });
    }
}
