# 左侧
from PyQt5.Qt import *
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QCheckBox, QGroupBox
from PyQt5 import QtCore


# 设置自定义table表头
class CxTableItem(QWidget):
    deleteClicked = pyqtSignal([QWidget])
    viewClicked = pyqtSignal([QWidget])
    exportClicked = pyqtSignal([QWidget])
    Id = 0

    def __init__(self, controls, parent=None):
        super(CxTableItem, self).__init__(parent)
        self.setObjectName("CxTableItem")
        # 复选框
        self.checkBox = QCheckBox()
        self.checkBox.setMaximumWidth(40)
        self.checkBox.setMaximumHeight(20)
        self.checkBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        # 名称
        self.lblName = QLabel()
        # 类型
        #print("====>",type(controls[1])," size:",len(controls))
        self.lblType = QLabel()
        # x起始值
        self.lblXStart = QLabel()
        # x结束至
        self.lblXEnd = QLabel()
        # x步长
        self.lblXStep = QLabel()
        # y起始值
        self.lblYStart = QLabel()
        # y结束至
        self.lblYEnd = QLabel()
        # y步长
        self.lblYStep = QLabel()
        # 入射角
        self.lblAngle = QLabel()
        # 折射率
        self.lblZSL = QLabel()
        # 分频系数
        self.lblDivFreq = QLabel()
        # 扫描范围
        self.lblScanRange = QLabel()
        # 操作员
        self.lblOperator = QLabel()
        # 日期
        self.lblDate = QLabel()
        # 操作
        self.gpxOptional = QGroupBox()
        self.gpxOptional.setStyleSheet('''background-color: transparent;''')
        self.gpxOptional.setContentsMargins(0, 0, 0, 0)
        self.hboxOpt = QHBoxLayout(self.gpxOptional)
        self.hboxOpt.setContentsMargins(0, 0, 0, 0)
        self.hboxOpt.setSpacing(0)
        self.viewBtn = QPushButton(self.gpxOptional)
        self.exportBtn = QPushButton(self.gpxOptional)
        self.deleteBtn = QPushButton(self.gpxOptional)
        self.viewBtn.setText("查看")
        self.viewBtn.setObjectName("optView")
        self.exportBtn.setText("导出")
        self.exportBtn.setObjectName("optExport")
        self.deleteBtn.setText("删除")
        self.deleteBtn.setObjectName("optDel")
        self.hboxOpt.addWidget(self.viewBtn)
        self.hboxOpt.addWidget(self.exportBtn)
        self.hboxOpt.addWidget(self.deleteBtn)

        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.hbox = QHBoxLayout()
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)
        #print("checkbox width:",controls[1].maximumWidth())
        self.checkBox.setMaximumWidth(controls[1].maximumWidth())
        self.checkBox.setMinimumWidth(controls[1].minimumWidth())
        self.hbox.addWidget(self.checkBox)
        self.lblName.setMaximumWidth(controls[2].maximumWidth())
        self.lblName.setMinimumWidth(controls[2].minimumWidth())
        #print("lblName width:", controls[2].minimumWidth())
        self.hbox.addWidget(self.lblName)
        self.lblType.setMaximumWidth(controls[3].maximumWidth())
        self.lblType.setMinimumWidth(controls[3].minimumWidth())
        #print("lblType width:", controls[3].minimumWidth())
        self.hbox.addWidget(self.lblType)
        self.lblXStart.setMaximumWidth(controls[4].maximumWidth())
        self.lblXStart.setMinimumWidth(controls[4].minimumWidth())
        #print("lblScanTime width:", controls[4].minimumWidth())
        self.hbox.addWidget(self.lblXStart)
        self.lblXEnd.setMaximumWidth(controls[5].maximumWidth())
        self.lblXEnd.setMinimumWidth(controls[5].minimumWidth())
        #print("lblThickness width:", controls[5].minimumWidth())
        self.hbox.addWidget(self.lblXEnd)

        self.lblXStep.setMaximumWidth(controls[6].maximumWidth())
        self.lblXStep.setMinimumWidth(controls[6].minimumWidth())
        # print("lblThickness width:", controls[5].minimumWidth())
        self.hbox.addWidget(self.lblXStep)

        self.lblYStart.setMaximumWidth(controls[7].maximumWidth())
        self.lblYStart.setMinimumWidth(controls[7].minimumWidth())
        # print("lblScanTime width:", controls[4].minimumWidth())
        self.hbox.addWidget(self.lblYStart)
        self.lblYEnd.setMaximumWidth(controls[8].maximumWidth())
        self.lblYEnd.setMinimumWidth(controls[8].minimumWidth())
        # print("lblThickness width:", controls[5].minimumWidth())
        self.hbox.addWidget(self.lblYEnd)

        self.lblYStep.setMaximumWidth(controls[9].maximumWidth())
        self.lblYStep.setMinimumWidth(controls[9].minimumWidth())
        # print("lblThickness width:", controls[5].minimumWidth())
        self.hbox.addWidget(self.lblYStep)

        self.lblAngle.setMaximumWidth(controls[10].maximumWidth())
        self.lblAngle.setMinimumWidth(controls[10].minimumWidth())
        # print("lblThickness width:", controls[5].minimumWidth())
        self.hbox.addWidget(self.lblAngle)

        self.lblZSL.setMaximumWidth(controls[11].maximumWidth())
        self.lblZSL.setMinimumWidth(controls[11].minimumWidth())
        # print("lblThickness width:", controls[5].minimumWidth())
        self.hbox.addWidget(self.lblZSL)

        self.lblDivFreq.setMaximumWidth(controls[12].maximumWidth())
        self.lblDivFreq.setMinimumWidth(controls[12].minimumWidth())
        # print("lblDivFreq width:", controls[6].minimumWidth())
        self.hbox.addWidget(self.lblDivFreq)
        self.lblScanRange.setMaximumWidth(controls[13].maximumWidth())
        self.lblScanRange.setMinimumWidth(controls[13].minimumWidth())
        # print("lblScanRange width:", controls[7].minimumWidth()," txt:",controls[7].text())
        self.hbox.addWidget(self.lblScanRange)
        self.lblOperator.setMaximumWidth(controls[14].maximumWidth())
        self.lblOperator.setMinimumWidth(controls[14].minimumWidth())
        # print("lblOperator width:", controls[8].minimumWidth())
        self.hbox.addWidget(self.lblOperator)
        self.lblDate.setMaximumWidth(controls[15].maximumWidth())
        self.lblDate.setMinimumWidth(controls[15].minimumWidth())
        # print("lblDate width:", controls[9].minimumWidth())
        self.hbox.addWidget(self.lblDate)
        self.gpxOptional.setMaximumWidth(controls[16].maximumWidth())
        self.gpxOptional.setMinimumWidth(controls[16].minimumWidth())
        # print("gpxOptional width:",controls[10].minimumWidth())
        self.hbox.addWidget(self.gpxOptional)

        # 设置widget的布局
        self.setLayout(self.hbox)
        self.deleteBtn.clicked.connect(self.OnDeleteBtnClicked)
        self.viewBtn.clicked.connect(self.OnViewBtnClicked)
        self.exportBtn.clicked.connect(self.OnExportBtnClicked)

    def OnDeleteBtnClicked(self):
        self.deleteClicked[QWidget].emit(self)

    def OnViewBtnClicked(self):
        self.viewClicked[QWidget].emit(self)

    def OnExportBtnClicked(self):
        self.exportClicked[QWidget].emit(self)
