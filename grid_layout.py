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
        # grid layouts are like a spreadsheet where there are cells and 
        # you put widgets into them
        self.setLayout(qw.QGridLayout())
        
        # create items - label and lists
        font_names_lb = qw.QLabel('Font')
        font_style_lb = qw.QLabel('Font Style')
        font_size_lb = qw.QLabel('Size')
        
        font_names_list = qw.QListWidget()
        font_names_list.addItem('Times')
        font_names_list.addItem('Palantino')
        font_names_list.addItem('Raleway')
        font_names_list.addItem('Ariel')
        
        font_style_list = qw.QListWidget()
        font_style_list.addItem('Roman')
        font_style_list.addItem('Italic')
        font_style_list.addItem('Oblique')
        
        font_size_list = qw.QListWidget()        
        # build number list using a loop and adding to widget list
        for index in range(10, 30, 2):
            font_size_list.addItem(str(index))
        
        # add to layout, the 2 end numbers are the cell coordinates of row, column
        self.layout().addWidget(font_names_lb, 0, 0)
        self.layout().addWidget(font_names_list, 1, 0)
        
        self.layout().addWidget(font_style_lb, 0, 1)
        self.layout().addWidget(font_style_list, 1, 1)
        
        self.layout().addWidget(font_size_lb, 0, 2)
        self.layout().addWidget(font_size_list, 1, 2)

dialog = simple_ui()
dialog.show()