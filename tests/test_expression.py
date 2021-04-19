import pytest
import numpy as np
from plotter.models.expression import *


class TestOperandEquality(object):
    def test_float(self):
        assert Operand(value=4.0) == Operand(value=4.0)

    def test_x_and_float(self):
        assert Operand(is_x=True) != Operand(value=4.0)

    def test_float_and_x(self):
        assert Operand(value=4.0) != Operand(is_x=True)
    
    def test_neg_x_and_float(self):
        assert Operand(is_neg_x=True) != Operand(value=4.0)

    def test_x_and_x(self):
        assert Operand(is_x=True) == Operand(is_x=True)
    
    def test_x_and_neg_x(self):
        assert Operand(is_x=True) != Operand(is_neg_x=True)
    
    def test_neg_x_and_x(self):
        assert Operand(is_neg_x=True) != Operand(is_x=True)
    
    def test_neg_x_and_neg_x(self):
        assert Operand(is_neg_x=True) == Operand(is_neg_x=True)


class TestExprTNodeEquality(object):
    def test_equal(self):
        tree_a = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        tree_b = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        assert tree_a == tree_b
    
    def test_keys_different(self):
        tree_a = ExprTNode(SubOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        tree_b = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        assert tree_a != tree_b
    
    def test_right_different(self):
        tree_a = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=3.0)))
        
        tree_b = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        assert tree_a != tree_b
    
    def test_left_different(self):
        tree_a = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=1.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        tree_b = ExprTNode(AddOperator(),
                 left=ExprTNode(Operand(value=4.0)),
                 right=ExprTNode(Operand(value=2.0)))
        
        assert tree_a != tree_b


class TestExprTreeEvaluate(object):
    def test_4_plus_2(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=4.0)),
                right=ExprTNode(Operand(value=2.0)))
        
        result = tree.evaluate()
        expected = 6.0
        assert result == expected
    
    def test_4_plus_neg_2(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=4.0)),
                right=ExprTNode(Operand(value=-2.0)))
        
        result = tree.evaluate()
        expected = 2.0
        assert result == expected
    
    def test_4_plus_x(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=4.0)),
                right=ExprTNode(Operand(is_x=True)))
        
        assert tree.evaluate(x=2.0) == (4.0 + 2.0)
        assert tree.evaluate(x=-2.0) == (4.0 + (-2.0))
        assert tree.evaluate(x=100.0) == (4.0 + 100.0)
    
    def test_4_plus_neg_x(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=4.0)),
                right=ExprTNode(Operand(is_neg_x=True)))
        
        assert tree.evaluate(x=2.0) == (4.0 + -2.0)
        assert tree.evaluate(x=-2.0) == (4.0 + -(-2.0))
        assert tree.evaluate(x=100.0) == (4.0 + -100.0)

    def test_4_plus_exception(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=4.0)))
        
        with pytest.raises(Exception):
            tree.evaluate()
    
    def test_4_plus_2_times_3(self):
        """
           +
        4     *
            2   3
        """

        tree = ExprTNode(AddOperator(),
                            left=ExprTNode(Operand(value=4.0)),
                            right=ExprTNode(MulOperator(),
                                left=ExprTNode(Operand(value=2.0)),
                                right=ExprTNode(Operand(value=3.0))))

        expected = 10
        assert tree.evaluate() == expected

    def test_x_plus_2_times_x(self):
        """
           +
        x     *
            2   x
        """

        tree = ExprTNode(AddOperator(),
                            left=ExprTNode(Operand(is_x=True)),
                            right=ExprTNode(MulOperator(),
                                left=ExprTNode(Operand(value=2.0)),
                                right=ExprTNode(Operand(is_x=True))))

        assert tree.evaluate(x=2.0) == (2.0 + 2.0 * 2.0)
        assert tree.evaluate(x=-2.0) == ((-2.0) + 2.0 * (-2.0))
        assert tree.evaluate(x=100.0) == (100.0 + 2.0 * 100.0)
    
    def test_const_nparray_plus_const_nparray(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=np.array([1, 2, 3]))),
                right=ExprTNode(Operand(value=np.array([4, 5, 6]))))
        
        result = tree.evaluate()
        expected = np.array([1, 2, 3]) + np.array([4, 5, 6])
        assert (result == expected).all()
    
    def test_const_nparray_plus_x(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=np.array([1, 2, 3]))),
                right=ExprTNode(Operand(is_x=True)))

        assert (tree.evaluate(x=2.0) == (np.array([1, 2, 3]) + 2.0)).all()
        assert (tree.evaluate(x=-2.0) == (np.array([1, 2, 3]) + (-2.0))).all()
        assert (tree.evaluate(x=100.0) == (np.array([1, 2, 3]) + (100.0))).all()
    
    def test_const_nparray_plus_neg_x(self):
        tree = ExprTNode(AddOperator(),
                left=ExprTNode(Operand(value=np.array([1, 2, 3]))),
                right=ExprTNode(Operand(is_neg_x=True)))

        assert (tree.evaluate(x=2.0) == (np.array([1, 2, 3]) - 2.0)).all()
        assert (tree.evaluate(x=-2.0) == (np.array([1, 2, 3]) - (-2.0))).all()
        assert (tree.evaluate(x=100.0) == (np.array([1, 2, 3]) - (100.0))).all()