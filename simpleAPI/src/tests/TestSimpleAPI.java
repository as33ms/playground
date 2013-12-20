package tests;

import junit.framework.TestCase;
import api.SimpleAPI;

public class TestSimpleAPI extends TestCase {
	/**
	 * Test method for {@link api.SimpleAPI#add(int, int)}.
	 */
	public void testAdd() {
		int a = SimpleAPI.add(2, 3);
		assertTrue("Add API not working. Expected 5 but received: " + a, a == 5);
	}

	/**
	 * Test method for {@link api.SimpleAPI#subtract(int, int)}.
	 */
	public void testSubtract() {
		int a = SimpleAPI.subtract(2, 3);
		assertTrue("Subtract API not working. Expected -1 but received: " + a, a == -1);

		a = SimpleAPI.subtract(3, -4);
		assertTrue("Subtract API not working. Expected 7 but received: " + a, a == 7);

		a = SimpleAPI.subtract(5, 4);
		assertTrue("Subtract API not working. Expected 1 but received: " + a, a == 1);
	}

	/**
	 * Test method for {@link api.SimpleAPI#divide(int, int)}.
	 */
	public void testDivide() {
		int a = SimpleAPI.divide(44, 11);
		assertTrue("Subtract API not working. Expected 4 but received: " + a, a == 4);
	}

	/**
	 * Test method for {@link api.SimpleAPI#multiply(int, int)}.
	 */
	public void testMultiply() {
		int a = SimpleAPI.multiply(2, 3);
		assertTrue("Multiply API not working. Expected 6 but received: " + a, a == 6);
	}

	public void testFailure1() {
		assertTrue("A dummy test failure: 1", false);
	}

	public void testFailure2() {
		assertTrue("A dummy test failure: 2", false);
	}
}
