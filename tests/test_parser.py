import pytest
from plotter.services.parser import *
from plotter.models.expression import *


@pytest.mark.unit
class TestTokenEquality(object):
    def test_4_and_4(self):
        assert FloatToken(4) == FloatToken(4)
    
    def test_4_and_2(self):
        assert FloatToken(4) != FloatToken(2)
    
    def test_4_and_plus(self):
        assert FloatToken(4) != OpToken('+')

    def test_4_and_open(self):
        assert FloatToken(4) != ParenToken('(')
    
    def test_4_and_x(self):
        assert FloatToken(4) != VarToken('x')
    
    def test_plus_and_plus(self):
        assert OpToken('+') == OpToken('+')
    
    def test_plus_and_minus(self):
        assert OpToken('+') != OpToken('-')
    
    def test_x_and_x(self):
        assert VarToken('x') == VarToken('x')

    def test_x_and_neg_x(self):
        assert VarToken('x') != VarToken('x', is_neg=True)
    
    def test_x_and_y(self):
        assert VarToken('x') != VarToken('y')
    
    def test_open_and_open(self):
        assert ParenToken('(') == ParenToken('(')
    
    def test_open_and_close(self):
        assert ParenToken('(') != ParenToken(')')


@pytest.mark.unit
class TestTokenize(object):
    def test_empty(self):
        parser = Parser()
        list_ = []
        expected = []
        assert parser.tokenize(list_) == expected
    
    def test_float(self):
        parser = Parser()
        list_ = ["4.2"]
        expected = [FloatToken(4.2)]
        assert parser.tokenize(list_) == expected

    def test_float_whitespace(self):
        parser = Parser()
        list_ = ["4 . 2"]
        expected = [FloatToken(4.2)]
        assert parser.tokenize(list_) == expected

    def test_add(self):
        parser = Parser()
        list_ = ["4.3 ", "+", " 2.23"]
        expected = [FloatToken(4.3), OpToken('+'), FloatToken(2.23)]
        assert parser.tokenize(list_) == expected
    
    def test_add_whitespace(self):
        parser = Parser()
        list_ = ["4 . 3", "+", "2 . 23"]
        expected = [FloatToken(4.3), OpToken('+'), FloatToken(2.23)]
        assert parser.tokenize(list_) == expected
    
    def test_pos_2(self):
        parser = Parser()
        list_ = ["+", "2"]
        expected = [OpToken('+'), FloatToken(2)]
        assert parser.tokenize(list_) == expected
    
    def test_4_plus_neg_2(self):
        parser = Parser()
        list_ = ['4', '+', '-', '2']
        expected = [FloatToken(4), OpToken('+'), OpToken('-'),
                    FloatToken(2)]
        assert parser.tokenize(list_) == expected

    def test_neg_2_pow_3(self):
        parser = Parser()
        list_ = ['-', '2', '^', '3']
        expected = [OpToken('-'), FloatToken(2), OpToken('^'),
                    FloatToken(3)]
        assert parser.tokenize(list_) == expected
    
    def test_paren_neg_x_pow_2(self):
        parser = Parser()
        list_ = ['(', '-', 'x', ')', '^', '2']
        expected = [ParenToken('('), OpToken('-'), VarToken('x'),
                    ParenToken(')'), OpToken('^'), FloatToken(2)]
        assert parser.tokenize(list_) == expected

    def test_complex_const(self):
        parser = Parser()
        list_ = ['4 ', '+', ' 2 ', '*', ' ', '-', '8.2', '^', '42',
                  ' ', '/', ' 9']
        expected = [FloatToken(4), OpToken('+'), FloatToken(2),
                    OpToken('*'), OpToken('-'), FloatToken(8.2),
                    OpToken('^'), FloatToken(42), OpToken('/'),
                    FloatToken(9)]
        output = parser.tokenize(list_)
        assert output == expected

    def test_complex_var(self):
        parser = Parser()
        list_ = ['x ', '+', ' 2 ', '*', ' ', '-', 'y', '^', '42 ', '/', ' 9']
        expected = [VarToken('x'), OpToken('+'), FloatToken(2), OpToken('*'),
                    OpToken('-'), VarToken('y'), OpToken('^'), FloatToken(42),
                    OpToken('/'), FloatToken(9)]
        assert parser.tokenize(list_) == expected
    
    def test_parentheses(self):
        parser = Parser()
        list_ = ['(', '(', '64. 2', '+', 'x', ')', ')']
        expected = [ParenToken('('), ParenToken('('), FloatToken(64.2),
                    OpToken('+'), VarToken('x'), ParenToken(')'),
                    ParenToken(')')]
        assert parser.tokenize(list_) == expected


