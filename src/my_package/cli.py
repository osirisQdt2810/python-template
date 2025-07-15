import argparse

import typer
from typing_extensions import Any

from my_package.new import sub

# This file contains the logic for our command-line tool.
app = typer.Typer()

def main() -> None:
    """
    The main entry point for the CLI tool.
    """
    print("Hello from my-professional-python-project!")
    print("This is a command-line tool defined in pyproject.toml.")
    sub(1, 1)

# A pure, fully-typed helper that can be used safely from both CLI paths.
def _add_numbers(a: int, b: int) -> int:
    """
    Add two integers and return the result.
    """
    return a + b

# mypy complains that Typer's decorator isn't fully typed; ignore that.
@app.command()
def add(a: int, b: int) -> int:
    """
    Add two integers and echo the result via Typer command.
    """
    result = _add_numbers(a, b)
    print(f"Adding {a} and {b}: {result}")
    return result

# @app.command()
# def add_typer_cli(
#     #  signifies that a command-line option or argument is required
#     num1: float = typer.Option(..., help="The first number to add."),
#     num2: float = typer.Option(..., help="The second number to add."),
# ):
#     """Add two numbers together."""
#     result = add(num1, num2)
#     typer.echo(f"The result is {result}")
#     return result

def add_argparse_cli() -> int:
    """
    Add two numbers together.
    """
    parser = argparse.ArgumentParser(description="Add two numbers together.")
    parser.add_argument("--num1", type=float, help="The first number to add.")
    parser.add_argument("--num2", type=float, help="The second number to add.")
    args = parser.parse_args()
    num1 = args.num1
    num2 = args.num2
    result = _add_numbers(num1, num2)
    print(f"The result is {result}")
    return result

def run() -> None:
    # app()
    print("Run function!!!")
    add_argparse_cli()

def my_function(a: int, b: Any, c: Any) -> str:
    """
    This is a docstring that is way too long and should definitely be wrapped by black to fit on a
    This is a docstring that is way too long and should definitely be wrapped by black to fit on a
    single line but it is not because it has not been formatted yet.
    """
    print("Hello")  # This line has 4 spaces
    if a == 1:
        return "hello"
    else:
        return "world"

if __name__ == "__main__":  # pragma: no cover
    run()
