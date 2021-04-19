## The parser validates and parses user input (functions of x) into an
## executable tree of operations. It represents a Model in the MVC pattern.

from ..util import split_str
from ..models.expression import *


SEP_LIST = OPERATORS + ['(', ')']

class Token(object):
    """
    A token can be an operator, parentheses, a variable or a float
    """

    pass


class OpToken(Token):
    """
    Represents an operator
    """
    
    def __init__(self, string):
        self.string = string
    
    def __eq__(self, other):
        if not isinstance(other, OpToken):
            return False
        return self.string == other.string
    
    def __str__(self):
        return self.string


class ParenToken(Token):
    """
    Represents an opening or closing parenthesis
    """

    def __init__(self, string):
        if string == '(':
            self.is_open = True
        elif string == ')':
            self.is_open = False
    
    def __eq__(self, other):
        if not isinstance(other, ParenToken):
            return False
        return self.is_open == other.is_open
    
    def __str__(self):
        return ('(' if self.is_open else ')')


class FloatToken(Token):
    """
    Represents a float
    """

    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, FloatToken):
            return False
        return self.value == other.value
    
    def __str__(self):
        return str(self.value)


class VarToken(Token):
    """
    Represents a variable, e.g. x
    """
    
    def __init__(self, name):
        self.name = name
    
    def __eq__(self, other):
        if not isinstance(other, VarToken):
            return False
        return self.name == other.name
    
    def __str__(self):
        return self.name


class Parser(object):
    def __init__(self):
        pass
    
    def parse(self, string):
        """
        Parses a string that represents a mathematical expression into a binary
        expression tree
        """

        # putting it all together
        list_ = split_str(string, SEP_LIST)
        token_list = self.tokenize(list_)
        infix = self.tokens_to_infix(token_list)
        postfix = self.infix_to_postfix(infix)
        tree = self.postfix_to_expr_tree(postfix)

        return tree

    def tokenize(self, list_):
        """
        Converts a list of strings into a list of valid tokens
        """

        token_list = []
        i = 0
        while i < len(list_):
            op = list_[i]

            # remove leading and trailing whitespace
            op = op.strip()
            if not op:
                i += 1
                continue

            if op in ['(', ')']:
                # parenthesis
                token_list.append(ParenToken(op))
            elif op in OPERATORS:
                # operator
                token_list.append(OpToken(op))
            else:
                try:
                    # float operand
                    value = ''.join(op.split())  # remove whitespace
                    value = float(value)
                    token_list.append(FloatToken(value))
                except ValueError:
                    # split on whitespace and add it to the list
                    op_list = op.split()
                    if len(op_list) == 1:
                        # variable
                        token_list.append(VarToken(op))
                    else:
                        list_ = list_[:i] + op_list + list_[i+1:]
                        continue
            i += 1
        
        return token_list
    
    def tokens_to_infix(self, token_list):
        """
        Converts a list of tokens into a valid infix expression taking care of
        leading positive and negative signs, unclosed parentheses, etc.
        """

        # [] means a single token
        # -2 => [-2]
        # +2 => 2
        # 4+-2 => 4+[-2]
        # 4++--2 => 4+2
        # 2^-3 => 2^[-3]
        # -(3) => [-1]*(3)
        # -2^-3 => [-1]*2^[-3]


        return []

    def infix_to_postfix(self, infix):
        """
        Converts a valid infix expression to postfix expression
        """

        stack = []
        postfix = []
        for op in infix:
            if isinstance(op, Operand):
                postfix.append(op)
            else:
                while stack and op.precedence <= stack[-1].precedence:
                    postfix.append(stack.pop())
                stack.append(op)

        # push any remaining operators
        while stack:
            postfix.append(stack.pop())
        
        return postfix
        
    def postfix_to_expr_tree(self, postfix):
        """
        Converts a postfix expression to a binary expression tree
        """

        if not postfix:
            return None

        stack = []
        for op in postfix:
            if isinstance(op, Operand):
                stack.append(ExprTNode(op))
            else:
                if len(stack) >= 2:
                    right = stack.pop()
                    left = stack.pop()
                    node = ExprTNode(op, left=left, right=right)
                    stack.append(node)
                else:
                    # TODO: be more specific
                    raise SyntaxError("Invalid expression")

        if len(stack) == 1:
            return stack[-1]
        else:
            raise SyntaxError("Invalid expression")
