## Implementation of the Presenter in the MVP pattern. It does the following:
## - Observes changes to the view (MainWidget)
## - Invokes the Parser service to generate the expression tree
## - Invokes the Evaluator service to evaluate the expression tree based on the
##   x min and max values
## - Updates the view to show the plot, or error messages

from PySide2.QtCore import Slot
from .util import EvaluationError
from .services.parser import ParserError
from .services.evaluator import XRangeError


class Presenter(object):
    def __init__(self, services, views):
        self.services = services
        self.views = views

        self.parser = self.services['parser']
        self.evaluator = self.services['evaluator']

        # connect view signals to presenter slots
        self.main_widget = views['main_widget']
        self.main_widget.on_plot.connect(self.on_plot)
    
    @Slot()
    def on_plot(self):
        """
        This slot is connected to the view's on_plot signal.
        """

        func_string = self.main_widget.get_input_string()
        x_min, x_max = self.main_widget.get_x_range()
        
        try:
            # parse
            func_expr = self.parser.parse(func_string)
            if func_expr is not None:
                # validate x range and evaluate
                x, y = self.evaluator.evaluate(func_expr, x_min, x_max)
                # render
                self.main_widget.render_plot(x, y)
            # no errors
            self.main_widget.update_message("")
        except (ParserError, EvaluationError, XRangeError) as e:
            self.main_widget.update_message(str(e))