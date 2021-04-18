## The expression module contains classes needed to form expression trees that
## can be evaluated

class Operator(object):
    def __init__(self, string, precedence):
        self.string = string
        self.precedence = precedence
    
    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.string == other.string

class PowOperator(Operator):
    def __init__(self):
        super().__init__('^', 3)


class MulOperator(Operator):
    def __init__(self):
        super().__init__('*', 2)


class DivOperator(Operator):
    def __init__(self):
        super().__init__('/', 2)


class AddOperator(Operator):
    def __init__(self):
        super().__init__('+', 1)


class SubOperator(Operator):
    def __init__(self):
        super().__init__('-', 1)


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
    Converts a string to an operator
    """

    if string in OPERATORS_DICT:
        OpClass = OPERATORS_DICT[string]
        return OpClass()
    else:
        raise SyntaxError(f"Unknown operator '{string}'")


class Operand(object):
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


class TreeNode(object):
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
    
    def __eq__(self, other):
        if not isinstance(other, TreeNode):
            return False
        
        return (self.key == other.key and
                self.left == other.left and
                self.right == other.right)
