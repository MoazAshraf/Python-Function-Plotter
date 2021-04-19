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
        self.operator = str_to_op(string)
        self.precedence = self.operator.precedence
    
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


class OperandToken(Token):
    """
    Represents an operand
    """

    def negate(self):
        """
        Set this token to its negative
        """

        pass

    def get_operand(self) -> Operand:
        """
        Returns an Operand object representing this token if possible
        """

        pass


class FloatToken(OperandToken):
    """
    Represents a float
    """

    def __init__(self, value):
        self.value = value
    
    def negate(self):
        self.value = -self.value
    
    def get_operand(self) -> Operand:
        return Operand(value=value)

    def __eq__(self, other):
        if not isinstance(other, FloatToken):
            return False
        return self.value == other.value
    
    def __str__(self):
        return str(self.value)


class VarToken(OperandToken):
    """
    Represents a variable, e.g. x
    """
    
    def __init__(self, name, is_neg=False):
        self.name = name
        self.is_neg = is_neg
    
    def negate(self):
        self.is_neg = not self.is_neg

    def get_operand(self) -> Operand:
        if self.name == 'x':
            operand = Operand(is_x=True)
            operand.is_neg = self.is_neg
        else:
            raise ValueError(f"Unknown symbol '{op}', use numbers, "
                             "^, *, /, +, -, (, ), or x")

    def __eq__(self, other):
        if not isinstance(other, VarToken):
            return False
        return self.name == other.name and self.is_neg == other.is_neg
    
    def __str__(self):
        return f"{'-' if self.is_neg else ''}{self.name}"


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
        # -2^3 => [-1]*2^3
        # -2*3 => [-2]*3

        if not token_list:
            return []

        infix = []
        paren_stack = []
        last_nonoperator = None
        last_operator = None
        for i in range(len(token_list)-1, -1, -1):
            tok = token_list[i]
            if isinstance(tok, OperandToken):
                infix.append(tok)
                last_nonoperator = tok
            elif isinstance(tok, ParenToken):
                infix.append(tok)
                last_nonoperator = tok
                if not tok.is_open:
                    paren_stack.append(tok)
                else:
                    if paren_stack:
                        paren_stack.pop()
                    else:
                        raise SyntaxError("Unclosed parenthesis '('")
            elif isinstance(tok, OpToken):
                if (not infix or isinstance(infix[-1], ParenToken) and
                        not infix[-1].is_open):
                    # trailing operator at the end or before closing parenthesis
                    raise SyntaxError(f"Unexpected operator '{tok.string}'")

                if isinstance(infix[-1], OpToken):
                    raise SyntaxError("Unexpected operator "
                                      f"'{infix[-1].string}'")

                if tok.string in ['+', '-']:
                    if i == 0 or isinstance(token_list[i-1], OpToken):
                        if tok.string == '-':
                            if (last_operator is not None and 
                                    last_operator.precedence > tok.precedence or
                                    isinstance(last_nonoperator, ParenToken) and
                                    last_nonoperator.is_open):
                                # add -1 * if '(' or higher precedence operator
                                infix.append(OpToken('*'))
                                infix.append(FloatToken(-1))
                            else:
                                # negate if operand
                                last_nonoperator.negate()
                    else:
                        infix.append(tok)
                else:
                    infix.append(tok)
                
                last_operator = tok

        if isinstance(infix[-1], OpToken):
            raise SyntaxError(f"Unexpected operator '{tok.string}'")

        if paren_stack:
            raise SyntaxError("Unopen parenthesis ')'")

        return list(reversed(infix))

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
