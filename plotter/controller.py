## Implementation of the Controller in the MVC pattern. The controller receives
## input events from the View (QWidget). The controller uses a Model (parser)
## to update the view.

from PySide2.QtCore import Slot


class Controller(object):
    def __init__(self, parser, widget):
        self.parser = parser
        self.widget = widget

        ## connect widget signals to controller slots
        self.widget.plot_button.clicked.connect(self.plot_button_clicked)
    
    @Slot()
    def plot_button_clicked(self):
        print("Plot Button Clicked!")