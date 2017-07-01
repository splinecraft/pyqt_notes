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
        self.example_te = qw.QTextEdit()
        # word wraps by default, turn off and will scroll if typing beyond initial space
        self.example_te.setWordWrapMode(qg.QTextOption.NoWrap)
        
        
        text_layout.addWidget(example_lb)
        text_layout.addWidget(example_le)
        text_layout.addWidget(self.example_te)
        
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
        # check box states are 0 and 2 rather than 0 and 1. 1 is rarely used inbetween state
                
        button_layout.addWidget(example_btn)
        button_layout.addWidget(a_radio)
        button_layout.addWidget(b_radio)
        button_layout.addWidget(c_radio)
        button_layout.addWidget(d_radio)
        button_layout.addWidget(example_check)
        
        # SIGNALS AND SLOTS
        # when something is changed, clicked, etc it sends out a signal
        # if its connected to a slot, the signal will cause something to happen
        # in PyQt unlike Qt we don't have to worry about the slots
        counter_layout = qw.QHBoxLayout()
        counter_layout.setSpacing(5)
        self.layout().addLayout(counter_layout)
        
        # EXAMPLE 1
        # here we'll connect a slider to a spin box so the spin box automatically 
        # changes when the slider is moved and vice versa
        # create a slider
        example_slider = qw.QSlider()
        example_slider.setOrientation(qc.Qt.Horizontal)
        example_slider.setRange(0, 10)
        
        # create a spinbox
        example_spin = qw.QSpinBox()
        example_spin.setRange(0, 10)
        
        # 2 ways to connect, option one is more pythonic, but not as easy to read
        #self.connect(example_slider, qc.SIGNAL('valueChanged(int)'), example_spin.setValue)
        #self.connect(example_spin, qc.SIGNAL('valueChanged(int)'), example_slider.setValue)
        
        # option 2, less pythonic but less code, more readable
        example_slider.valueChanged.connect(example_spin.setValue)
        example_spin.valueChanged.connect(example_slider.setValue)
        
        # EXAMPLE 2
        # connect a button to a function we've defined below: print_text
        example_btn.clicked.connect(self.print_text)
        
        # EXAMPLE 3
        # clicking checkbox on/off enables/disables the button
        example_check.stateChanged.connect(example_btn.setDisabled)
        
        # EXAMPLE 4
        # get signal for which radio button is clicked and print
        btn_grp_1.buttonClicked.connect(self.add_to_text_edit)
        
        counter_layout.addWidget(example_slider)
        counter_layout.addWidget(example_spin)
        
        
        
    def print_text(self):
        '''example to print what's in the text_edit in the console'''
        print self.example_te.toPlainText()
        # text edits use toPlainText since they deal with formatted text
        # simpler widgets like line edits would use text()
        # example_le.text()
        
    def add_to_text_edit(self, button):
        '''example to print clicked button in text edit widget'''
        button_text = button.text()
        self.example_te.setText(self.example_te.toPlainText() + button_text)
        

dialog = simple_ui()
dialog.show()