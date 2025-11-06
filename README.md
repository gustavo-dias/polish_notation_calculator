# Polish Notation Calculator

This repo contains a script that implements a basic Polish notation calculator, i.e., a calculator capable of evaluating basic aritmetic expressions written in Polish notation [1]. By basic we mean expression that only involve four fundamental aritmetic operations: addition, subtraction, multiplication and division.

E.g.: "+ - / 4 2 1 5" = ((4/2) - 1) + 5 = 6.

### Environment and Usage

The script requires only Python 3.12+.

It can be run as:

`python3 pn_calculator.py --expression <expression>`

E.g.: `python3 pn_calculator.py --expression "+ - / 4 2 1 5"`

The input is a string containing operands and operatos separated by whitespaces; the supported operators are +, -, *, /.

### Output

The value of the expression.

### References
[1] https://en.wikipedia.org/wiki/Polish_notation
