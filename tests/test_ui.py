from PySide2 import QtCore
from pytestqt import qtbot
from main import create_mvp


def test_plot(qtbot):
    # create the MVP components and the qtbot instance
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    plot_button = main_widget.func_widget.plot_button
    message_label = main_widget.message_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("x^2")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert not message_label.isVisible()
    assert plot_widget.axes.lines   # check if there's a plot

def test_unexpected_operator(qtbot):
    # create the MVP components and the qtbot instance
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    plot_button = main_widget.func_widget.plot_button
    message_label = main_widget.message_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("x^")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert message_label.isVisible()
    assert message_label.text().startswith("Unexpected operator")
    assert not plot_widget.axes.lines   # check if there's no plot

def test_unknown_symbol(qtbot):
    # create the MVP components and the qtbot instance
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    plot_button = main_widget.func_widget.plot_button
    message_label = main_widget.message_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("y")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert message_label.isVisible()
    assert message_label.text().startswith("Unknown symbol")
    assert not plot_widget.axes.lines   # check if there's no plot