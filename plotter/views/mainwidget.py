## The main widget contains the whole user interface and is the widget directly
## rendered by the application. Represents the View in the MVC pattern.

import numpy as np
from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import (
    QWidget, QLabel, QTextEdit, QPushButton,
    QLayout, QVBoxLayout, QHBoxLayout,
    QSizePolicy
    )

from ..models.expression import ExprTNode
from .mplwidget import MplCanvasWidget


class CustomHBoxWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

    def _add_label(self, text=""):
        self.x_min_label = QLabel(text)
        self.layout.addWidget(self.x_min_label)

    def _add_text_input(self, text="0"):
        textedit = QTextEdit(text)
        textedit.setMaximumHeight(28)
        textedit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        textedit.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(textedit)
        return textedit
    
    def _add_button(self, text):
        button = QPushButton(text)
        self.layout.addWidget(button)
        return button


class FunctionWidget(CustomHBoxWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.func_label = self._add_label("f(x) = ")

        self.func_input = self._add_text_input()
        self.func_input.setPlaceholderText("e.g. x^2")

        self.plot_button = self._add_button("Plot")


class MainWidget(QWidget):
    # define signals
    on_plot = Signal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the main layout (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # matplotlib canvas widget
        self.plot_widget = MplCanvasWidget()
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding)
        self.layout.addWidget(self.plot_widget)

        # function input widget
        self.func_widget = FunctionWidget()
        self.func_widget.setMaximumWidth(640)
        self.layout.addWidget(self.func_widget,
            alignment=QtCore.Qt.AlignHCenter)

        # error message widget
        self.message_label = QLabel()
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setVisible(False)
        self.message_label.setStyleSheet("color: red")
        self.layout.addWidget(self.message_label)

        # connect signals to slots
        self.func_widget.plot_button.clicked.connect(self._on_plot_button_clicked)
    
    @Slot()
    def _on_plot_button_clicked(self):
        x = np.linspace(0, 1, 100)
        self.on_plot.emit(x)
    
    def get_input_string(self):
        """
        Returns the function input string
        """

        return self.func_widget.func_input.toPlainText()

    def update_message(self, string):
        """
        Updates the message label
        """

        self.message_label.setText(string)
        self.message_label.setVisible(True if string else False)
    
    def plot(self, x: np.ndarray, y: np.ndarray):
        """
        Plot the provided x and y values
        """

        self.plot_widget.plot(x, y)