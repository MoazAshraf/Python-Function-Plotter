## The main widget contains the whole user interface and is the widget directly
## rendered by the application. Represents the view (passive) in the MVP
## architecture.

from PySide2 import QtCore
from PySide2.QtCore import Slot, Signal, QLocale
from PySide2.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QPushButton,
    QLayout, QVBoxLayout, QHBoxLayout,
    QSizePolicy
    )
from PySide2.QtGui import QDoubleValidator
from .mplwidget import MplCanvasWidget


class CustomWidget(QWidget):
    """
    Helper widget base class used to add UI elements with the same style to
    avoid writing too much boilerplate code.
    """

    def __init__(self, layout, *args, **kwargs):
        """
        Parameters
        ----------
        layout : QLayout
            The layout to use for this widget
        """

        super().__init__(*args, **kwargs)

        self.layout = layout
        self.setLayout(self.layout)

    def _add_label(self, text=""):
        self.x_min_label = QLabel(text)
        self.layout.addWidget(self.x_min_label)

    def _add_line_edit(self, text=""):
        lineedit = QLineEdit(text)
        lineedit.setMaximumHeight(28)
        lineedit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        lineedit.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(lineedit)
        return lineedit
    
    def _add_float_line_edit(self, text="0",
            min_val=float('-inf'), max_val=float('inf'), decimals=100):
        validator = QDoubleValidator(min_val, max_val, decimals)
        validator.setLocale(QLocale.English)
        numedit = self._add_line_edit(text)
        numedit.setValidator(validator)
        return numedit

    def _add_text_edit(self, text=""):
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


class AxisRangeWidget(CustomWidget):
    """
    The X min and max inputs widget
    """

    def __init__(self, *args, **kwargs):
        super().__init__(QHBoxLayout(), *args, **kwargs)

        self.x_min_label = self._add_label("X Min:")
        self.x_min_input = self._add_float_line_edit()

        self.x_max_label = self._add_label("X Max:")
        self.x_max_input = self._add_float_line_edit("1")
    
    def get_x_values(self):
        """
        Reads the x range values as floats
        
        Returns
        -------
        x_min : float
            The value of the x min input
        x_max : float
            The value of the x max input
        
        Raises
        ------
        ValueError
            User entered a string that doesn't represent a float
        """

        try:
            x_min = float(self.x_min_input.text())
        except ValueError:
            raise ValueError("X Min must be a number")

        try:
            x_max = float(self.x_max_input.text())
        except ValueError:
            raise ValueError("X Max must be a number")

        return x_min, x_max


class FunctionWidget(CustomWidget):
    """
    The widget containing the function text input and the plot button
    """

    def __init__(self, *args, **kwargs):
        super().__init__(QHBoxLayout(), *args, **kwargs)

        self.func_label = self._add_label("f(x) = ")

        self.func_input = self._add_line_edit()
        self.func_input.setPlaceholderText("e.g. x^2")

        self.plot_button = self._add_button("Plot")


class MainWidget(QWidget):
    """
    The main widget rendered directly by the application. It contains:
    - Axis range widget
    - Range error label
    - Matplotlib widget
    - Function widget
    - Syntax error label
    """

    # define signals
    on_plot = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the main layout (vertical)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # axis range widget
        self.axis_range_widget = AxisRangeWidget()
        self.axis_range_widget.setMaximumWidth(320)
        self.layout.addWidget(self.axis_range_widget,
            alignment=QtCore.Qt.AlignHCenter)
        
        # range error message widget
        self.range_error_label = QLabel()
        self.range_error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.range_error_label.setVisible(False)
        self.range_error_label.setStyleSheet("color: red")
        self.layout.addWidget(self.range_error_label)

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

        # syntax error message widget
        self.syntax_error_label = QLabel()
        self.syntax_error_label.setAlignment(QtCore.Qt.AlignCenter)
        self.syntax_error_label.setVisible(False)
        self.syntax_error_label.setStyleSheet("color: red")
        self.layout.addWidget(self.syntax_error_label)

        # connect signals to slots
        self.func_widget.plot_button.clicked.connect(self._on_plot_button_clicked)
    
    @Slot()
    def _on_plot_button_clicked(self):
        self.on_plot.emit()
    
    def get_input_string(self):
        """
        Returns
        -------
        func_text : str
            The function input text
        """

        return self.func_widget.func_input.text()
    
    def get_x_range(self):
        """
        Reads the x range values as floats
        
        Returns
        -------
        x_min : float
            The value of the x min input
        x_max : float
            The value of the x max input
        """

        return self.axis_range_widget.get_x_values()

    def update_range_error_message(self, string=""):
        """
        Updates the range error message label. If the string is empty, makes the
        message invisible.

        Parameters
        ----------
        string : str
            Defaults to ""
        """

        self.range_error_label.setText(string)
        self.range_error_label.setVisible(True if string else False)

    def update_syntax_error_message(self, string=""):
        """
        Updates the syntax error message label. If the string is empty, makes the
        message invisible.

        Parameters
        ----------
        string : str
            Defaults to ""
        """

        self.syntax_error_label.setText(string)
        self.syntax_error_label.setVisible(True if string else False)
    
    def render_plot(self, x, y):
        """
        Renders the plot provided by the x and y values

        Parameters
        ----------
        x : numpy.ndarray
            The x values of the points to plot
        y : numpy.ndarray
            The y values of the points to plot
        """

        self.plot_widget.render_plot(x, y)
