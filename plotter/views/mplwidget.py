## The Matplotlib canvas widget responsible for rendering the plot.

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvasWidget(FigureCanvas):
    """
    Matplotlib Canvas Widget
    """

    # FigureCanvas inherits from QtWidget
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # create the figure and axes used for plotting
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(1, 1, 1)
        self.set_labels()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)
    
    def render_plot(self, x, y):
        """
        Renders the plot provided by the x and y values

        Parameters
        ----------
        x : numpy.ndarray
            The x values of the points to plot
        y : numpy.ndarray
            The y values of the points to plot
        """
        
        x_min, x_max = x[0], x[-1]
        self.axes.cla()
        self.axes.set_xlim(x_min, x_max)
        self.set_labels()
        self.axes.plot(x, y)
        self.draw()
    
    def set_labels(self):
        """
        Sets the x and y axis labels
        """

        self.axes.set_xlabel("x")
        self.axes.set_ylabel("f(x)")
