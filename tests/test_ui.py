from PySide2 import QtCore
from pytestqt import qtbot
from plotter.views.mainwidget import MainWidget
from plotter.controller import Controller
from plotter.services.parser import Parser
from main import create_mvc


def test_plot(qtbot):
    # create the MVC components and the qtbot instance
    parser, widget, controller = create_mvc()
    widget.show()   # show widget to test label visibility
    qtbot.addWidget(widget)

    # aliases for ui elements
    func_input = widget.func_widget.func_input
    plot_button = widget.func_widget.plot_button
    message_label = widget.message_label
    plot_widget = widget.plot_widget

    # user interaction
    func_input.setText("x^2")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert not message_label.isVisible()
    assert plot_widget.axes.lines   # check if there's a plot

def test_unexpected_operator(qtbot):
    # create the MVC components and the qtbot instance
    parser, widget, controller = create_mvc()
    widget.show()   # show widget to test label visibility
    qtbot.addWidget(widget)

    # aliases for ui elements
    func_input = widget.func_widget.func_input
    plot_button = widget.func_widget.plot_button
    message_label = widget.message_label
    plot_widget = widget.plot_widget

    # user interaction
    func_input.setText("x^")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert message_label.isVisible()
    assert message_label.text().startswith("Unexpected operator")
    assert not plot_widget.axes.lines   # check if there's no plot

def test_unknown_symbol(qtbot):
    # create the MVC components and the qtbot instance
    parser, widget, controller = create_mvc()
    widget.show()   # show widget to test label visibility
    qtbot.addWidget(widget)

    # aliases for ui elements
    func_input = widget.func_widget.func_input
    plot_button = widget.func_widget.plot_button
    message_label = widget.message_label
    plot_widget = widget.plot_widget

    # user interaction
    func_input.setText("y")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert message_label.isVisible()
    assert message_label.text().startswith("Unknown symbol")
    assert not plot_widget.axes.lines   # check if there's no plot