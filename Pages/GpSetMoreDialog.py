import globalvar as gl
from AppData import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Common.DialogEx import DialogEx


class GpSetMoreDialog(DialogEx):
    def __init__(self):
        super(GpSetMoreDialog, self).__init__(None)
        self.set1BtnMode()
        self.content = QWidget()

        self.gridLayout = QGridLayout(self.content)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.label1 = QLabel('相位：', self.widget)
        self.label1.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label1, 0, 0, 1, 1)
        self.txtPhase = QLineEdit(self.widget)
        self.txtPhase.setValidator(QIntValidator(0, 360, self))
        self.txtPhase.textChanged.connect(self.onTextChanged)
        self.gridLayout.addWidget(self.txtPhase, 0, 1, 1, 1)
        self.hLayout = QHBoxLayout()
        self.label3 = QLabel('0', self.widget)

        self.hLayout.addWidget(self.label3)
        self.slider = QSlider(self.widget)

        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setRange(0, 360)
        self.slider.valueChanged.connect(self.onValueChanged)
        self.hLayout.addWidget(self.slider)
        self.label4 = QLabel('360', self.widget)
        self.hLayout.addWidget(self.label4)
        self.gridLayout.addLayout(self.hLayout, 0, 2, 1, 1)
        self.label2 = QLabel('积分时间：', self.widget)
        self.label2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.label2, 1, 0, 1, 1)
        self.txtTime = QLineEdit(self.widget)
        self.txtTime.setValidator(QIntValidator(0, 20000, self))
        self.gridLayout.addWidget(self.txtTime, 1, 1, 1, 1)
        self.hLayout2 = QHBoxLayout()
        self.label5 = QLabel('ms', self.widget)
        self.hLayout2.addWidget(self.label5)
        self.spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hLayout2.addItem(self.spacer)
        self.gridLayout.addLayout(self.hLayout2, 1, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 6)
        self.txtPhase.setText(f'{SysConf.devGpMode.amplifier.phase}')
        self.txtTime.setText(f'{SysConf.devGpMode.amplifier.time}')
        self.setContent(self.content)
        self.resize(400, 250)

    def onValueChanged(self, data):
        self.txtPhase.setText(f'{data}')

    def onTextChanged(self, text):
        if gl.isStrNoneOrEmpty(text):
            self.slider.setValue(0)
        else:
            self.slider.setValue(int(text))

    @pyqtSlot()
    def on_btnOk_clicked(self):
        SysConf.devGpMode.amplifier.phase = self.slider.value()
        SysConf.devGpMode.amplifier.time = int(self.txtTime.text())
        SysConf.saveDevGp('config/gpMode.json')
        self.done(DialogEx.OK)