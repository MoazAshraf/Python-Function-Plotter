from plotter.expression import *


class TestOperandEquality(object):
    def test_float(self):
        assert Operand(value=4.0) == Operand(value=4.0)

    def test_x_and_float(self):
        assert Operand(is_x=True) != Operand(value=4.0)

    def test_float_and_x(self):
        assert Operand(value=4.0) != Operand(is_x=True)

    def test_x_and_x(self):
        assert Operand(is_x=True) == Operand(is_x=True)


class TestTreeEquality(object):
    def test_equal(self):
        tree_a = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        tree_b = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        assert tree_a == tree_b
    
    def test_keys_different(self):
        tree_a = TreeNode(SubOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        tree_b = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        assert tree_a != tree_b
    
    def test_right_different(self):
        tree_a = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=3.0)))
        
        tree_b = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        assert tree_a != tree_b
    
    def test_left_different(self):
        tree_a = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=1.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        tree_b = TreeNode(AddOperator(),
                 left=TreeNode(Operand(value=4.0)),
                 right=TreeNode(Operand(value=2.0)))
        
        assert tree_a != tree_b

