import pytest
import numpy as np
from plotter.services.evaluator import *
from plotter.models.expression import *


class TestEvaluate(object):
    def test_x_squared(self):
        evaluator = Evaluator()
        tree = ExprTNode(PowOperator(),
                         left=ExprTNode(Operand(is_x=True)),
                         right=ExprTNode(Operand(value=2)))
        x_min = -1
        x_max = 1
        freq = 1000
        output = evaluator.evaluate(tree, x_min, x_max, x_tick_frequency=freq)
        output_x, output_y = output
        expected_x = np.linspace(x_min, x_max, freq)
        expected_y = np.power(expected_x, 2)

        assert (output_x == expected_x).all()
        assert (output_y == expected_y).all()
    
    def test_invalid_range(self):
        evaluator = Evaluator()
        tree = ExprTNode(PowOperator(),
                         left=ExprTNode(Operand(is_x=True)),
                         right=ExprTNode(Operand(value=2)))
        x_min = 1
        x_max = -1
        freq = 1000

        with pytest.raises(XRangeError):
            evaluator.evaluate(tree, x_min, x_max, x_tick_frequency=freq)
