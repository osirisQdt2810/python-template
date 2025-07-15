"""
High coverage test suite for the calculator module.
This file aims to test most of the functionality and edge cases.
"""

from io import StringIO
import sys
from unittest.mock import patch

import pytest

from my_package import cli
from my_package.calculator import Calculator, add, divide, multiply, subtract


class TestCalculatorBasicOperations:
    """Test the four basic operations with comprehensive coverage."""

    def test_add_positive_numbers(self):
        """Test addition with positive numbers."""
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(0, 0) == 0
        assert calc.add(1.5, 2.5) == 4.0

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        calc = Calculator()
        assert calc.add(-2, -3) == -5
        assert calc.add(-1, 1) == 0
        assert calc.add(-5, 3) == -2

    def test_subtract_positive_numbers(self):
        """Test subtraction with positive numbers."""
        calc = Calculator()
        assert calc.subtract(5, 3) == 2
        assert calc.subtract(0, 0) == 0
        assert calc.subtract(1.5, 0.5) == 1.0

    def test_subtract_negative_numbers(self):
        """Test subtraction with negative numbers."""
        calc = Calculator()
        assert calc.subtract(-5, -3) == -2
        assert calc.subtract(-1, 1) == -2
        assert calc.subtract(5, -3) == 8

    def test_multiply_positive_numbers(self):
        """Test multiplication with positive numbers."""
        calc = Calculator()
        assert calc.multiply(2, 3) == 6
        assert calc.multiply(0, 5) == 0
        assert calc.multiply(1.5, 2) == 3.0

    def test_multiply_negative_numbers(self):
        """Test multiplication with negative numbers."""
        calc = Calculator()
        assert calc.multiply(-2, 3) == -6
        assert calc.multiply(-2, -3) == 6
        assert calc.multiply(-1, 0) == 0

    def test_divide_positive_numbers(self):
        """Test division with positive numbers."""
        calc = Calculator()
        assert calc.divide(6, 2) == 3
        assert calc.divide(7, 2) == 3.5
        assert calc.divide(0, 5) == 0

    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        calc = Calculator()
        assert calc.divide(-6, 2) == -3
        assert calc.divide(-6, -2) == 3
        assert calc.divide(6, -2) == -3

    def test_divide_by_zero(self):
        """Test division by zero raises ZeroDivisionError."""
        calc = Calculator()
        with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
            calc.divide(5, 0)
        assert calc.get_error_count() == 1


class TestCalculatorAdvancedOperations:
    """Test advanced calculator operations."""

    def test_power_positive_numbers(self):
        """Test power operation with positive numbers."""
        calc = Calculator()
        assert calc.power(2, 3) == 8
        assert calc.power(5, 0) == 1
        assert calc.power(1, 100) == 1

    def test_power_negative_numbers(self):
        """Test power operation with negative numbers."""
        calc = Calculator()
        assert calc.power(-2, 3) == -8
        assert calc.power(-2, 2) == 4
        assert calc.power(2, -2) == 0.25

    def test_square_root_positive_numbers(self):
        """Test square root with positive numbers."""
        calc = Calculator()
        assert calc.square_root(4) == 2
        assert calc.square_root(0) == 0
        assert calc.square_root(1) == 1
        assert calc.square_root(9) == 3

    def test_square_root_negative_number(self):
        """Test square root with negative number raises ValueError."""
        calc = Calculator()
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            calc.square_root(-1)
        assert calc.get_error_count() == 1

    def test_absolute_positive_numbers(self):
        """Test absolute value with positive numbers."""
        calc = Calculator()
        assert calc.absolute(5) == 5
        assert calc.absolute(0) == 0
        assert calc.absolute(3.14) == 3.14

    def test_absolute_negative_numbers(self):
        """Test absolute value with negative numbers."""
        calc = Calculator()
        assert calc.absolute(-5) == 5
        assert calc.absolute(-3.14) == 3.14
        assert calc.absolute(-0) == 0


