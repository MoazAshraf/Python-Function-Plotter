## The entry point of the program that runs to start the application

import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel
from plotter.mainwidget import MainWidget


if __name__ == "__main__":
    # create the Qt application
    app = QApplication([])

    # create and show the main widget
    widget = MainWidget()
    widget.resize(640, 480)
    widget.setWindowTitle("Function Plotter")
    widget.show()

    # run the main Qt loop
    sys.exit(app.exec_())