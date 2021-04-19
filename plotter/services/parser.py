## The parser validates and parses user input (functions of x) into an
## executable tree of operations. It represents a Model in the MVC pattern.

from ..util import split_str
from ..models.expression import *


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

    def _parse_raw_expr_list(self, string):
        """
        Parses a string to an infix expression list of operators and operands.
        Doesn't take care of positive and negative signs
        """
        
        str_list = split_str(string, OPERATORS)
        expr = []

        i = 0
        while i < len(str_list):
            op = str_list[i]

            # remove leading and trailing whitespace
            op = op.strip()
            if not op:
                i += 1
                continue

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
                        val = ''.join(op.split())  # remove whitespace
                        val = float(val)
                        expr.append(Operand(value=val))
                    except ValueError:
                        # split on whitespace and add it to the list
                        op_list = op.split()
                        if len(op_list) == 1:
                            raise ValueError(f"Unknown symbol '{op}', use "
                                "numbers, ^, *, /, +, - or x")
                        else:
                            str_list = str_list[:i] + op_list + str_list[i+1:]
                            continue
            i += 1
        
        return expr

    def _combine_signs_in_expr(self, expr):
        """
        Combines positive and negative signs with operands
        """

        if not expr:
            return []

        new_expr = []
        current_operand = None
        for i in range(len(expr)-1, -1, -1):
            if isinstance(expr[i], Operand):
                current_operand = expr[i]
            else:
                if current_operand is None:
                    # trailing operator
                    raise SyntaxError("Invalid expression")

                # if there's a sign after this operator, combine it with the
                # next operand
                if isinstance(new_expr[-1], AddOperator):
                    new_expr = new_expr[:-1]
                elif isinstance(new_expr[-1], SubOperator):
                    current_operand.reverse_sign()
                    new_expr = new_expr[:-1]
            
                # stop tracking this operand if the operator is neither + nor -
                if (not isinstance(expr[i], AddOperator) and
                        not isinstance(expr[i], SubOperator)):
                    # another operator type
                    current_operand = None

            new_expr.append(expr[i])

        # combine final positive or negative sign with operand
        if isinstance(new_expr[-1], AddOperator):
            new_expr = new_expr[:-1]
        elif isinstance(new_expr[-1], SubOperator):
            current_operand.reverse_sign()
            new_expr = new_expr[:-1]

        return list(reversed(new_expr))

    def parse_to_expr_list(self, string):
        """
        Parses a string to an infix expression list of operators and operands.
        Also takes care of positive and negative signs.
        """

        expr = self._parse_raw_expr_list(string)
        expr = self._combine_signs_in_expr(expr)
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
