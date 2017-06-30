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
        # box layouts are simplest - vertical and horizontal
        self.setLayout(qw.QVBoxLayout())
        
        # create buttons
        btn_1 = qw.QPushButton('Button 1')
        btn_2 = qw.QPushButton('Button 2')
        btn_3 = qw.QPushButton('Button 3')
        btn_4 = qw.QPushButton('Button 4')
        btn_5 = qw.QPushButton('Button 5')
        
        # add to layout, they'll be spaced evenly vertically in the layout
        self.layout().addWidget(btn_1)
        self.layout().addWidget(btn_2)
        self.layout().addWidget(btn_3)
        self.layout().addWidget(btn_4)
        self.layout().addWidget(btn_5)
        
dialog = simple_ui()
dialog.show()