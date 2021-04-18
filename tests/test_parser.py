import pytest
from plotter.parser import Parser, Operand, Operator


def test_float_operand_equality():
    assert Operand(value=4.0) == Operand(value=4.0)

def test_x_and_float_operand_equality():
    assert Operand(is_x=True) != Operand(value=4.0)

def test_x_and_float_operand_equality():
    assert Operand(value=4.0) != Operand(is_x=True)

def test_x_and_x_operand_equality():
    assert Operand(is_x=True) == Operand(is_x=True)

def test_parse_to_expr_list_simple_const():
    parser = Parser()
    string = "4 + 2"
    expected = [Operand(value=4.0), Operator.ADD, Operand(value=2.0)]
    assert parser.parse_to_expr_list(string) == expected

def test_parse_to_expr_list_complex_const():
    parser = Parser()
    string = "4 + 2 * -8.2^42 / 9"
    expected = [Operand(value=4.0), Operator.ADD, Operand(value=2.0),
                Operator.MUL, Operator.SUB, Operand(value=8.2), Operator.POW,
                Operand(value=42), Operator.DIV, Operand(value=9)]
    assert parser.parse_to_expr_list(string) == expected

def test_parse_to_expr_list_complex_x():
    parser = Parser()
    string = "x + 2 * -x^42 / 9"
    expected = [Operand(is_x=True), Operator.ADD, Operand(value=2.0),
                Operator.MUL, Operator.SUB, Operand(is_x=True), Operator.POW,
                Operand(value=42), Operator.DIV, Operand(value=9)]
    assert parser.parse_to_expr_list(string) == expected

def test_parse_to_expr_list_unknown():
    parser = Parser()
    string = "y + 2 * -y^42 / 9"
    with pytest.raises(ValueError):
        parser.parse_to_expr_list(string)