from PySide2 import QtCore
from pytestqt import qtbot
from main import create_mvp


def test_plot(qtbot):
    # create the MVP components
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    plot_button = main_widget.func_widget.plot_button
    syntax_error_label = main_widget.syntax_error_label
    range_error_label = main_widget.range_error_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("x^2")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert not syntax_error_label.isVisible()
    assert not range_error_label.isVisible()
    assert plot_widget.axes.lines   # check if there's a plot

def test_unexpected_operator(qtbot):
    # create the MVP components
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    plot_button = main_widget.func_widget.plot_button
    syntax_error_label = main_widget.syntax_error_label
    range_error_label = main_widget.range_error_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("x^")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert not range_error_label.isVisible()
    assert syntax_error_label.isVisible()
    assert syntax_error_label.text().startswith("Unexpected operator")
    assert not plot_widget.axes.lines   # check if there's no plot

def test_unknown_symbol(qtbot):
    # create the MVP components
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    plot_button = main_widget.func_widget.plot_button
    syntax_error_label = main_widget.syntax_error_label
    range_error_label = main_widget.range_error_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("y")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert not range_error_label.isVisible()
    assert syntax_error_label.isVisible()
    assert syntax_error_label.text().startswith("Unknown symbol")
    assert not plot_widget.axes.lines   # check if there's no plot

def test_invalid_range(qtbot):
    # create the MVP components
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    x_min_input = main_widget.axis_range_widget.x_min_input
    x_max_input = main_widget.axis_range_widget.x_max_input
    plot_button = main_widget.func_widget.plot_button
    syntax_error_label = main_widget.syntax_error_label
    range_error_label = main_widget.range_error_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("x")
    x_min_input.setText("10")
    x_max_input.setText("0")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert not syntax_error_label.isVisible()
    assert range_error_label.isVisible()
    assert range_error_label.text().startswith("X Max must be greater")
    assert not plot_widget.axes.lines   # check if there's no plot

def test_invalid_range_and_unexpected_operator(qtbot):
        # create the MVP components
    services, views, presenter = create_mvp()
    main_widget = views['main_widget']
    main_widget.show()   # show widget to test label visibility
    qtbot.addWidget(main_widget)

    # aliases for ui elements
    func_input = main_widget.func_widget.func_input
    x_min_input = main_widget.axis_range_widget.x_min_input
    x_max_input = main_widget.axis_range_widget.x_max_input
    plot_button = main_widget.func_widget.plot_button
    syntax_error_label = main_widget.syntax_error_label
    range_error_label = main_widget.range_error_label
    plot_widget = main_widget.plot_widget

    # user interaction
    func_input.setText("x^")
    x_min_input.setText("10")
    x_max_input.setText("0")
    qtbot.mouseClick(plot_button, QtCore.Qt.LeftButton)

    assert syntax_error_label.isVisible()
    assert syntax_error_label.text().startswith("Unexpected operator")
    assert range_error_label.isVisible()
    assert range_error_label.text().startswith("X Max must be greater")
    assert not plot_widget.axes.lines   # check if there's no plot