class TestCalculatorUtilityMethods:
    """Test utility methods like history, state management, etc."""

    def test_history_tracking(self):
        """Test that operations are recorded in history."""
        calc = Calculator()
        calc.add(2, 3)
        calc.subtract(5, 2)
        calc.multiply(2, 4)

        history = calc.get_history()
        assert len(history) == 3
        assert "2 + 3 = 5" in history[0]
        assert "5 - 2 = 3" in history[1]
        assert "2 x 4 = 8" in history[2]

    def test_history_limit(self):
        """Test that history is limited to 100 operations."""
        calc = Calculator()
        # Perform 101 operations
        for i in range(101):
            calc.add(i, 1)

        history = calc.get_history()
        assert len(history) == 100
        # First operation should be removed
        assert "0 + 1 = 1" not in history[0]
        assert "100 + 1 = 101" in history[-1]

    def test_clear_history(self):
        """Test clearing operation history."""
        calc = Calculator()
        calc.add(2, 3)
        calc.subtract(5, 2)

        calc.clear_history()
        assert len(calc.get_history()) == 0

    def test_last_result_tracking(self):
        """Test that last result is tracked properly."""
        calc = Calculator()
        assert calc.get_last_result() is None

        calc.add(2, 3)
        assert calc.get_last_result() == 5

        calc.multiply(2, 4)
        assert calc.get_last_result() == 8

    def test_error_count_tracking(self):
        """Test that error count is tracked properly."""
        calc = Calculator()
        assert calc.get_error_count() == 0

        # Cause a division by zero error
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)
        assert calc.get_error_count() == 1

        # Cause a square root error
        with pytest.raises(ValueError):
            calc.square_root(-1)
        assert calc.get_error_count() == 2

    def test_reset_functionality(self):
        """Test reset functionality."""
        calc = Calculator()
        calc.add(2, 3)
        calc.multiply(4, 5)

        # Cause an error
        with pytest.raises(ZeroDivisionError):
            calc.divide(5, 0)

        # Reset and verify everything is cleared
        calc.reset()
        assert len(calc.get_history()) == 0
        assert calc.get_last_result() is None
        assert calc.get_error_count() == 0

    def test_number_type_checking(self):
        """Test number type checking methods."""
        calc = Calculator()

        # Test positive numbers
        assert calc.is_positive(5) is True
        assert calc.is_positive(0) is False
        assert calc.is_positive(-5) is False

        # Test negative numbers
        assert calc.is_negative(-5) is True
        assert calc.is_negative(0) is False
        assert calc.is_negative(5) is False

        # Test zero
        assert calc.is_zero(0) is True
        assert calc.is_zero(5) is False
        assert calc.is_zero(-5) is False


class TestConvenienceFunctions:
    """Test standalone convenience functions."""

    def test_convenience_add(self):
        """Test convenience add function."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0

    def test_convenience_subtract(self):
        """Test convenience subtract function."""
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5

    def test_convenience_multiply(self):
        """Test convenience multiply function."""
        assert multiply(2, 3) == 6
        assert multiply(-2, 3) == -6

    def test_convenience_divide(self):
        """Test convenience divide function."""
        assert divide(6, 2) == 3
        assert divide(7, 2) == 3.5

        with pytest.raises(ZeroDivisionError):
            divide(5, 0)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_large_numbers(self):
        """Test operations with large numbers."""
        calc = Calculator()
        large_num = 1e10
        assert calc.add(large_num, large_num) == 2e10
        assert calc.multiply(large_num, 2) == 2e10

    def test_small_numbers(self):
        """Test operations with very small numbers."""
        calc = Calculator()
        small_num = 1e-10
        assert calc.add(small_num, small_num) == 2e-10
        assert calc.multiply(small_num, 2) == 2e-10

    def test_float_precision(self):
        """Test float precision handling."""
        calc = Calculator()
        # Test with numbers that might have precision issues
        result = calc.add(0.1, 0.2)
        assert abs(result - 0.3) < 1e-10

    def test_integer_division(self):
        """Test integer division results."""
        calc = Calculator()
        assert calc.divide(5, 2) == 2.5
        assert calc.divide(4, 2) == 2.0
        assert calc.divide(1, 3) == 1 / 3


class TestCLI:
    """Test the CLI interface."""

    def test_main_func(self):
        cli.main()

    def test_add_func(self):
        assert cli.add(2, 3) == 5

    def test_add_argparse_cli(self):
        test_args = ["", "--num1", "2", "--num2", "3"]  # argparse automatically uses sys.argv[1:]
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = cli.add_argparse_cli()  # Call the function
                # Capture the printed output
                output = mock_stdout.getvalue().strip()
                # Check if the expected print statement was produced
                assert output == "The result is 5.0"
                # Optionally, you can assert the returned result as well
                assert result == 5.0

    def test_my_function(self):
        assert cli.my_function(1, 2, 3) == "hello"
        assert cli.my_function(2, 2, 3) == "world"

    def test_runc_func(self):
        test_args = ["", "--num1", "2", "--num2", "3"]  # argparse automatically uses sys.argv[1:]
        with patch.object(sys, "argv", test_args):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                cli.run()
                output = mock_stdout.getvalue().strip()
                assert output == "Run function!!!\nThe result is 5.0"
