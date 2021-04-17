## The entry point of the program that runs to start the application

import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    # create the Qt application
    app = QApplication([])

    # create and show the widget placeholder
    label = QLabel("Main Widget Placeholder", alignment=QtCore.Qt.AlignCenter)
    label.resize(600, 400)
    label.setWindowTitle("Function Plotter")
    label.show()

    # run the main Qt loop
    sys.exit(app.exec_())