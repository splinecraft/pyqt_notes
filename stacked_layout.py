from PySide2 import QtWidgets as qw, QtCore as qc, QtGui as qg
# maya 2017

from functools import partial

class simple_ui(qw.QDialog):
    
    def __init__(self):
        qw.QDialog.__init__(self)

        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setFixedWidth(300)
        
        # layouts control how widgets go into their parent (the dialog here)
        # stacked layouts are multiple widgets in a list on top of each other
        # the index of the widget determines which one is shown currently
        self.setLayout(qw.QVBoxLayout())
        self.stacked_layout = qw.QStackedLayout()
        self.layout().addLayout(self.stacked_layout)

        # make a button layout that will stay persistent at the bottom to switch between the layouts
        button_layout = qw.QHBoxLayout()
        layout_1_bttn = qw.QPushButton('Layout_1')
        layout_2_bttn = qw.QPushButton('Layout_2')
        layout_3_bttn = qw.QPushButton('Layout_3')
        layout_4_bttn = qw.QPushButton('Layout_4')
        button_layout.addWidget(layout_1_bttn)
        button_layout.addWidget(layout_2_bttn)
        button_layout.addWidget(layout_3_bttn)
        button_layout.addWidget(layout_4_bttn)

        # add layout to main layout
        self.layout().addLayout(button_layout)

        # VBOX AND HBOX
        # make an empty widget to hold a layout
        hbox_widget = qw.QWidget()
        hbox_widget.setLayout(qw.QHBoxLayout())

        bttn_1 = qw.QPushButton('Button 1')
        bttn_2 = qw.QPushButton('Button 2')
        bttn_3 = qw.QPushButton('Button 3')
        bttn_4 = qw.QPushButton('Button 4')
        bttn_5 = qw.QPushButton('Button 5')

        hbox_widget.layout().addWidget(bttn_1)
        hbox_widget.layout().addWidget(bttn_2)
        hbox_widget.layout().addWidget(bttn_3)
        hbox_widget.layout().addWidget(bttn_4)
        hbox_widget.layout().addWidget(bttn_5)

        # layout 2 inside another widget
        vbox_widget = qw.QWidget()
        vbox_widget.setLayout(qw.QVBoxLayout())

        bttn_1 = qw.QPushButton('Button 1')
        bttn_2 = qw.QPushButton('Button 2')
        bttn_3 = qw.QPushButton('Button 3')
        bttn_4 = qw.QPushButton('Button 4')
        bttn_5 = qw.QPushButton('Button 5')

        vbox_widget.layout().addWidget(bttn_1)
        vbox_widget.layout().addWidget(bttn_2)
        vbox_widget.layout().addWidget(bttn_3)
        vbox_widget.layout().addWidget(bttn_4)
        vbox_widget.layout().addWidget(bttn_5)

        # FORM layout 3 inside another widget
        form_widget = qw.QWidget()
        form_widget.setLayout(qw.QFormLayout())

        name_le  = qw.QLineEdit()
        email_le = qw.QLineEdit()
        age_le   = qw.QSpinBox()

        form_widget.layout().addRow('Name:', name_le)
        form_widget.layout().addRow('Email:', email_le)
        form_widget.layout().addRow('Age:', age_le)

        # GRID layout 4 inside another widget
        grid_widget = qw.QWidget()
        grid_widget.setLayout(qw.QGridLayout())

        font_names_lb = qw.QLabel('Font')
        font_style_lb = qw.QLabel('Font Style')
        font_size_lb  = qw.QLabel('Size')

        font_names_list = qw.QListWidget()
        font_names_list.addItem('Times')
        font_names_list.addItem('Helvetica')
        font_names_list.addItem('Courier')
        font_names_list.addItem('Palatino')
        font_names_list.addItem('Gill Sans')

        font_style_list = qw.QListWidget()
        font_style_list.addItem('Roman')
        font_style_list.addItem('Italic')
        font_style_list.addItem('Oblique')

        font_size_list  = qw.QListWidget()
        for index in range(10, 30, 2):
            font_size_list.addItem(str(index))

        grid_widget.layout().addWidget(font_names_lb,   0, 0)
        grid_widget.layout().addWidget(font_names_list, 1, 0)

        grid_widget.layout().addWidget(font_style_lb,   0, 1)
        grid_widget.layout().addWidget(font_style_list, 1, 1)

        grid_widget.layout().addWidget(font_size_lb,   0, 2)
        grid_widget.layout().addWidget(font_size_list, 1, 2)

        # the order the widgets are added to the stacked layout determines their index
        self.stacked_layout.addWidget(vbox_widget)
        self.stacked_layout.addWidget(hbox_widget)
        self.stacked_layout.addWidget(form_widget)
        self.stacked_layout.addWidget(grid_widget)

        # clicking the button switches the index and therefore the widget and its layout within shown
        layout_1_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 0))
        layout_2_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 1))
        layout_3_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 2))
        layout_4_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 3))

dialog = simple_ui()
dialog.show()