"""
Calculator module with four basic operations and additional functionality for testing coverage.
"""

from typing import Optional


class Calculator:
    """
    A calculator class with four basic operations and additional utility methods.
    """

    def __init__(self) -> None:
        """
        Initialize the calculator.
        """
        self.history: list[str] = []
        self.last_result: Optional[float] = None
        self.error_count: int = 0

    def add(self, a: float, b: float) -> float:
        """Add two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Sum of a and b
        """
        result = a + b
        self._record_operation(f"{a} + {b} = {result}")
        self.last_result = result
        return result

    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Difference of a and b
        """
        result = a - b
        self._record_operation(f"{a} - {b} = {result}")
        self.last_result = result
        return result

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers.

        Args:
            a: First number
            b: Second number

        Returns:
            Product of a and b
        """
        result = a * b
        self._record_operation(f"{a} x {b} = {result}")
        self.last_result = result
        return result

    def divide(self, a: float, b: float) -> float:
        """Divide two numbers.

        Args:
            a: First number (dividend)
            b: Second number (divisor)

        Returns:
            Quotient of a and b

        Raises:
            ZeroDivisionError: If divisor is zero
        """
        if b == 0:
            self.error_count += 1
            raise ZeroDivisionError("Cannot divide by zero")

        result = a / b
        self._record_operation(f"{a} : {b} = {result}")
        self.last_result = result
        return result

    def power(self, a: float, b: float) -> float:
        """Calculate a raised to the power of b.

        Args:
            a: Base number
            b: Exponent

        Returns:
            a raised to the power of b
        """
        result: float = a**b
        self._record_operation(f"{a} ^ {b} = {result}")
        self.last_result = result
        return result

    def square_root(self, a: float) -> float:
        """Calculate the square root of a number.

        Args:
            a: Number to find square root of

        Returns:
            Square root of a

        Raises:
            ValueError: If a is negative
        """
        if a < 0:
            self.error_count += 1
            raise ValueError("Cannot calculate square root of negative number")

        result: float = a**0.5
        self._record_operation(f"√{a} = {result}")
        self.last_result = result
        return result

    def _record_operation(self, operation: str) -> None:
        """Record an operation in the history.

        Args:
            operation: String representation of the operation
        """
        self.history.append(operation)
        if len(self.history) > 100:  # Keep only last 100 operations
            self.history.pop(0)

    def get_history(self) -> list[str]:
        """Get the operation history.

        Returns:
            List of operation strings
        """
        return self.history.copy()

    def clear_history(self) -> None:
        """
        Clear the operation history.
        """
        self.history.clear()

    def get_last_result(self) -> Optional[float]:
        """Get the result of the last operation.

        Returns:
            Last operation result or None if no operations performed
        """
        return self.last_result

    def get_error_count(self) -> int:
        """Get the number of errors encountered.

        Returns:
            Number of errors
        """
        return self.error_count

    def reset(self) -> None:
        """
        Reset the calculator to initial state.
        """
        self.history.clear()
        self.last_result = None
        self.error_count = 0

    def is_positive(self, number: float) -> bool:
        """Check if a number is positive.

        Args:
            number: Number to check

        Returns:
            True if number is positive, False otherwise
        """
        return number > 0

    def is_negative(self, number: float) -> bool:
        """Check if a number is negative.

        Args:
            number: Number to check

        Returns:
            True if number is negative, False otherwise
        """
        return number < 0

    def is_zero(self, number: float) -> bool:
        """Check if a number is zero.

        Args:
            number: Number to check

        Returns:
            True if number is zero, False otherwise
        """
        return number == 0

    def absolute(self, number: float) -> float:
        """Get the absolute value of a number.

        Args:
            number: Number to get absolute value of

        Returns:
            Absolute value of the number
        """
        result = abs(number)
        self._record_operation(f"|{number}| = {result}")
        self.last_result = result
        return result


# Convenience functions for direct use
def add(a: float, b: float) -> float:
    """
    Add two numbers.
    """
    return Calculator().add(a, b)


def subtract(a: float, b: float) -> float:
    """
    Subtract two numbers.
    """
    return Calculator().subtract(a, b)


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    """
    return Calculator().multiply(a, b)


def divide(a: float, b: float) -> float:
    """
    Divide two numbers.
    """
    return Calculator().divide(a, b)
