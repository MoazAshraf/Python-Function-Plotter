## The expression module contains entities needed to form binary expression
## trees that can be evaluated.

from ..util import EvaluationError
import numpy as np


class Operator(object):
    """
    Base binary operator class.
    Each operator has a string representation, precedence and a python function
    of the form (float, float) => float.
    """

    def __init__(self, string, precedence, func):
        """
        Parameters
        ----------
        string : str
            The operator's string representation
        precedence : int
            The operator's precedence
        func : (float, float) -> float
            The function used to evaluate this operator
        """

        self.string = string
        self.precedence = precedence
        self.func = func
    
    def __str__(self):
        return self.string

    def __eq__(self, other):
        if not isinstance(other, Operator):
            return False
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


class Operand(object):
    """
    An operand can either be x or a float value.
    """

    def __init__(self, is_x=False, is_neg_x=False, value=None):
        """
        Parameters
        ----------
        is_x : bool
            If True, creates an 'x' operand
        is_neg_x : bool
            If True, creates a '-x' operand
        value : float
            If provided, creates a float operand with this value
        """

        if is_x:
            self.is_x = True
            self.is_neg = False
        elif is_neg_x:
            self.is_x = True
            self.is_neg = True
        else:
            self.is_x = False
            self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, Operand):
            return False

        if self.is_x and other.is_x:
            return self.is_neg == other.is_neg
        elif self.is_x != other.is_x:
            return False
        else:
            return self.value == other.value
    
    def __str__(self):
        if self.is_x:
            if self.is_neg:
                return '-x'
            else:
                return 'x'
        else:
            return str(self.value)
    
    def evaluate(self, x=0.0):
        """
        Evaluate the operand.
        
        Parameters
        ----------
        x
            The value of x to substitute into the operand if it's a variable
            'x' operand. Can be a numpy ndarray.
            Defaults to 0.

        Returns
        -------
        result
            Has the same type as x
        """

        if self.is_x:
            return x * (-1 if self.is_neg else 1)
        else:
            if isinstance(x, np.ndarray):
                return np.full_like(x, self.value)
            return self.value


class ExprTNode(object):
    """
    A binary expression tree is a data structure that represents expressions
    and can be used to evaluate them efficiently. Expressions have variables (x)
    whose values can be passed as arguments when evaluated. This allows the same
    expression to be evaluated for different values of x.

    This class represents a node in an expression tree.
    """

    def __init__(self, key, left=None, right=None):
        """
        Parameters
        ----------
        key : Operator or Operand
            The key of this node, an Operator or Operand object
        left : ExprTNode
            The left child of this node
        right : ExprTNode
            The right child of this node
        """

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
        Evaluate the expression tree.
        
        Parameters
        ----------
        x
            The value of x to substitute into 'x' operands.
            Can be a numpy ndarray.
            Defaults to 0.

        Returns
        -------
        result
            Has the same type as x
        
        Raises
        ------
        EvaluationError
            Tree is built incorrectly
        """

        op = self.key
        if isinstance(op, Operand):
            return op.evaluate(x)
        elif isinstance(op, Operator):
            if self.left is None or self.right is None:
                raise EvaluationError(f"Expression tree has an incorrect "
                    "syntactical structure")
                    
            # postorder traversal
            a = self.left.evaluate(x)
            b = self.right.evaluate(x)
            return op.func(a, b)
        else:
            raise EvaluationError(f"Unexpected object '{op}' in tree node")
            