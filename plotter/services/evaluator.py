## The evaluator service validates the given min and max x-values, generates
## x-values and uses the given expression tree to generate the y-values. It is
## part of the application domain model in the MVP architecture.

import numpy as np
from ..util import EvaluationError


class XRangeError(Exception):
    pass


class Evaluator(object):
    def __init__(self):
        pass
    
    def evaluate(self, tree, x_min, x_max, x_tick_frequency=1000):
        """
        Evaluates the given expression tree on the given x range with the given
        tick frequency (defaults to 1000).

        Returns x and y numpy arrays in a tuple
        """

        if x_max <= x_min:
            raise XRangeError("X Max must be greater than X Min")

        x = np.linspace(x_min, x_max, 1000)
        y = tree.evaluate(x)
        return x, y