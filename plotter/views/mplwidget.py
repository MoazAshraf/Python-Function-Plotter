## The matplotlib canvas widget.

import numpy as np
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvasWidget(FigureCanvas):
    # FigureCanvas inherits from QtWidget
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # create the figure and axes used for plotting
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(1, 1, 1)
        self.set_labels()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)
    
    def plot(self, x, y, x_min, x_max):
        self.axes.cla()
        self.axes.set_xlim(x_min, x_max)
        self.set_labels()
        self.axes.plot(x, y)
        self.draw()
    
    def set_labels(self):
        self.axes.set_xlabel("x")
        self.axes.set_ylabel("f(x)")
