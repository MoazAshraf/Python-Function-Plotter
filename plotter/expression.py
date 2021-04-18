## The expression module contains classes needed to form expression trees that
## can be evaluated

class Operator(object):
    """
    Base operator class.
    Each operator has a string representation, precedence and a python function
    of the form (float, float) => float.
    """

    def __init__(self, string, precedence, func):
        self.string = string
        self.precedence = precedence
        self.func = func
    
    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other.string

class PowOperator(Operator):
    def __init__(self):
        super().__init__('^', 3, pow)


class MulOperator(Operator):
    def __init__(self):
        super().__init__('*', 2, lambda a, b: a * b)


class DivOperator(Operator):
    def __init__(self):
        super().__init__('/', 2, lambda a, b: a / b)


class AddOperator(Operator):
    def __init__(self):
        super().__init__('+', 1, lambda a, b: a + b)


class SubOperator(Operator):
    def __init__(self):
        super().__init__('-', 1, lambda a, b: a - b)


# operator classes dictionary
OPERATORS_DICT = {
    '^': PowOperator,
    '*': MulOperator,
    '/': DivOperator,
    '+': AddOperator,
    '-': SubOperator
}

# list of operators as strings
OPERATORS = list(OPERATORS_DICT.keys())

def str_to_op(string):
    """
    Converts a string to an operator.
    """

    if string in OPERATORS_DICT:
        OpClass = OPERATORS_DICT[string]
        return OpClass()
    else:
        raise SyntaxError(f"Unknown operator '{string}'")


class Operand(object):
    """
    An operand can either by x or a float value.
    """

    def __init__(self, is_x=False, value=None):
        self.is_x = is_x
        if not is_x:
            self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, Operand):
            return False

        if self.is_x and other.is_x:
            return True
        elif self.is_x != other.is_x:
            return False
        else:
            return self.value == other.value
    
    def __str__(self):
        if self.is_x:
            return 'x'
        else:
            return str(self.value)
    
    def evaluate(self, x=0.0):
        """
        Evaluate the operand and return the result as a float.
        x is the value to use if the operand is x. Defaults to 0.
        """

        if self.is_x:
            return x
        else:
            return self.value


class ExprTNode(object):
    """
    A binary expression tree is a data structure that represents expressions
    and can be used to evaluate them efficiently. Expressions have variables (x)
    whose values can be passed as arguments when evaluated. This allows the same
    expression to be evaluated for different values of x.

    This class represents a node in an expression tree.
    Each tree has a key which can be either an operator or an operand and
    pointers to left and right children.
    """

    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        if not isinstance(other, ExprTNode):
            return False
        
        return (self.key == other.key and
                self.left == other.left and
                self.right == other.right)
    
    def evaluate(self, x=0.0):
        """
        Evaluate the expression tree and return the result.
        x is the value to set every occurence of 'x' to. Defaults to 0.
        """

        op = self.key
        if isinstance(op, Operand):
            return op.evaluate(x)
        elif isinstance(op, Operator):
            if self.left is None or self.right is None:
                raise Exception(f"Expression tree incorrect syntactical "
                    "structure")
                    
            # postorder traversal
            a = self.left.evaluate(x)
            b = self.right.evaluate(x)
            return op.func(a, b)
        else:
            raise Exception(f"Unexpected object '{op}' in tree node")