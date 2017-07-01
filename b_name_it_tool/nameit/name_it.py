from PySide2 import QtWidgets as qw, QtCore as qc, QtGui as qg
import utils.names as names
import maya.cmds as cmds
# maya 2017

# global variable for our instance. Using this and create/delete functions prevents multiple
# instances filling up in memory each time we close/reopen a UI. These instances will have 
# the same name but there would be no way to delete them. 
dialog = None


# ------------------------------------------------------------------------#

class NameIt(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Name It')
        self.setFixedHeight(285)
        self.setFixedWidth(320)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(5)
        self.layout().setAlignment(qc.Qt.AlignTop)

        # RENAME WIDGET
        # each section of the tool is its own widget/layout
        # advantageous to just using layouts because layouts are visual only
        # widgets can be changed, hidden, etc
        #
        rename_widget = qw.QWidget()
        rename_widget.setLayout(qw.QVBoxLayout())
        rename_widget.layout().setContentsMargins(0, 0, 0, 0)
        rename_widget.layout().setSpacing(2)
        rename_widget.setSizePolicy(qw.QSizePolicy.Minimum,
                                    qw.QSizePolicy.Fixed)
        self.layout().addWidget(rename_widget)

        # add the horizontal line splitter with a custom widget we made below
        rename_splitter = Splitter(text='RENAME')
        rename_widget.layout().addWidget(rename_splitter)

        # rename text layout
        rename_text_layout = qw.QHBoxLayout()
        rename_text_layout.setContentsMargins(4, 0, 4, 0)
        rename_text_layout.setSpacing(2)
        # add to rename widget
        rename_widget.layout().addLayout(rename_text_layout)

        # rename text widgets
        rename_text_lb = qw.QLabel('New Name:')
        self.rename_le = qw.QLineEdit()
        rename_text_layout.addWidget(rename_text_lb)
        rename_text_layout.addWidget(self.rename_le)

        # use regular expressions to prevent typing symbols into the rename le, which aren't allowed in Maya names
        reg_ex_ren = qc.QRegExp("^(?!^_)[a-zA-Z_]+")
        # second argument is the parent, which we assign just to keep it alive, otherwise it may be deleted right after
        text_validator_rename = qg.QRegExpValidator(reg_ex_ren, self.rename_le)
        self.rename_le.setValidator(text_validator_rename)

        # add the custom divider line
        rename_widget.layout().addLayout(SplitterLayout())

        # rename multiples layout
        rename_mult_layout = qw.QHBoxLayout()
        rename_mult_layout.setContentsMargins(4, 0, 4, 0)
        rename_mult_layout.setSpacing(2)
        # add to rename widget
        rename_widget.layout().addLayout(rename_mult_layout)

        # rename multiples widgets
        rename_mult_method_lb = qw.QLabel('Multiples Naming Method:')
        self.rename_mult_method_combo = qw.QComboBox()
        self.rename_mult_method_combo.addItem('Numbers (0-9)')
        self.rename_mult_method_combo.addItem('Letters (a-z)')
        self.rename_mult_method_combo.setFixedWidth(120)  # otherwise will expand to fill space
        rename_mult_layout.addWidget(rename_mult_method_lb)
        rename_mult_layout.addWidget(self.rename_mult_method_combo)

        # rename multiples options layout
        # The options will change depending on what is selected in the combo box above
        multi_options_layout = qw.QHBoxLayout()
        multi_options_layout.setContentsMargins(4, 0, 4, 0)
        multi_options_layout.setSpacing(2)
        # add to rename widget
        rename_widget.layout().addLayout(multi_options_layout)

        # rename multiples options widgets
        # numbers option from rename_multi_method_combo
        self.frame_pad_lb = qw.QLabel('No. Padding:')
        self.frame_pad_spin = qw.QSpinBox()
        self.frame_pad_spin.setFixedWidth(40)
        self.frame_pad_spin.setMinimum(0)
        self.frame_pad_spin.setMaximum(10)

        # letters option from rename_multi_method_combo
        self.lower_radio = qw.QRadioButton('Lowercase')
        self.upper_radio = qw.QRadioButton('Uppercase')
        # since the numbers option is the default, turn these off for now
        self.lower_radio.setVisible(False)
        self.upper_radio.setVisible(False)
        self.lower_radio.setFixedHeight(19)
        self.upper_radio.setFixedHeight(19)
        self.lower_radio.setChecked(True)  # default selected option

        # add to multi options layout
        # left side options
        multi_options_layout.addWidget(self.frame_pad_lb)
        multi_options_layout.addWidget(self.lower_radio)
        # use an expanding spacer to push each one to the left/right
        multi_options_layout.addSpacerItem(qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding))
        # right side options
        multi_options_layout.addWidget(self.frame_pad_spin)
        multi_options_layout.addWidget(self.upper_radio)

        # add the custom divider line
        rename_widget.layout().addLayout(SplitterLayout())

        # prefix/suffix options layout
        fix_layout = qw.QHBoxLayout()
        fix_layout.setContentsMargins(4, 0, 4, 0)
        fix_layout.setSpacing(2)
        # add to rename widget
        rename_widget.layout().addLayout(fix_layout)

        # prefix and suffix checks/options widgets
        self.prefix_check = qw.QCheckBox('Prefix:')
        self.prefix_le = qw.QLineEdit()
        self.prefix_le.setEnabled(False)  # don't allow typing into line edit if not checked
        self.prefix_le.setFixedWidth(85)
        self.prefix_le.setValidator(text_validator_rename)  # use the same validator, don't need a new parent

        self.suffix_check = qw.QCheckBox('Suffix:')
        self.suffix_le = qw.QLineEdit()
        self.suffix_le.setEnabled(False)  # don't allow typing into line edit if not checked
        self.suffix_le.setFixedWidth(85)
        self.suffix_le.setValidator(text_validator_rename)

        # add to fix layout
        fix_layout.addWidget(self.prefix_check)
        fix_layout.addWidget(self.prefix_le)
        fix_layout.addSpacerItem(qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding))
        fix_layout.addWidget(self.suffix_check)
        fix_layout.addWidget(self.suffix_le)

        # add the custom divider line
        rename_widget.layout().addLayout(SplitterLayout())

        # rename button layout
        rename_button_layout = qw.QHBoxLayout()
        rename_button_layout.setContentsMargins(4, 0, 4, 0)
        rename_button_layout.setSpacing(0)
        # add to rename widget
        rename_widget.layout().addLayout(rename_button_layout)

        # rename button widgets
        self.rename_lb = qw.QLabel('e.g.')
        rename_btn = qw.QPushButton('Rename')
        rename_btn.setFixedHeight(20)
        rename_btn.setFixedWidth(55)

        # add to rename button layout
        rename_button_layout.addWidget(self.rename_lb)
        rename_button_layout.addWidget(rename_btn)

        # REPLACE WIDGET
        #
        replace_widget = qw.QWidget()
        replace_widget.setLayout(qw.QVBoxLayout())
        replace_widget.layout().setContentsMargins(0, 0, 0, 0)
        replace_widget.layout().setSpacing(2)
        replace_widget.setSizePolicy(qw.QSizePolicy.Minimum,
                                     qw.QSizePolicy.Fixed)
        self.layout().addWidget(replace_widget)

        # replace splitter from custom widget class below
        replace_splitter = Splitter(text='FIND/REPLACE')
        replace_widget.layout().addWidget(replace_splitter)

        # replace layout
        replace_layout = qw.QHBoxLayout()
        replace_layout.setContentsMargins(4, 0, 4, 0)
        replace_layout.setSpacing(2)
        # add to replace widget
        replace_widget.layout().addLayout(replace_layout)

        # replace widgets
        replace_lb = qw.QLabel('Find:')
        replace_lb.setFixedWidth(55)
        self.replace_le = qw.QLineEdit()

        # find/replace validator; simpler than rename one because we may search for strings within strings
        reg_ex_rep = qc.QRegExp("[a-zA-Z_]+")
        text_validator_replace = qg.QRegExpValidator(reg_ex_rep, self.replace_le)
        self.replace_le.setValidator(text_validator_replace)

        # add to replace layout
        replace_layout.addWidget(replace_lb)
        replace_layout.addWidget(self.replace_le)

        # replace with layout
        with_layout = qw.QHBoxLayout()
        with_layout.setContentsMargins(4, 0, 4, 0)
        with_layout.setSpacing(2)
        # add to replace widget
        replace_widget.layout().addLayout(with_layout)

        # with widgets
        with_lb = qw.QLabel('Replace:')
        with_lb.setFixedWidth(55)
        self.with_le = qw.QLineEdit()
        self.with_le.setValidator(text_validator_replace)

        # add to replace with layout
        with_layout.addWidget(with_lb)
        with_layout.addWidget(self.with_le)

        # add the custom divider line
        replace_widget.layout().addLayout(SplitterLayout())

        # selection layout
        selection_layout = qw.QHBoxLayout()
        selection_layout.setContentsMargins(4, 0, 4, 0)
        selection_layout.setSpacing(2)
        # add to replace widget
        replace_widget.layout().addLayout(selection_layout)

        # selection widgets
        selection_mode_lb = qw.QLabel('Selection Mode:')
        self.all_radio = qw.QRadioButton('All')
        self.all_radio.setFixedHeight(19)
        self.all_radio.setChecked(True)
        selected_radio = qw.QRadioButton('Selected')
        selected_radio.setFixedHeight(19)

        # add to selection layout
        selection_layout.addWidget(selection_mode_lb)
        spacer_item = qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding)
        selection_layout.addSpacerItem(spacer_item)
        selection_layout.addWidget(self.all_radio)
        selection_layout.addWidget(selected_radio)

        # add the custom divider line
        replace_widget.layout().addLayout(SplitterLayout())

        # replace button layout
        replace_btn_layout = qw.QHBoxLayout()
        replace_btn_layout.setContentsMargins(4, 0, 4, 0)
        replace_btn_layout.setSpacing(2)
        replace_btn_layout.setAlignment(qc.Qt.AlignRight)
        # add to replace widget
        replace_widget.layout().addLayout(replace_btn_layout)

        # replace button
        replace_btn = qw.QPushButton('Replace')
        replace_btn.setFixedHeight(20)
        replace_btn.setFixedWidth(55)

        # add to replace button layout
        replace_btn_layout.addWidget(replace_btn)

        # ------------------------------------------------------------------------#
        # good practice to put all modifiers and connections in one place

        # connect modifiers
        #
        self.prefix_check.stateChanged.connect(self.prefix_le.setEnabled)
        self.suffix_check.stateChanged.connect(self.suffix_le.setEnabled)
        self.prefix_check.stateChanged.connect(self._update_example_rename)
        self.suffix_check.stateChanged.connect(self._update_example_rename)

        self.rename_mult_method_combo.currentIndexChanged.connect(self._toggle_multi_naming_method)
        self.rename_mult_method_combo.currentIndexChanged.connect(self._update_example_rename)
        self.lower_radio.clicked.connect(self._update_example_rename)
        self.upper_radio.clicked.connect(self._update_example_rename)
        self.frame_pad_spin.valueChanged.connect(self._update_example_rename)

        self.rename_le.textChanged.connect(self._update_example_rename)
        self.prefix_le.textChanged.connect(self._update_example_rename)
        self.suffix_le.textChanged.connect(self._update_example_rename)

        rename_btn.clicked.connect(self.rename)
        replace_btn.clicked.connect(self.replace)

        self._update_example_rename()

    # ------------------------------------------------------------------------#

    # create a function to facilitate the multi options switching
    def _toggle_multi_naming_method(self, index):
        self.lower_radio.setVisible(index)
        self.upper_radio.setVisible(index)
        self.frame_pad_lb.setVisible(not (index))
        self.frame_pad_spin.setVisible(not (index))

    # ------------------------------------------------------------------------#

    def _get_rename_settings(self):
        text = str(self.rename_le.text()).strip()  # text is a Qt string, change to python string
        naming_method = bool(self.rename_mult_method_combo.currentIndex())  # change Qt bool to python bool

        padding = 0;
        upper = True
        if naming_method == 0:  # using numbers
            padding = self.frame_pad_spin.value()
        else:  # using letters
            upper = self.upper_radio.isChecked()

        prefix = '';
        suffix = ''
        if self.prefix_check.isChecked():
            prefix = str(self.prefix_le.text()).strip()
        if self.suffix_check.isChecked():
            suffix = str(self.suffix_le.text()).strip()

        # return in order the rename function is expecting arguments
        return text, prefix, suffix, padding, naming_method, upper

    # ------------------------------------------------------------------------#

    def _update_example_rename(self):
        example_text = ''

        text, prefix, suffix, padding, naming_method, upper = self._get_rename_settings()

        if not text:  # keep default example
            self.rename_lb.setText('<font color=#646464>e.g.</font>')  # can use html styling to format text
            return

        if prefix:  example_text += '%s_' % prefix
        example_text += '%s_' % text

        if naming_method:
            if upper:
                example_text += 'A'
            else:
                example_text += 'a'
        else:
            example_text += (padding * '0') + '1'

        if suffix: example_text += '_%s' % suffix

        self.rename_lb.setText('<font color=#646464>e.g. \'%s\'</font>' % example_text)

    # ------------------------------------------------------------------------#

    def rename(self):
        names.rename(cmds.ls(sl=True), *self._get_rename_settings())

    # ------------------------------------------------------------------------#

    def replace(self):
        replace_text = str(self.replace_le.text()).strip()
        with_text = str(self.with_le.text()).strip()

        if self.all_radio.isChecked():
            nodes = cmds.ls()
        else:
            nodes = cmds.ls(sl=True)

        names.find_replace(nodes, replace_text, with_text)

