## The plotter service validates the given min and max x-values, generates
## x-values and uses the given expression tree to generate the y-values. It is
## part of the application domain model in the MVP architecture.

import numpy as np


class XRangeError(Exception):
    pass


class Plotter(object):
    """
    Represents a Plotter service. The Plotter validates the x range, generates
    valid x-values and evaluates the give expression to get the y-values.
    """
    
    def validate_x_range(self, x_min, x_max):
        """
        Validates the x range and raises an XRangeError if invalid.

        Parameters
        ----------
        x_min : float
            The minimum value of x
        x_max : float
            The maximum value of x
        
        Raises
        ------
        XRangeError
            Invalid range
        """

        if x_max <= x_min:
            raise XRangeError("X Max must be greater than X Min")

    def plot(self, tree, x_min, x_max, x_tick_frequency=1000):
        """
        Plots the expression on the given x range.

        Parameters
        ----------
        tree : ExprTNode
            The expression representing the function to plot
        x_min : float
            The minimum value of x
        x_max : float
            The maximum value of x
        x_tick_frequency : int
            The tick frequency of the x-axis, i.e. how many points to plot
        
        Returns
        -------
        x : numpy.ndarray
            The x values of the points
        y : numpy.ndarray
            The y values of the points
        
        Raises
        ------
        XRangeError
            Invalid range
        """

        self.validate_x_range(x_min, x_max)

        x = np.linspace(x_min, x_max, 1000)
        y = tree.evaluate(x)
        return x, y