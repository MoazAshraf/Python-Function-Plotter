## The parser service validates the input expression and parses it to an
## expression tree. It is part of the application domain model in the MVP
## architecture.

from ..util import split_str
from ..models.expression import *


# list of separators to use when separating tokens
SEP_LIST = OPERATORS + ['(', ')']


class ParserError(Exception):
    pass


def str_to_op(string):
    """
    Converts a string to an operator if possible.

    Parameters
    ----------
    string : str
        The string representation of the operator.
        Can be one of '^', '*', '/', '+', or '-'.

    Returns
    -------
    operator : Operator
        A matching Operator object
    
    Raises
    ------
    ParserError
        Unknown operator
    """

    if string in OPERATORS_DICT:
        OpClass = OPERATORS_DICT[string]
        return OpClass()
    else:
        raise ParserError(f"Unknown operator '{string}'")


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
        """
        Parameters
        ----------
        string : str
            The string representation of the operator.
        """

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
        """
        Parameters
        ----------
        string : str
            The string representation of the parenthesis, either '(' or ')'. 
        """

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
        Set this operand to its negative.
        """

        pass

    def get_operand(self):
        """
        Returns
        -------
        operand : Operand
            An Operand object representing this token
        """

        pass


class FloatToken(OperandToken):
    """
    Represents a float
    """

    def __init__(self, value):
        """
        Parameters
        ----------
        value : float
            The float value for this operand token
        """

        self.value = value
    
    def negate(self):
        """
        Set this operand to its negative.
        """

        self.value = -self.value
    
    def get_operand(self):
        """
        Returns
        -------
        operand : Operand
            An Operand object representing this token
        """

        return Operand(value=self.value)

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
        """
        Parameters
        ----------
        name : string
            The name of this variable operand token
        is_neg : bool
            Whether this variable should be negated when evaluated
        """
        self.name = name
        self.is_neg = is_neg
    
    def negate(self):
        """
        Set this operand to its negative.
        """

        self.is_neg = not self.is_neg

    def get_operand(self) -> Operand:
        """
        Returns
        -------
        operand : Operand
            An Operand object representing this token
        """

        if self.name == 'x':
            operand = Operand(is_x=True)
            operand.is_neg = self.is_neg
            return operand
        else:
            raise ParserError(f"Unknown symbol '{self.name}', use numbers, "
                                "^, *, /, +, -, (, ), or x")

    def __eq__(self, other):
        if not isinstance(other, VarToken):
            return False
        return self.name == other.name and self.is_neg == other.is_neg
    
    def __str__(self):
        return f"{'-' if self.is_neg else ''}{self.name}"


class Parser(object):
    """
    Represents a Parser service. The Parser takes a raw string as input,
    validates it, tokenizes it and finally builds an expression tree that
    can be evaluated.
    """
    
    def parse(self, string):
        """
        Parses a string that represents a mathematical expression into a binary
        expression tree

        Parameters
        ----------
        string : str
            The raw string to validate and parse

        Returns
        -------
        tree : ExprTNode
            The binary expression tree
        
        Raises
        ------
        ParserError
            Syntax and semantics errors, e.g. unexpected operators, unclosed
            parentheses
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
        Converts a list of strings into a list of known tokens

        Parameters
        ----------
        list_ : list(str)
            A list of raw strings

        Returns
        -------
        token_list : list(Token)
            A list of known tokens
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
    
    def _get_open_paren_index(self, token_list, closing_index):
        """
        Starts at the closing parenthesis and goes in reverse until the open
        parenthesis is found. This method is used internally by
        tokens_to_infix() and shouldn't be called directly.

        Parameters
        ----------
        token_list : list(Token)
            The full token list being processed
        closing_index : int
            The index of the closing parenthesis
        
        Returns
        -------
        open_index : int
            The index of the open parenthesis
        
        Raises
        ------
        ParserError
            Unopened parenthesis or empty parenthesis
        """

        i = closing_index
        stack = [token_list[i]]
        j = i-1
        while j >= 0 and stack:
            tok = token_list[j]
            if isinstance(tok, ParenToken):
                if tok.is_open:
                    stack.pop()
                else:
                    stack.append(tok)
            j -= 1
        j += 1

        if j == i-1:
            raise ParserError("Empty parenthesis")

        if not stack:
            return j
        else:
            raise ParserError("Unopened parenthesis ')'")
    
    def _collapse_operand_signs(self, token_list, operand_index):
        """
        Starts at the operand and goes in reverse collecting all positive and
        negative signs belonging to this operand.

        Parameters
        ----------
        token_list : list(Token)
            The full token list being processed
        operand_index : int
            The index of the operand
        
        Returns
        -------
        next_index : int
            The index of the next token to process, -1 if no tokens left
        sign : int
            The final sign of the operand
        """

        i = operand_index
        j = i-1
        prev_sign = 1
        sign = 1
        while j >= 0:
            tok = token_list[j]
            if isinstance(tok, OpToken):
                if tok.string in ['+', '-']:
                    prev_sign = sign
                    if tok.string == '-':
                        sign = -sign
                else:
                    break
            else:
                if (isinstance(tok, OperandToken) or
                        isinstance(tok, ParenToken) and not tok.is_open):
                    sign = prev_sign
                    j += 1
                break
            j -= 1
        return j, sign

    def _tokens_to_infix(self, token_list):
        """
        Builds valid infix expression from a list of tokens in reverse for
        efficiency. Called internally by tokens_to_infix(), shouldn't be called
        directly.

        Parameters
        ----------
        token_list : list(Token)
            A list of known tokens

        Returns
        -------
        infix : list(Token)
            A reversed valid infix expression
        
        Raises
        ------
        ParserError
            Syntax and semantics errors, e.g. unexpected operators, unclosed
            parentheses        
        """

        infix = []
        i = len(token_list)-1
        last_operator = None
        while i >= 0:
            tok = token_list[i]
            if isinstance(tok, OperandToken):
                i, sign = self._collapse_operand_signs(token_list, i)
                infix.append(tok)
                if sign == -1:
                    if last_operator and last_operator.precedence > 2:
                        # unary + and - have precedence 2, e.g. -x^2 => -1*x^2
                        infix.extend([OpToken('*'), FloatToken(-1)])
                    else:
                        tok.negate()
                continue
            elif isinstance(tok, ParenToken):
                if not tok.is_open:
                    # closing parenthesis
                    j = self._get_open_paren_index(token_list, i)
                    
                    # recursive call on sub expression
                    tokens = token_list[j:i+1]
                    sub_infix = [ParenToken(')')]
                    sub_infix.extend(self._tokens_to_infix(tokens[1:-1]))
                    sub_infix.append(ParenToken('('))
                    
                    # collect sub expression outer sign
                    i, sign = self._collapse_operand_signs(token_list, j)
                    if sign == -1:
                        infix.append(ParenToken(')'))
                        infix.extend(sub_infix)
                        infix.extend([OpToken('*'), FloatToken(-1),
                                      ParenToken('(')])
                    else:
                        infix.extend(sub_infix)
                    continue
                else:
                    # opening parenthesis
                    raise ParserError("Unclosed parenthesis '('")
            elif isinstance(tok, OpToken):
                if not infix or isinstance(infix[-1], OpToken):
                    raise ParserError(f"Unexpected operator '{tok}'")
                last_operator = tok
                infix.append(tok)

            i -= 1
        
        if isinstance(infix[-1], OpToken):
            raise ParserError(f"Unexpected operator '{infix[-1]}'")

        return infix

    def tokens_to_infix(self, token_list):
        """
        Converts a list of tokens into a valid infix expression taking care of
        leading positive and negative signs, unclosed parentheses, etc.

        Parameters
        ----------
        token_list : list(Token)
            A list of known tokens

        Returns
        -------
        infix : list(Token)
            A valid expression
        
        Raises
        ------
        ParserError
            Syntax and semantics errors, e.g. unexpected operators, unclosed
            parentheses
        """

        if not token_list:
            return []

        return list(reversed(self._tokens_to_infix(token_list)))

    def infix_to_postfix(self, infix):
        """
        Converts a valid infix expression to a postfix expression.

        Parameters
        ----------
        infix : list(Token)
            A valid infix expression

        Returns
        -------
        postfix : list(Operator, Operand)
            A list of Operator and Operand objects representing a valid postfix
            expression
        """

        stack = []
        postfix = []

        for op in infix:
            if isinstance(op, OperandToken):
                # operand
                postfix.append(op.get_operand())
            elif isinstance(op, ParenToken):
                if op.is_open:
                    # open parenthesis
                    stack.append(op)
                else:
                    # closing parenthesis
                    while stack and isinstance(stack[-1], OpToken):
                        # pop all operators
                        postfix.append(stack.pop().operator)
                    if stack and isinstance(stack[-1], ParenToken):
                        # open parenthesis reached
                        stack.pop()
            elif isinstance(op, OpToken):   
                while (stack and isinstance(stack[-1], OpToken) and
                        op.precedence <= stack[-1].precedence):
                    # pop all operators with higher or equal precedence
                    postfix.append(stack.pop().operator)
                stack.append(op)

        # pop any remaining operators
        while stack:
            postfix.append(stack.pop().operator)
        
        return postfix
        
    def postfix_to_expr_tree(self, postfix):
        """
        Converts a postfix expression to a binary expression tree.

        Parameters
        ----------
        postfix : list(Operator, Operand)
            A list of Operator and Operand objects representing a valid postfix
            expression

        Returns
        -------
        tree : ExprTNode
            A valid binary expression tree ready to be evaluated.
        
        Raises
        ------
        ParserError
            Invalid postfix expression
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
                    raise ParserError("Invalid expression")

        if len(stack) == 1:
            return stack[-1]
        else:
            raise ParserError("Invalid expression")
