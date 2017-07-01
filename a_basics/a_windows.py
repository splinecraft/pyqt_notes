from PySide2 import QtWidgets as qw, QtCore as qc, QtGui as qg
# maya 2017

# windows for more extensive applications
window = qw.QMainWindow()

# adds a menubar along the top of the window
menubar = qw.QMenuBar()
menubar.addAction('File')
menubar.addAction('Edit')
menubar.addSeparator()
menubar.addAction('Modify')
window.setMenuBar(menubar)

# toolbar that can be torn off and placed elsewhere within the window
toolbar = qw.QToolBar()
toolbar.addAction('File')
toolbar.addAction('Edit')
toolbar.addSeparator()
toolbar.addAction('Modify')
window.addToolBar(toolbar)

# displays a status message for a given length of time in milliseconds
statusbar = qw.QStatusBar()
statusbar.showMessage('Loading...', 5000)
window.setStatusBar(statusbar)


window.show()