# ------------------------------------------------------------------------#
# For the splitter we make our own widget that inherits from QWidget class
# We can customize it to make a widget that suits our needs
class Splitter(qw.QWidget):
    def __init__(self, text=None, shadow=True, color=(150, 150, 150)):
        qw.QWidget.__init__(self)

        self.setMinimumHeight(2)
        self.setLayout(qw.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignVCenter)

        # use a frame (basically a styled widget) to create the horizontal line separator
        first_line = qw.QFrame()
        first_line.setFrameStyle(qw.QFrame.HLine)
        self.layout().addWidget(first_line)

        # In PyQt we can use style sheets which function much like html or css styles to modify attributes like
        # colors, fonts, etc. Maya's interface has a style sheet of its own, which is what the UI's we build
        # inherit from by default, and we can then override them if we like
        main_color = 'rgba( %s, %s, %s, 255)' % color
        shadow_color = 'rgba(45, 45, 45, 255)'

        bottom_border = ''
        if shadow:
            bottom_border = 'border-bottom:1px solid %s;' % shadow_color

        style_sheet = "border:0px solid rgba(0,0,0,0); \
                       background-color: %s; \
                       max-height:1px; \
                       %s" % (main_color, bottom_border)
        first_line.setStyleSheet(style_sheet)

        # if not using the text label option for our widget, just exit
        if text is None:
            return

        # otherwise, create our font and text attributes for the label
        first_line.setMaximumWidth(5)

        font = qg.QFont()
        font.setBold(True)

        # Qt has font metrics to get the size of the label
        text_width = qg.QFontMetrics(font)
        width = text_width.width(text) + 6  # little bit of space after the label before the line continues

        label = qw.QLabel()
        label.setText(text)
        label.setFont(font)
        label.setMaximumWidth(width)
        label.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)

        self.layout().addWidget(label)

        second_line = qw.QFrame()
        second_line.setFrameStyle(qw.QFrame.HLine)
        second_line.setStyleSheet(style_sheet)
        self.layout().addWidget(second_line)


# class for the light divider lines, inherits from a horizontal layout and based off of the custom splitter
class SplitterLayout(qw.QHBoxLayout):
    def __init__(self):
        qw.QHBoxLayout.__init__(self)
        self.setContentsMargins(40, 2, 40, 2)

        splitter = Splitter(shadow=False, color=(60, 60, 60))
        splitter.setFixedHeight(1)

        self.addWidget(splitter)


# ------------------------------------------------------------------------#


def create():
    """If the global dialog is None, no instance exists so create one and show it.
    If its not, then it does exist so simply bring it back. This way any settings
    we had from before will still be there and we won't get multiple copies of NameIt
    instances filling up in memory"""
    global dialog
    if dialog is None:
        dialog = NameIt()
    dialog.show()


def delete():
    """Function to properly get rid of our ui instance"""
    global dialog
    if dialog is None:
        return

    # With Qt flags and signals can sometimes keep instances alive, so we explicitly flag it
    # to delete when changed, then set it to None so python deletes it    
    dialog.deleteLater()
    dialog = None
