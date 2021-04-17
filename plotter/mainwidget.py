## The main widget contains the whole user interface and is the widget directly
## rendered by the application

from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        # simple label
        self.label = QLabel("Main Widget")

        # use a vertical box layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)
        self.setLayout(self.layout)