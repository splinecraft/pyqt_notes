import pymel.core as pm
from PySide2 import QtWidgets as qw, QtCore as qc

from pyqt_notes.interpolate_tool.utils.generic import undo

dialog = None
START = 'start'
END = 'end'
NODE = 'node'
CACHE = 'cache'

class InterpolateIt(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Interpolate It')

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(5,5,5,5)
        self.layout().setSpacing(5)

        # layouts
        select_layout = qw.QHBoxLayout()
        button_layout = qw.QHBoxLayout()
        slider_layout = qw.QHBoxLayout()
        check_layout = qw.QHBoxLayout()
        self.layout().addLayout(select_layout)
        self.layout().addLayout(button_layout)
        self.layout().addLayout(slider_layout)
        self.layout().addLayout(check_layout)

        # buttons
        # row 1
        store_items = qw.QPushButton('Store Items')
        clear_items = qw.QPushButton('Clear Items')

        select_layout.addSpacerItem(qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding))
        select_layout.addWidget(store_items)
        select_layout.addWidget(clear_items)
        select_layout.addSpacerItem(qw.QSpacerItem(5, 5, qw.QSizePolicy.Expanding))

        # row 2
        self.store_start_btn = qw.QPushButton('Store Start')
        self.reset_item_btn = qw.QPushButton('Reset')
        self.store_end_btn = qw.QPushButton('Store End')

        button_layout.addWidget(self.store_start_btn)
        button_layout.addWidget(self.reset_item_btn)
        button_layout.addWidget(self.store_end_btn)

        # row 3
        self.start_lb = qw.QLabel('Start')
        self.slider = qw.QSlider()
        self.slider.setRange(0, 49)
        self.slider.setOrientation(qc.Qt.Horizontal)
        self.end_lb = qw.QLabel('End')

        slider_layout.addWidget(self.start_lb)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.end_lb)

        # row 4
        self.transforms_chbx = qw.QCheckBox('Transform')
        self.attributes_chbx = qw.QCheckBox('UD Attributes')
        self.transforms_chbx.setCheckState(qc.Qt.Checked)
        check_layout.addWidget(self.transforms_chbx)
        check_layout.addWidget(self.attributes_chbx)

        # dict to store objects
        self.items = {}
        self.slider_down = False

        # connections
        #
        store_items.clicked.connect(self.store_items)
        clear_items.clicked.connect(self.clear_items)
        self.store_start_btn.clicked.connect(self.store_start)
        self.reset_item_btn.clicked.connect(self.reset_attributes)
        self.store_end_btn.clicked.connect(self.store_end)

        self.slider.valueChanged.connect(self.set_linear_interpolation)
        self.slider.sliderReleased.connect(self._end_slider_undo)

        self.enable_buttons(False)

    # ------------------------------------------------------------------------#

    # each tick on the slider when moved is recorded as an action, so we will chunk the undos when the slider
    # is moved so each move is an action
    def _start_slider_undo(self):
        pm.undoInfo(openChunk=True)

    def _end_slider_undo(self):
        pm.undoInfo(closeChunk=True)
        self.slider_down = False

    # ------------------------------------------------------------------------#

    def store_items(self):
        selection = pm.ls(selection=True, flatten=True)
        if not selection:
            return False

        self.clear_items()
        for node in selection:
            self.items[node.name()] = {NODE:node,START:{},END:{},CACHE:{}}

        self.enable_buttons(True)

    def clear_items(self):
        self.items = {}
        self.enable_buttons(False)

    # ------------------------------------------------------------------------#

    def enable_buttons(self, value):
        self.store_start_btn.setEnabled(value)
        self.reset_item_btn.setEnabled(value)
        self.store_end_btn.setEnabled(value)
        self.transforms_chbx.setEnabled(value)
        self.attributes_chbx.setEnabled(value)
        self.slider.setEnabled(value)
        self.start_lb.setEnabled(value)
        self.end_lb.setEnabled(value)

    # ------------------------------------------------------------------------#

    def store_start(self):
        if not self.items:
            return
        self._store(START, 0)
        self._cache()

    def store_end(self):
        if not self.items:
            return
        self._store(END, 50)
        self._cache()

    def _store(self, key, value):
        for item_dict in self.items.values():
            node = item_dict[NODE]
            attrs = self.get_attributes(node)
            data = item_dict[key]
            for attr in attrs:
                data[attr] = node.attr(attr).get()
                # in pymel, use .attr method with the attribute as the argument and
                # .get() to get the value of an attribute

            print(item_dict)

        # if the slider is set while storing the attributes its signal will trigger
        # again during, which we don't want. Turn its signals off during this update
        # then back on again after
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)

    def _cache(self):
        for item_dict in self.items.values():
            node = item_dict[NODE]

            start = item_dict[START]
            end = item_dict[END]
            if not start or not end:
                item_dict[CACHE] = None
                continue

            attrs = list(set(start.keys()) and set(end.keys()))

            cache = item_dict[CACHE] = {}
            for attr in attrs:
                start_attr = start[attr]
                end_attr = end[attr]
                if start_attr == end_attr:
                    cache[attr] = None
                else:
                    cache_values = cache[attr] = []
                    interval = float(end_attr - start_attr) / 49.0
                    for index in range(50):
                        cache_values.append((interval * index) + start_attr)

    # ------------------------------------------------------------------------#

    def get_attributes(self, node):
        attrs = []
        if self.transforms_chbx.isChecked():
            for transform in 'trs':
                for axis in 'xyz':
                    channel = '%s%s' %(transform, axis)
                    if node.attr(channel).isLocked(): continue
                    attrs.append(channel)

        if self.attributes_chbx.isChecked():
            for attr in node.listAttr(ud=True):
                if attr.isLocked(): continue
                if attr.type() not in ('double', 'int'): continue

                attrs.append(attr.name().split('.')[-1])

        return attrs

    @undo
    def reset_attributes(self, *args):
        if not self.items:
            return

        for item_dict in self.items.values():
            node = item_dict[NODE]
            attrs = self.get_attributes(node)

            for attr in attrs:
                default_value = pm.attributeQuery(attr, node=node, ld=True)[0]
                node.attr(attr).set(default_value)
    # ------------------------------------------------------------------------#

    def set_linear_interpolation(self, value):
        if not self.items:
            return

        if not self.slider_down:
            self._start_slider_undo()
            self.slider_down = True

        for item_dict in self.items.values():
            node = item_dict[NODE]
            start = item_dict[START]

            if not start or not item_dict[END]: continue

            cache = item_dict[CACHE]

            for attr in cache.keys():
                if cache[attr] == None: continue
                node.attr(attr).set(cache[attr][value])
# ------------------------------------------------------------------------#


def create():
    """If the global dialog is None, no instance exists so create one and show it.
    If its not, then it does exist so simply bring it back. This way any settings
    we had from before will still be there and we won't get multiple copies of NameIt
    instances filling up in memory"""
    global dialog
    if dialog is None:
        dialog = InterpolateIt()
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