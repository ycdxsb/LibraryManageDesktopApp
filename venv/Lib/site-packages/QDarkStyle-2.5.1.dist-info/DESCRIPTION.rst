QDarkStyle is a dark stylesheet for Python and Qt applications.

This module provides a function to transparently load the stylesheets
with the correct rc file.

First, start importing our module

.. code-block:: python

    import qdarkstyle

Then you can get stylesheet provided by QDarkStyle for various Qt wrappers
as shown bellow

.. code-block:: python

    # PySide
    dark_stylesheet = qdarkstyle.load_stylesheet_pyside()
    # PyQt4
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt()
    # PyQt5
    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()

Or from environment variables provided for QtPy or PyQtGraph, see

.. code-block:: python

    # QtPy
    dark_stylesheet = qdarkstyle.load_stylesheet_from_environment()
    # PyQtGraph
    dark_stylesheet = qdarkstyle.load_stylesheet_from_environment(is_pyqtgraph)

Finally, set your QApplication with it

.. code-block:: python

    app.setStyleSheet(dark_stylesheet)

Enjoy!




