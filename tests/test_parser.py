import pytest
from plotter.parser import Parser
from plotter.expression import *


class TestParseToExprList(object):
    def test_empty(self):
        parser = Parser()
        string = ""
        expected = []
        assert parser.parse_to_expr_list(string) == expected

    def test_simple_const(self):
        parser = Parser()
        string = "4 + 2"
        expected = [Operand(value=4.0), AddOperator(), Operand(value=2.0)]
        assert parser.parse_to_expr_list(string) == expected

    def test_complex_const(self):
        parser = Parser()
        string = "4 + 2 * -8.2^42 / 9"
        expected = [Operand(value=4.0), AddOperator(), Operand(value=2.0),
                    MulOperator(), SubOperator(), Operand(value=8.2), PowOperator(),
                    Operand(value=42), DivOperator(), Operand(value=9)]
        assert parser.parse_to_expr_list(string) == expected

    def test_complex_x(self):
        parser = Parser()
        string = "x + 2 * -x^42 / 9"
        expected = [Operand(is_x=True), AddOperator(), Operand(value=2.0),
                    MulOperator(), SubOperator(), Operand(is_x=True), PowOperator(),
                    Operand(value=42), DivOperator(), Operand(value=9)]
        assert parser.parse_to_expr_list(string) == expected

    def test_unknown(self):
        parser = Parser()
        string = "y + 2 * -y^42 / 9"
        with pytest.raises(ValueError):
            parser.parse_to_expr_list(string)
    

class TestInfixToPostfix(object):
    def test_empty(self):
        parser = Parser()
        infix = []
        expected = []
        assert parser.infix_to_postfix(infix) == expected

    def test_add(self):
        """
        infix = 4 + 2
        expected = 4 2 +
        """
        parser = Parser()
        infix = [Operand(value=4.0), AddOperator(), Operand(value=2.0)]
        expected = [Operand(value=4.0), Operand(value=2.0), AddOperator()]
        assert parser.infix_to_postfix(infix) == expected

    def test_add_sub(self):
        """
        infix = 4 + 2 - 1
        expected = 4 2 + 1 -
        """
        parser = Parser()
        infix = [Operand(value=4.0), AddOperator(), Operand(value=2.0),
                 SubOperator(), Operand(value=1.0)]

        expected = [Operand(value=4.0), Operand(value=2.0), AddOperator(),
                    Operand(value=1.0), SubOperator()]
        assert parser.infix_to_postfix(infix) == expected

    def test_add_mul(self):
        """
        infix = 4 + 2 * 1
        expected = 4 2 1 * +
        """
        parser = Parser()
        infix = [Operand(value=4.0), AddOperator(), Operand(value=2.0),
                 MulOperator(), Operand(value=1.0)]

        expected = [Operand(value=4.0), Operand(value=2.0), Operand(value=1.0),
                    MulOperator(), AddOperator()]
        assert parser.infix_to_postfix(infix) == expected

    def test_mul_add(self):
        """
        infix = 4 * 2 + 1
        expected = 4 2 * 1 +
        """
        parser = Parser()
        infix = [Operand(value=4.0), MulOperator(), Operand(value=2.0),
                 AddOperator(), Operand(value=1.0)]

        expected = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                    Operand(value=1.0), AddOperator()]
        assert parser.infix_to_postfix(infix) == expected

    def test_complex(self):
        """
        infix = 4 * x + 1 - 8^9 / 23 / 9 * 4 - x^3
        expected = 4 x * 1 + 8 9 ^ 23 / 9 / 4 * - x 3 ^ -
        """
        parser = Parser()
        infix = [Operand(value=4.0), MulOperator(), Operand(is_x=True),
                 AddOperator(), Operand(value=1.0), SubOperator(),
                 Operand(value=8.0), PowOperator(), Operand(value=9.0),
                 DivOperator(), Operand(value=23.0), DivOperator(),
                 Operand(value=9.0), MulOperator(), Operand(value=4.0),
                 SubOperator(), Operand(is_x=True), PowOperator(),
                 Operand(value=3.0)]

        expected = [Operand(value=4.0), Operand(is_x=True), MulOperator(),
                    Operand(value=1.0), AddOperator(), Operand(value=8.0),
                    Operand(value=9.0), PowOperator(), Operand(value=23.0),
                    DivOperator(), Operand(value=9.0), DivOperator(),
                    Operand(value=4.0), MulOperator(), SubOperator(),
                    Operand(is_x=True), Operand(value=3.0), PowOperator(),
                    SubOperator()]

        assert parser.infix_to_postfix(infix) == expected

    def test_invalid_1(self):
        """
        infix = 4 * 2 +
        expected = 4 2 * +
        """
        parser = Parser()
        infix = [Operand(value=4.0), MulOperator(), Operand(value=2.0),
                 AddOperator()]

        expected = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                    AddOperator()]
        assert parser.infix_to_postfix(infix) == expected

    def test_invalid_2(self):
        """
        infix = + 4 * 2
        expected = 4 2 * +
        """
        parser = Parser()
        infix = [AddOperator(), Operand(value=4.0), MulOperator(),
                 Operand(value=2.0)]

        expected = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                    AddOperator()]
        assert parser.infix_to_postfix(infix) == expected
    
    def test_invalid_3(self):
        """
        infix = 4 + 2 1
        expected = 4 2 1 +
        """
        parser = Parser()
        infix = [Operand(value=4.0), AddOperator(), Operand(value=2.0),
                 Operand(value=1.0)]

        expected = [Operand(value=4.0), Operand(value=2.0), Operand(value=1.0),
                    AddOperator()]
        assert parser.infix_to_postfix(infix) == expected


