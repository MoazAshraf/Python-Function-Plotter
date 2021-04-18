## The main widget contains the whole user interface and is the widget directly
## rendered by the application. Represents the View in the MVC pattern.

from PySide2 import QtCore
from PySide2.QtWidgets import (
    QWidget, QLabel, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout,
    QSizePolicy
    )


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        ## create the widgets
        self.plot_widget = QLabel("Plot Widget Placeholder")
        self.func_label = QLabel("f(x) = ")
        self.func_input = QTextEdit()
        self.plot_button = QPushButton("Plot")
        self.message_label = QLabel()

        ## define the layout
        # nested layout for function text input and plot button
        self.input_widget = QWidget()
        self.input_layout = QHBoxLayout()
        self.input_layout.addWidget(self.func_label)
        self.input_layout.addWidget(self.func_input)
        self.input_layout.addWidget(self.plot_button)
        self.input_widget.setLayout(self.input_layout)
        # main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.plot_widget)
        self.layout.addWidget(self.input_widget)
        self.layout.addWidget(self.message_label)
        self.setLayout(self.layout)

        ## alignment and size policies
        # function text input
        self.func_input.setMaximumHeight(28)
        self.func_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.func_input.setAlignment(QtCore.Qt.AlignLeft)
        self.func_input.setPlaceholderText("e.g. x^2")
        # plot widget
        self.plot_widget.setSizePolicy(QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self.plot_widget.setAlignment(QtCore.Qt.AlignCenter)
        # message label
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setVisible(False)
        self.message_label.setStyleSheet("color: red")

        ## give signals names to be used by controller
        self.plot_clicked = self.plot_button.clicked
    
    def get_input_string(self):
        """
        Returns the function input string
        """

        return self.func_input.toPlainText()

    def update_message(self, string):
        """
        Updates the message label
        """

        self.message_label.setText(string)
        self.message_label.setVisible(True if string else False)