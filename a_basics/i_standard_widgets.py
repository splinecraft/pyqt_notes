from PySide2 import QtWidgets as qw, QtCore as qc, QtGui as qg
# maya 2017

class simple_ui(qw.QDialog):
    
    def __init__(self):
        qw.QDialog.__init__(self)

        self.setWindowTitle('Simple UI')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setModal(False)
        self.setFixedHeight(250)
        self.setMinimumWidth(300)
        
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(5)
        
        ### TEXT WIDGETS
        text_layout = qw.QHBoxLayout()
        text_layout.setSpacing(5)
        self.layout().addLayout(text_layout)                
        
        # label - static text, can change with setText
        example_lb = qw.QLabel('Title:')
        # example_lb.setText('Foo')
        # set font of label, can change font of any widget with text
        bold_font = qg.QFont()
        bold_font.setBold(True)
        example_lb.setFont(bold_font)

        # line edit - single line box you can type text into
        example_le = qw.QLineEdit()
        example_le.setPlaceholderText('Type something...')
        # text validator to limit what can be entered (only letters and underscore here)
        reg_ex = qc.QRegExp("[a-zA-Z_]+") 
        text_validator = qg.QRegExpValidator(reg_ex, example_le)
        example_le.setValidator(text_validator)
        
        # text edit - multiline text, can deal with rich text, html etc
        # expands to fill space
        example_te = qw.QTextEdit()
        # word wraps by default, turn off and will scroll if typing beyond initial space
        example_te.setWordWrapMode(qg.QTextOption.NoWrap)
        
        
        text_layout.addWidget(example_lb)
        text_layout.addWidget(example_le)
        text_layout.addWidget(example_te)
        
        ### BUTTON WIDGETS
        button_layout = qw.QHBoxLayout()
        button_layout.setSpacing(5)
        self.layout().addLayout(button_layout)
        
        # push button - standard button, expands to fit space
        example_btn = qw.QPushButton('Button')
        
        # radio buttons
        a_radio = qw.QRadioButton('a')
        b_radio = qw.QRadioButton('b')
        c_radio = qw.QRadioButton('c')
        d_radio = qw.QRadioButton('d')
        
        # set default selected button
        a_radio.setChecked(True)
        
        # put radio buttons in groups
        btn_grp_1 = qw.QButtonGroup(self)
        btn_grp_2 = qw.QButtonGroup(self)
        
        btn_grp_1.addButton(a_radio)
        btn_grp_1.addButton(b_radio)
        
        btn_grp_2.addButton(c_radio)
        btn_grp_2.addButton(d_radio)
        
        # check box
        example_check = qw.QCheckBox('Check')
        
        
        button_layout.addWidget(example_btn)
        button_layout.addWidget(a_radio)
        button_layout.addWidget(b_radio)
        button_layout.addWidget(c_radio)
        button_layout.addWidget(d_radio)
        button_layout.addWidget(example_check)

dialog = simple_ui()
dialog.show()