class TestPostfixToExprTree(object):
    def test_empty(self):
        parser = Parser()
        postfix = []
        expected = None
        assert parser.postfix_to_expr_tree(postfix) == expected

    def test_add(self):
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
    
    def test_mul_add(self):
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

    def test_add_mul(self):
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

    def test_invalid_1_syntaxerror(self):
        """
        postfix = 4 2 * +
        expected: SyntaxError
        """
        
        parser = Parser()

        postfix = [Operand(value=4.0), Operand(value=2.0), MulOperator(),
                   AddOperator()]
        
        with pytest.raises(SyntaxError):
            parser.postfix_to_expr_tree(postfix)
    
    def test_invalid_2_syntaxerror(self):
        """
        postfix = 4 2 1 +
        expected: SyntaxError
        """
        
        parser = Parser()

        postfix = [Operand(value=4.0), Operand(value=2.0), Operand(value=1.0),
                   AddOperator()]
        
        with pytest.raises(SyntaxError):
            parser.postfix_to_expr_tree(postfix)

    def test_invalid_3_syntaxerror(self):
        """
        postfix = + 4 2
        expected: SyntaxError
        """
        
        parser = Parser()

        postfix = [AddOperator(), Operand(value=4.0), Operand(value=2.0)]
        
        with pytest.raises(SyntaxError):
            parser.postfix_to_expr_tree(postfix)


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
    
    def test_4_plus_syntaxerror(self):
        parser = Parser()
        string = "4 +"

        with pytest.raises(SyntaxError):
            parser.parse(string)
    
    def test_y_valueerror(self):
        parser = Parser()
        string = "y"

        with pytest.raises(ValueError):
            parser.parse(string)
    
    def test_negative_2(self):
        parser = Parser()
        string = "-2"
        expected = ExprTNode(Operand(value=-2.0))

        assert parser.parse(string) == expected
    
    def test_4_plus_negative_2(self):
        parser = Parser()
        string = "4+-2"
        expected = ExprTNode(AddOperator(),
                    left=ExprTNode(Operand(value=4.0)),
                    right=ExprTNode(Operand(value=-2.0)))

        assert parser.parse(string) == expected
    
    def test_4_plus_plus_plus_minus_minus_2(self):
        parser = Parser()
        string = "4+++--2"
        expected = ExprTNode(AddOperator(),
                    left=ExprTNode(Operand(value=4.0)),
                    right=ExprTNode(Operand(value=2.0)))

        assert parser.parse(string) == expected