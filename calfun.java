
import java.util.*;

public class calfun {

    public static double add(double a, double b) {
        return a + b;
    }

    public static double  sub(double a, double b) {
        return a - b;
    }

    public static double mul(double a, double b) {
        return a * b;
    }

    public static double div(double a, double b) {
        return a / b;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.println("choose option \n 1> for normal cal \n 2> for scientific");
        int choice = sc.nextInt();

        // using rule switch case ->
        switch (choice) {
            case 1 -> {
                System.out.print(" enter the value of a= ");
                double a = sc.nextDouble();
                System.out.println("press /,*,-,+ for oprations");
              
                char choice1 = sc.next().charAt(0);
                System.out.print(" enter the value of b= ");
                double b = sc.nextDouble();
                // using rule switch case ->
                switch (choice1) {
                    case '+' ->
                        System.out.println("sum = " + add(a, b));

                    case '-' ->
                        System.out.println("sub = " + sub(a, b));

                    case '*' ->
                        System.out.println("mul = " + mul(a, b));

                    case '/' ->
                        System.out.println("div = " + div(a, b));

                    default ->
                        System.out.println(" option is invalid ");

                }
            }
            case 2 -> {

            }
            default ->
                System.out.println(" option is invalid ");

        }

    }

}
