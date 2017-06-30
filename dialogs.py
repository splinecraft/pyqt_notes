from PySide2 import QtWidgets as qw, QtCore as qc, QtGui as qg
# maya 2017

# for really simple dialogs could create a dialog and call it's functions
"""
dialog = qw.QDialog()
dialog.setWindowTitle('Simple UI')

# keeps dialog window on top of maya interface, depends on OS
dialog.setWindowFlags(qc.Qt.WindowStaysOnTopHint)

# if true doesn't let user interact with main Maya interface
# for "are you sure?" dialogs, etc
# if False behaves like any other window
dialog.setModal(False)

# fixed height/width, can't resize
#dialog.setFixedHeight(250)
dialog.setFixedWidth(300)

# set minimum height, won't resize less than this
dialog.setMinimumHeight(250)

dialog.show()
"""

# usually better to build a class though
# can import this into other modules and have all functionality
class simple_ui(qw.QDialog):
    
    def __init__(self):
        qw.QDialog.__init__(self)

        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setFixedWidth(300)
        
dialog = simple_ui()
dialog.show()