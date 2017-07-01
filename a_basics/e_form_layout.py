from PySide2 import QtWidgets as qw, QtCore as qc, QtGui as qg
# maya 2017

class simple_ui(qw.QDialog):
    
    def __init__(self):
        qw.QDialog.__init__(self)

        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setFixedWidth(300)
        
        # layouts control how widgets go into their parent (the dialog here)
        # form layouts create a list with labels on left and widget on right
        # good for preferences or when you need to fill in items, etc
        self.setLayout(qw.QFormLayout())
        
        # create items
        name_le = qw.QLineEdit()
        email_le = qw.QLineEdit()
        age_le = qw.QSpinBox()
        
        # add to layout, the label for each row will appear next to its widget
        self.layout().addRow('Name', name_le)
        self.layout().addRow('Email', email_le)
        self.layout().addRow('Age', age_le)


dialog = simple_ui()
dialog.show()