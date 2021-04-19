## The entry point of the program that runs to start the application

import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel
from plotter.views.mainwidget import MainWidget
from plotter.services.parser import Parser
from plotter.controller import Controller

def create_mvc():
    # create and show the main widget (view)
    widget = MainWidget()
    size = (640, 640)
    widget.setMinimumSize(*size)
    widget.resize(*size)
    widget.setWindowTitle("Function Plotter")

    # create an instance of the function parser service
    parser = Parser()

    # create the controller
    controller = Controller(parser, widget)

    return parser, widget, controller

if __name__ == "__main__":
    # create the Qt application
    app = QApplication([])

    # MVC components
    parser, widget, controller = create_mvc()
    widget.show()

    # run the main Qt loop
    sys.exit(app.exec_())