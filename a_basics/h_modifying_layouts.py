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
        
        # add frames which are widgets with style elements
        # gap between edge of window and frame drawn is contents margin
        # gap between frames/widgets is the spacing
        
        # set the contents margin - right, left, top, bottom
        self.layout().setContentsMargins(5, 5, 5, 5)
        
        # set spacing
        self.layout().setSpacing(5)
        
        top_frame = qw.QFrame()
        top_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        middle_frame = qw.QFrame()
        middle_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        bottom_frame = qw.QFrame()
        bottom_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        
        self.layout().addWidget(top_frame)
        self.layout().addWidget(middle_frame)
        self.layout().addWidget(bottom_frame)
        
        middle_frame.setLayout(qw.QHBoxLayout())
        
        # can set contents margins/spacing for individual frames
        middle_frame.layout().setContentsMargins(5,5,5,5)
        middle_frame.layout().setSpacing(5)
        
        # set alignment for frame contents
        middle_frame.layout().setAlignment(qc.Qt.AlignTop)
        
        # set size policy so frame doesn't expand to all available space, only to the size of its contents
        # width, height
        # maximum means it won't expand past the maximum of the contents
        # minimum means it will start at the minimum value and expand the contents if resized
        middle_frame.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Maximum)
        
        btn_1 = qw.QPushButton('1')
        btn_2 = qw.QPushButton('2')
        btn_3 = qw.QPushButton('3')
        btn_4 = qw.QPushButton('4')
        btn_5 = qw.QPushButton('5')
        
        middle_frame.layout().addWidget(btn_1)
        middle_frame.layout().addWidget(btn_2)
        middle_frame.layout().addWidget(btn_3)
        middle_frame.layout().addWidget(btn_4)
        middle_frame.layout().addWidget(btn_5)
        

dialog = simple_ui()
dialog.show()