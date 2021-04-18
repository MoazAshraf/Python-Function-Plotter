## The parser validates and parses user input (functions of x) into an
## executable tree of operations. It represents a Model in the MVC pattern.

from .util import split_str
from .expression import *


class Parser(object):
    def __init__(self):
        pass
    
    def parse(self, string):
        """
        Parses an infix expression string to a binary expression tree
        """

        # putting it all together
        infix = self.parse_to_expr_list(string)
        postfix = self.infix_to_postfix(infix)
        tree = self.postfix_to_expr_tree(postfix)
        return tree

    def parse_to_expr_list(self, string):
        """
        Parses a string to an infix expression list of operators and operands
        """
        
        str_list = split_str(string, OPERATORS)
        expr = []

        for op in str_list:
            try:
                # operator
                expr.append(str_to_op(op))
            except:
                # x operand
                if op == 'x':
                    expr.append(Operand(is_x=True))
                else:
                    try:
                        # float operand
                        val = float(op)
                        expr.append(Operand(value=val))
                    except ValueError:
                        raise ValueError(f"Unknown symbol '{op}', use numbers,"
                            " ^, *, /, +, - or x")

        return expr
    
    def infix_to_postfix(self, infix):
        """
        Converts an infix expression to postfix expression
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
