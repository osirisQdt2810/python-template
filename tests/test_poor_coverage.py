"""
Poor coverage test suite for the calculator module.
This file only tests basic functionality and will result in low coverage.
"""

from my_package.calculator import Calculator


class TestBasicCalculatorOperations:
    """Test only the most basic calculator operations."""

    def test_simple_addition(self):
        """Test simple addition."""
        calc = Calculator()
        assert calc.add(2, 3) == 5

    def test_simple_subtraction(self):
        """Test simple subtraction."""
        calc = Calculator()
        assert calc.subtract(5, 3) == 2

    def test_simple_multiplication(self):
        """Test simple multiplication."""
        calc = Calculator()
        assert calc.multiply(2, 3) == 6

    def test_simple_division(self):
        """Test simple division."""
        calc = Calculator()
        assert calc.divide(6, 2) == 3


class TestCalculatorInitialization:
    """Test calculator initialization."""

    def test_calculator_creation(self):
        """Test that calculator can be created."""
        calc = Calculator()
        assert calc is not None


# Note: This test file intentionally has poor coverage
# It doesn't test:
# - Error conditions (divide by zero, square root of negative)
# - Advanced operations (power, square root, absolute)
# - History functionality
# - State management (reset, last result, error count)
# - Number type checking methods
# - Convenience functions
# - Edge cases
# - Negative numbers
# - Float numbers
# - Large numbers
# - And many other features...
