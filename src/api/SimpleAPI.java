package api;

import java.util.Scanner;

public class SimpleAPI {

	public SimpleAPI() {
		// TODO Auto-generated constructor stub
	}

	public static void main(String[] args) {
	    System.out.println("Hello World!");

	    Scanner input = new Scanner(System.in);

	    System.out.println("1. Add | 2. Subtract | 3. Divide | 4.Multiply");
	    System.out.println("Dear lord, enter your option: ");
	    
	    int command = input.nextInt();

	    int a = 0, b = 0;

	    System.out.println("Enter First Number: ");
	    a = input.nextInt();

	    System.out.println("Enter Second Number: ");
	    b = input.nextInt();
	    
	    input.close();

	    switch (command){
	        case 1:
	        	System.out.println(a + " plus " + b + " equals " + add(a, b));
	        	break;
	        case 2:
	        	System.out.println(a + " minus " + b + " equals " + subtract(a, b));
	        	break;
	        case 3:
	        	System.out.println(a + " divided by " + b + " equals " + divide(a, b));
	        	break;
	        case 4:
	        	System.out.println(a + " times " + b + " equals " + multiply(a, b));
	        	break;
	        default:
	        	System.out.println("your input is invalid!");
	        	break;
	    }
	    
	    System.out.println("Good bye, Lord!");
	}

	public static int add(int first, int second) {
	        return first + second;
	}
	public static int subtract(int first, int second) {
	        return first - second;
	}
	public static int divide(int first, int second) {
	        return first / second;
	}
	public static int multiply(int first, int second) {
	        return first * second;
	}
}
