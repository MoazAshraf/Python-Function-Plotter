## The parser validates and parses user input (functions of x) into an
## executable tree of operations. It represents a Model in the MVC pattern.

from enum import Enum
from util import split_str


class Operator(Enum):
    POW = 1
    MULT = 2
    DIV = 3
    ADD = 4
    SUB = 5


class Operand(object):
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
            self.isvariable = False
        elif isinstance(value, str):
            self.name = value
            self.isvariable = True


class Parser(object):
    def __init__(self):
        pass

    def parse_to_expr_list(string):
        """
        Parses a string to an infix expression list of operators and operands
        """
        
        expr = []
        # TODO