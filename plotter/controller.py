## Implementation of the Controller in the MVC pattern. The controller receives
## input events from the View (QWidget). The controller uses a Model (parser)
## to update the view.

import numpy as np
from PySide2.QtCore import Slot


class Controller(object):
    def __init__(self, parser, widget):
        self.parser = parser
        self.widget = widget

        # connect view signals to controller slots
        self.widget.on_plot.connect(self.on_plot)
    
    @Slot(str, np.ndarray)
    def on_plot(self, func_string, x):
        """
        This slot is connected to the view's on_plot signal.
        func_string is the function input text
        x is a numpy array.
        """

        # parse the expression, evaluate at the given x values and give the
        # result to the view
        try:
            func_expr = self.parser.parse(func_string)
            if func_expr is not None:
                y = func_expr.evaluate(x)
                self.widget.plot(x, y)
            self.widget.update_message("")
        except (ValueError, SyntaxError) as e:
            self.widget.update_message(str(e))