@pytest.mark.unit
class TestTokensToInfix(object):
    def test_empty(self):
        parser = Parser()
        tokens = []
        expected = []
        assert parser.tokens_to_infix(tokens) == expected
    
    def test_4_plus_2(self):
        parser = Parser()
        tokens = [FloatToken(4), OpToken('+'), FloatToken(2)]
        expected = [FloatToken(4), OpToken('+'), FloatToken(2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected

    def test_pos_2(self):
        parser = Parser()
        tokens = [OpToken('+'), FloatToken(2)]
        expected = [FloatToken(2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_2(self):
        parser = Parser()
        tokens = [OpToken('-'), FloatToken(2)]
        expected = [FloatToken(-2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_x(self):
        parser = Parser()
        tokens = [OpToken('-'), VarToken('x')]
        expected = [VarToken('x', is_neg=True)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_pos_pos_neg_neg_2(self):
        parser = Parser()
        tokens = [OpToken('+'), OpToken('+'), OpToken('-'), OpToken('-'),
                  FloatToken(2)]
        expected = [FloatToken(2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_pos_pos_neg_neg_x(self):
        parser = Parser()
        tokens = [OpToken('+'), OpToken('+'), OpToken('-'), OpToken('-'),
                  VarToken('x')]
        expected = [VarToken('x')]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_4_plus_neg_2(self):
        parser = Parser()
        tokens = [FloatToken(4), OpToken('+'), OpToken('-'), FloatToken(2)]
        expected = [FloatToken(4), OpToken('+'), FloatToken(-2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_4_plus_pos_2(self):
        parser = Parser()
        tokens = [FloatToken(4), OpToken('+'), OpToken('+'), FloatToken(2)]
        expected = [FloatToken(4), OpToken('+'), FloatToken(2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_4_plus_pos_neg_neg_2(self):
        parser = Parser()
        tokens = [FloatToken(4), OpToken('+'), OpToken('+'), OpToken('-'),
                  OpToken('-'), FloatToken(2)]
        expected = [FloatToken(4), OpToken('+'), FloatToken(2)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_2_pow_3(self):
        parser = Parser()
        tokens = [OpToken('-'), FloatToken(2), OpToken('^'), FloatToken(3)]
        expected = [FloatToken(-1), OpToken('*'), FloatToken(2), OpToken('^'),
                    FloatToken(3)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_2_pow_neg_3(self):
        parser = Parser()
        tokens = [FloatToken(2), OpToken('^'), OpToken('-'), FloatToken(3)]
        expected = [FloatToken(2), OpToken('^'), FloatToken(-3)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_paren_3(self):
        parser = Parser()
        tokens = [OpToken('-'), ParenToken('('), FloatToken(3), ParenToken(')')]
        expected = [FloatToken(-1), OpToken('*'), ParenToken('('),
                    FloatToken(3), ParenToken(')')]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_2_pow_neg_3(self):
        parser = Parser()
        tokens = [OpToken('-'), FloatToken(2), OpToken('^'), OpToken('-'),
                  FloatToken(3)]
        expected = [FloatToken(-1), OpToken('*'), FloatToken(2), OpToken('^'),
                    FloatToken(-3)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_paren_neg_2_pow_3(self):
        parser = Parser()
        tokens = [ParenToken('('), OpToken('-'), FloatToken(2),
                  ParenToken(')'),OpToken('^'), FloatToken(3)]
        expected = [ParenToken('('), FloatToken(-2), ParenToken(')'),
                    OpToken('^'), FloatToken(3)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_2_pow_neg_3_plus_1(self):
        parser = Parser()
        tokens = [OpToken('-'), FloatToken(2), OpToken('^'), OpToken('-'),
                  FloatToken(3), OpToken('+'), FloatToken(1)]
        expected = [FloatToken(-1), OpToken('*'), FloatToken(2), OpToken('^'),
                    FloatToken(-3), OpToken('+'), FloatToken(1)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_neg_2_pow_neg_x_plus_1(self):
        parser = Parser()
        tokens = [OpToken('-'), FloatToken(2), OpToken('^'), OpToken('-'),
                  VarToken('x'), OpToken('+'), FloatToken(1)]
        expected = [FloatToken(-1), OpToken('*'), FloatToken(2), OpToken('^'),
                    VarToken('x', is_neg=True), OpToken('+'), FloatToken(1)]
        output = parser.tokens_to_infix(tokens)
        assert output == expected
    
    def test_unclosed_paren(self):
        parser = Parser()
        tokens = [ParenToken('('), FloatToken(2)]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)
    
    def test_unopened_paren(self):
        parser = Parser()
        tokens = [FloatToken(2), ParenToken(')')]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)
    
    def test_unopened_and_unclosed_paren(self):
        parser = Parser()
        tokens = [ParenToken(')'), FloatToken(2), ParenToken('(')]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)
    
    def test_empty_paren(self):
        parser = Parser()
        tokens = [ParenToken('('), ParenToken(')')]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)

    def test_leading_operator(self):
        parser = Parser()
        tokens = [OpToken('*'), FloatToken(2)]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)

    def test_trailing_operator(self):
        parser = Parser()
        tokens = [FloatToken(2), OpToken('*')]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)
    
    def test_2_times_pow_2(self):
        parser = Parser()
        tokens = [FloatToken(2), OpToken('*'), OpToken('^'), FloatToken(2)]
        with pytest.raises(ParserError):
            parser.tokens_to_infix(tokens)


@pytest.mark.unit
class TestInfixToPostfix(object):
    def test_empty(self):
        parser = Parser()
        infix = []
        expected = []
        output = parser.infix_to_postfix(infix)
        assert output == expected

    def test_4_plus_2(self):
        """
        infix = 4 + 2
        expected = 4 2 +
        """
        parser = Parser()
        infix = [FloatToken(4), OpToken('+'), FloatToken(2)]
        expected = [Operand(value=4.0), Operand(value=2.0), AddOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected

    def test_4_plus_x(self):
        """
        infix = 4 + x
        expected = 4 x +
        """
        parser = Parser()
        infix = [FloatToken(4), OpToken('+'), VarToken('x')]
        expected = [Operand(value=4), Operand(is_x=True), AddOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected
    
    def test_4_plus_neg_x(self):
        """
        infix = 4 + [-x]
        expected = 4 [-x] +
        """
        parser = Parser()
        infix = [FloatToken(4), OpToken('+'), VarToken('x', is_neg=True)]
        expected = [Operand(value=4), Operand(is_neg_x=True), AddOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected
    
    def test_4_plus_y(self):
        """
        infix = 4 + y
        expected: unknown symbol
        """
        parser = Parser()
        infix = [FloatToken(4), OpToken('+'), VarToken('y')]
        
        with pytest.raises(ParserError):
            parser.infix_to_postfix(infix)
        
    def test_4_plus_2_minus_1(self):
        """
        infix = 4 + 2 - 1
        expected = 4 2 + 1 -
        """
        parser = Parser()
        infix = [FloatToken(4.0), OpToken('+'), FloatToken(2.0), OpToken('-'),
                 FloatToken(1.0)]
        expected = [Operand(value=4.0), Operand(value=2.0), AddOperator(),
                    Operand(value=1.0), SubOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected

    def test_4_plus_2_times_1(self):
        """
        infix = 4 + 2 * 1
        expected = 4 2 1 * +
        """
        parser = Parser()
        infix = [FloatToken(4.0), OpToken('+'), FloatToken(2.0), OpToken('*'),
                 FloatToken(1.0)]
        expected = [Operand(value=4.0), Operand(value=2.0), Operand(value=1.0),
                    MulOperator(), AddOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected

    def test_4_times_2_plus_1(self):
        """
        infix = 4 * 2 + 1
        expected = 4 2 * 1 +
        """
        parser = Parser()
        infix = [FloatToken(4.0), OpToken('*'), FloatToken(2.0), OpToken('+'),
                 FloatToken(1.0)]
        expected = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                    Operand(value=1.0), AddOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected

    def test_paren_3(self):
        """
        infix = (3)
        expected = 3
        """
        parser = Parser()
        infix = [ParenToken('('), FloatToken(3.0), ParenToken(')')]
        expected = [Operand(value=3.0)]
        output = parser.infix_to_postfix(infix)
        assert output == expected
    
    def test_2_times_paren_4_plus_3(self):
        """
        infix = 2*(4+3)
        expected = 2 4 3 + *
        """
        parser = Parser()
        infix = [FloatToken(2.0), OpToken('*'), ParenToken('('),
                 FloatToken(4.0), OpToken('+'), FloatToken(3.0),
                 ParenToken(')')]
        expected = [Operand(value=2.0), Operand(value=4.0), Operand(value=3.0),
                    AddOperator(), MulOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected
    
    def test_2_times_paren_4_plus_3(self):
        """
        infix = 2*(4+3^([-10]/9))+(5/100)
        expected = 2 4 3 [-10] 9 / ^ + * 5 100 / +
        """
        parser = Parser()
        infix = [FloatToken(2.0), OpToken('*'), ParenToken('('),
                 FloatToken(4.0), OpToken('+'), FloatToken(3.0),
                 OpToken('^'), ParenToken('('), FloatToken(-10),
                 OpToken('/'), FloatToken(9), ParenToken(')'),
                 ParenToken(')'), OpToken('+'), ParenToken('('),
                 FloatToken(5), OpToken('/'), FloatToken(100),
                 ParenToken(')')]
        expected = [Operand(value=2), Operand(value=4), Operand(value=3),
                    Operand(value=-10), Operand(value=9), DivOperator(),
                    PowOperator(), AddOperator(), MulOperator(),
                    Operand(value=5), Operand(value=100), DivOperator(),
                    AddOperator()]
        output = parser.infix_to_postfix(infix)
        assert output == expected


@pytest.mark.unit
class TestPostfixToExprTree(object):
    def test_empty(self):
        parser = Parser()
        postfix = []
        expected = None
        assert parser.postfix_to_expr_tree(postfix) == expected

    def test_4_2_add(self):
        """
        postfix = 4 2 +
        expected:
            +
          4   2
        """

        parser = Parser()

        postfix = [Operand(value=4.0), Operand(value=2.0), AddOperator()]
        expected = ExprTNode(AddOperator(),
                        left=ExprTNode(Operand(value=4.0)),
                        right=ExprTNode(Operand(value=2.0)))
        output = parser.postfix_to_expr_tree(postfix)
        assert output == expected
    
    def test_4_2_mul_1_add(self):
        """
        postfix = 4 2 * 1 +
        expected:
                 +
              *     1
            4   2
        """
        
        parser = Parser()

        postfix = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                   Operand(value=1.0), AddOperator()]
        expected = ExprTNode(AddOperator(),
                        left=ExprTNode(MulOperator(),
                            left=ExprTNode(Operand(value=4.0)),
                            right=ExprTNode(Operand(value=2.0))),
                        right=ExprTNode(Operand(value=1.0)))
        output = parser.postfix_to_expr_tree(postfix)

        assert output == expected

    def test_4_2_1_mul_add(self):
        """
        postfix = 4 2 1 * +
        expected:
                 +
              4     *
                  2   1
        """
        
        parser = Parser()
        postfix = [Operand(value=4.0), Operand(value=2.0), Operand(value=1.0),
                   MulOperator(), AddOperator()]
        expected = ExprTNode(AddOperator(),
                        left=ExprTNode(Operand(value=4.0)),
                        right=ExprTNode(MulOperator(),
                            left=ExprTNode(Operand(value=2.0)),
                            right=ExprTNode(Operand(value=1.0))))
        output = parser.postfix_to_expr_tree(postfix)

        assert output == expected

    def test_4_2_mul_add(self):
        """
        postfix = 4 2 * +
        expected: ParserError
        """
        
        parser = Parser()
        postfix = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                   AddOperator()]
        
        with pytest.raises(ParserError):
            parser.postfix_to_expr_tree(postfix)
    
    def test_4_2_1_add(self):
        """
        postfix = 4 2 1 +
        expected: ParserError
        """
        
        parser = Parser()
        postfix = [Operand(value=4.0), Operand(value=2.0), Operand(value=1.0),
                   AddOperator()]
        
        with pytest.raises(ParserError):
            parser.postfix_to_expr_tree(postfix)

    def test_add_4_2(self):
        """
        postfix = + 4 2
        expected: ParserError
        """
        
        parser = Parser()
        postfix = [AddOperator(), Operand(value=4.0), Operand(value=2.0)]
        
        with pytest.raises(ParserError):
            parser.postfix_to_expr_tree(postfix)


@pytest.mark.unit
class TestParse(object):
    def test_empty(self):
        parser = Parser()
        string = ""
        expected = None

        assert parser.parse(string) == expected

    def test_4_plus_2(self):
        parser = Parser()
        string = "4 + 2"
        expected = ExprTNode(AddOperator(),
                        left=ExprTNode(Operand(value=4.0)),
                        right=ExprTNode(Operand(value=2.0)))
        
        assert parser.parse(string) == expected
    
    def test_4_plus_x(self):
        parser = Parser()
        string = "4 + x"
        expected = ExprTNode(AddOperator(),
                        left=ExprTNode(Operand(value=4.0)),
                        right=ExprTNode(Operand(is_x=True)))
        
        assert parser.parse(string) == expected
    
    def test_4_plus_2_times_1(self):
        parser = Parser()
        string = "4 + 2 * 1"
        expected = ExprTNode(AddOperator(),
                        left=ExprTNode(Operand(value=4.0)),
                        right=ExprTNode(MulOperator(),
                            left=ExprTNode(Operand(value=2.0)),
                            right=ExprTNode(Operand(value=1.0))))
        
        assert parser.parse(string) == expected
    
    def test_4_plus_ParserError(self):
        parser = Parser()
        string = "4 +"

        with pytest.raises(ParserError):
            parser.parse(string)
    
    def test_y_ParserError(self):
        parser = Parser()
        string = "y"

        with pytest.raises(ParserError):
            parser.parse(string)
    
    def test_neg_2(self):
        parser = Parser()
        string = "-2"
        expected = ExprTNode(Operand(value=-2))

        assert parser.parse(string) == expected
    
    def test_4_plus_minus_2(self):
        parser = Parser()
        string = "4+-2"
        expected = ExprTNode(AddOperator(),
                    left=ExprTNode(Operand(value=4)),
                    right=ExprTNode(Operand(value=-2)))

        output = parser.parse(string)
        assert output == expected
    
    def test_4_plus_plus_plus_minus_minus_2(self):
        parser = Parser()
        string = "4+++--2"
        expected = ExprTNode(AddOperator(),
                    left=ExprTNode(Operand(value=4.0)),
                    right=ExprTNode(Operand(value=2.0)))

        assert parser.parse(string) == expected
