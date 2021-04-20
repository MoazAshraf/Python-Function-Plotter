## The plotter service validates the given min and max x-values, generates
## x-values and uses the given expression tree to generate the y-values. It is
## part of the application domain model in the MVP architecture.

import numpy as np


class XRangeError(Exception):
    pass


class Plotter(object):
    def __init__(self):
        pass
    
    def validate_x_range(self, x_min, x_max):
        """
        Validates the x range and raises an XRangeError if invalid
        """

        if x_max <= x_min:
            raise XRangeError("X Max must be greater than X Min")

    def plot(self, tree, x_min, x_max, x_tick_frequency=1000):
        """
        Evaluates the given expression tree on the given x range with the given
        tick frequency (defaults to 1000).

        Returns x and y numpy arrays in a tuple
        """

        self.validate_x_range(x_min, x_max)

        x = np.linspace(x_min, x_max, 1000)
        y = tree.evaluate(x)
        return x, y