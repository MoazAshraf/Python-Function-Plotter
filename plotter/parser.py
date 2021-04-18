## The parser validates and parses user input (functions of x) into an
## executable tree of operations. It represents a Model in the MVC pattern.

from enum import Enum
from .util import split_str


class Operator(Enum):
    POW = 1
    MUL = 2
    DIV = 3
    ADD = 4
    SUB = 5

# String to operator
STR_TO_OPERATOR = {
    '^': Operator.POW,
    '*': Operator.MUL,
    '/': Operator.DIV,
    '+': Operator.ADD,
    '-': Operator.SUB
}

# list of operators as strings
OPERATORS = list(STR_TO_OPERATOR.keys())

class Operand(object):
    def __init__(self, is_x=False, value=None):
        self.is_x = is_x
        if not is_x:
            self.value = value
    
    def __eq__(self, other):
        if self.is_x and other.is_x:
            return True
        elif self.is_x != other.is_x:
            return False
        else:
            return self.value == other.value


class Parser(object):
    def __init__(self):
        pass

    def parse_to_expr_list(self, string):
        """
        Parses a string to an infix expression list of operators and operands
        """
        
        str_list = split_str(string, OPERATORS)
        expr = []

        for op in str_list:
            # operator
            if op in STR_TO_OPERATOR:
                expr.append(STR_TO_OPERATOR[op])
            else:
                # operand
                try:
                    # float operand
                    val = float(op)
                    expr.append(Operand(value=val))
                except ValueError:
                    # x operand
                    if op == 'x':
                        expr.append(Operand(is_x=True))
                    else:
                        raise ValueError(f"Unknown symbol '{op}', use numbers,"
                            " ^, *, /, +, - or x")

        return expr