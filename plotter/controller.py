## Implementation of the Controller in the MVC pattern. The controller receives
## input events from the View (QWidget). The controller uses a Model (parser)
## to update the view.

from PySide2.QtCore import Slot


class Controller(object):
    def __init__(self, parser, widget):
        self.parser = parser
        self.widget = widget

        ## connect widget signals to controller slots
        self.widget.plot_clicked.connect(self.plot_button_clicked)
    
    @Slot()
    def plot_button_clicked(self):
        func_string = self.widget.get_input_string()

        try:
            self.parser.parse(func_string)
            self.widget.update_message("")
        except (ValueError, SyntaxError) as e:
            self.widget.update_message(str(e))