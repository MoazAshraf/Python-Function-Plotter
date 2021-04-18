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

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)
    
    def plot(self, x, y):
        self.axes.cla()
        self.axes.plot(x, y)
        self.draw()
