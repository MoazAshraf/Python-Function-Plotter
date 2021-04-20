## Implementation of the Presenter in the MVP pattern. It does the following:
## - Observes changes to the view (MainWidget)
## - Invokes the Parser service to generate the expression tree
## - Invokes the Plotter service to evaluate the expression tree based on the
##   x min and max values
## - Updates the view to show the plot, or error messages

from PySide2.QtCore import Slot
from .util import EvaluationError
from .services.parser import ParserError
from .services.plotter import XRangeError


class Presenter(object):
    def __init__(self, services, views):
        self.services = services
        self.views = views

        self.parser = self.services['parser']
        self.plotter = self.services['plotter']

        # connect view signals to presenter slots
        self.main_widget = views['main_widget']
        self.main_widget.on_plot.connect(self.on_plot)
    
    @Slot()
    def on_plot(self):
        """
        This slot is connected to the view's on_plot signal.
        """

        error = False
        self.main_widget.update_syntax_error_message()
        self.main_widget.update_range_error_message()
        
        func_string = self.main_widget.get_input_string()
        try:
            x_min, x_max = self.main_widget.get_x_range()
        except ValueError as e:
            self.main_widget.update_range_error_message(str(e))
        else:
            try:
                self.plotter.validate_x_range(x_min, x_max)
            except XRangeError as e:
                self.main_widget.update_range_error_message(str(e))
                error = True

            try:
                # parse
                func_expr = self.parser.parse(func_string)
            except ParserError as e:
                self.main_widget.update_syntax_error_message(str(e))
                error = True
        
            if not error and func_expr is not None:
                # plot and render
                x, y = self.plotter.plot(func_expr, x_min, x_max)
                self.main_widget.render_plot(x, y)
