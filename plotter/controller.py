## Implementation of the Controller in the MVC pattern. The controller receives
## input events from the View (QWidget). The controller uses a Model (parser)
## to update the view.

class Controller(object):
    def __init__(self, parser, widget):
        self.parser = parser
        self.widget = widget