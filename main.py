## The entry point of the program that runs to start the application

import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel
from plotter.views.mainwidget import MainWidget
from plotter.services.parser import Parser
from plotter.services.evaluator import Evaluator
from plotter.presenter import Presenter

def create_mvp():
    """
    Create instances of the services, views and presenter and returns them
    """

    # services
    parser = Parser()
    evaluator = Evaluator()
    services = {"parser": parser, "evaluator": evaluator}

    # views
    widget = MainWidget()
    size = (640, 640)
    widget.setMinimumSize(*size)
    widget.resize(*size)
    widget.setWindowTitle("Function Plotter")
    views = {"main_widget": widget}

    # create the presenter
    presenter = Presenter(services, views)

    return services, views, presenter

if __name__ == "__main__":
    # create the Qt application
    app = QApplication([])

    # MVP components
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()

    # run the main Qt loop
    sys.exit(app.exec_())