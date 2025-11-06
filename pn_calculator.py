#!usr/bin/env

"""Docstring of script pn_calculator.py.

This script implements a Polish notation (PN) calculator, meaning it accepts a
string representing an aritmetic expression described using Polish notation and
returns the value of its evaluation. E.g.: '+ - 4 1 3' = (4-1)+3 = 6.

Classes
-------
    - PNExpression(object)

Functions
---------
    - convert_to_number(value: str) -> Union[int, float, str]
    - convert_to_callable(value: str) -> Union[Callable, str]
    - add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    - sub(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    - div(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    - mul(a: Union[int, float], b: Union[int, float]) -> Union[int, float]
    - get_cli_arguments() -> Union[None, list[Any]]
    - main() -> None
"""

from __future__ import annotations

from argparse import ArgumentParser
from time import time
from logging import Logger, getLogger, DEBUG, basicConfig
from typing import Any, Callable, Union
from os.path import basename


logger: Logger = getLogger(basename(__file__))
basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=DEBUG)

APP_NAME: str = "Polish Notation Calculator"
APP_DESCRIPTION: str = \
    "Evaluates an aritmetic expression written in Polish notation."
ARGPARSER_ERROR_MSG: str = "The argument must be a str."


class PNExpression(object):
    """Class that represents aritmetic expressions in Polish notation.

    Attributes
    ----------
        - expression: str \\
        The expression to be evaluated.

    Methods
    -------
        - evaluate() -> Union[int, float]
    """

    def __init__(self, expression: str) -> None:
        """Initialize a PNExpression instance.

        Parameters
        ----------
            - expression: str \\
            The string representing the aritmetic expression to be evaluated.

        Raises
        ------
            - TypeError if expression is not a str.
        """
        self.expression: str = expression
        self._nodes: list = []
        self._evaluate_at_idx: int = 0
        self._parse_input(expression)

    @property
    def expression(self) -> str:
        """Get or set the aritmetic expression.

        The operators and operands must be a whitespace separated, as in
        '+ / 1 5 7'.

        Parameters
        ----------
            - value: str \\
            The expression in polish notation.

        Raise
        -----
            TypeError if value is not a str.
        """
        return self._expression

    @expression.setter
    def expression(self, value: str) -> None:
        """"""
        if not isinstance(value, str):
            raise TypeError(
                "PNExpression.expression: param value must be a str, got "
                f"a(n) {type(value).__name__}."
            )
        self._expression = value

    def _parse_input(self, input: str) -> None:
        """Parse the input expression."""
        values: list = str(input).split(' ')
        for idx, value in enumerate(values):
            self._nodes.append(convert_to_callable(convert_to_number(value)))
            if callable(self._nodes[-1]):
                self._evaluate_at_idx = idx

    def evaluate(self) -> Union[int, float]:
        """Evaluate the PN expression."""
        while True:
            # because pop removes the item from the list, we look twice at
            # self._evaluate_at_idx+1 to fetch the operands
            self._nodes[self._evaluate_at_idx] = \
                self._nodes[self._evaluate_at_idx](
                    self._nodes.pop(self._evaluate_at_idx+1),
                    self._nodes.pop(self._evaluate_at_idx+1),
                )
            self._evaluate_at_idx -= 1
            if self._evaluate_at_idx == -1:
                break
        return self._nodes[0]


def convert_to_number(value: str) -> Union[int, float, str]:
    """Convert value to either int or float.

    If value is not convertible (i.e. an operator), return value.
    """
    try:
        return int(value)
    except Exception:
        try:
            return float(value)
        except Exception:
            return value


def convert_to_callable(value: str) -> Union[Callable, str]:
    """Return the respective callable of value.

    If there is none (i.e. value is a number), return param.
    """
    callable = callable_per_operator.get(value)
    if callable is None:
        return value
    return callable


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return a+b"""
    return a+b


def sub(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return a-b."""
    return a-b


def mul(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return a*b."""
    return a*b


def div(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Return a/b."""
    return a/b


callable_per_operator: dict = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div,
}


def get_cli_arguments() -> Union[None, list[Any]]:
    """Get the arguments passed to the script via cli.

    Returns
    -------
        (a) None if there is an error parsing the cli arguments, (b) an empty
        list if no argument is passed or (c) a filled list otherwise.
    """
    parser = ArgumentParser(prog=APP_NAME, description=APP_DESCRIPTION)
    parser.add_argument('-e', '--expression', type=str, required=True)

    try:
        args = parser.parse_args()
    except SystemExit:
        logger.error(ARGPARSER_ERROR_MSG)
        return None
    else:
        if not vars(args):
            return []
        return [args.expression]


def main() -> None:
    """Run script in full."""
    logger.info("Execution started.")
    start = time()

    try:
        args = get_cli_arguments()
    except Exception as exc:
        logger.error("Unexpected error caught; see details below:")
        logger.exception(exc)
    else:
        if args is not None:
            logger.info(f"Result: {PNExpression(*args).evaluate()}.")

    end = time()
    logger.info(f"Execution ended after {end-start:.2f} seconds.")


if __name__ == '__main__':
    main()
