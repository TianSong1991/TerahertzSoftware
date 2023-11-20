import math
import globalvar
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg


class LineChart(QWidget):
    def __init__(self, parent=None):
        super(LineChart, self).__init__(parent)
        self.y = []
        self.x = []
        self.lineArr = []
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.content = QWidget(self)
        self.layout.addWidget(self.content)
        self.verticalLayout = QVBoxLayout(self.content)
        self.verticalLayout.setContentsMargins(5, 0, 20, 5)
        self.verticalLayout.setSpacing(0)
        self.titleBar = QWidget(self.content)
        self.horizontalLayout = QHBoxLayout(self.titleBar)
        self.horizontalLayout.setContentsMargins(0, 10, 0, 8)
        self.horizontalLayout.setSpacing(0)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.title = QLabel(self.titleBar)
        font = QFont()
        font.setPointSize(14)
        self.title.setFont(font)
        self.horizontalLayout.addWidget(self.title)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.xyLabel = QLabel('', self.titleBar)

        self.setStyleSheet('QPushButton{background-color:#FF00A3DA;color:white;border:none;font: 16pt "Webdings";}'
                           'QPushButton:hover{background-color:#8F00A3DA;}'
                           'QPushButton:checked{background-color:#FFFAAD14;}')

        self.btnInfo = QPushButton('N', self.titleBar)
        self.btnInfo.setFixedSize(24, 24)
        self.btnInfo.setCheckable(True)
        self.horizontalLayout.addWidget(self.btnInfo)
        self.btnInfo.clicked.connect(self.turnOnLineInfo)
        self.verticalLayout.addWidget(self.titleBar)

        pg.setConfigOption('background', QColor(255, 255, 255, 0xFF))
        self.plot = pg.PlotWidget()
        self.plot.setXRange(max=600, min=0)
        self.plot.setYRange(max=5000, min=0)
        self.plot.showGrid(x=True, y=True)  # 显示图形网格
        self.plot.setMenuEnabled(False)

        self.verticalLayout.addWidget(self.plot)
        self.legend = pg.LegendItem((80, 60), offset=(600, 15), verSpacing=-10)
        self.legend.setParentItem(self.plot.getViewBox())
        self.plot.scene().sigMouseMoved.connect(self.onMouseMove)
        self.text = pg.TextItem(anchor=(0.5, 2), angle=0, border='w', fill=(0, 0, 255, 255))
        self.arrow = pg.ArrowItem(pos=(0, 0), angle=-90)
        self.text.hide()
        self.arrow.hide()

    def setVisibleEx(self, isVisible):
        self.setVisible(isVisible)
        self.title.setVisible(isVisible)

    def setLegendOffset(self, offset):
        self.legend.setOffset(offset)

    def turnOnLineInfo(self):
        if self.btnInfo.isChecked():
            #self.btnInfo.setText("关")
            self.plot.addItem(self.text)
            self.plot.addItem(self.arrow)
            for line in self.lineArr:
                if line.property('hide'):
                    continue
                line.setSymbol('o')
        else:
            #self.btnInfo.setText("开")
            self.plot.removeItem(self.text)
            self.plot.removeItem(self.arrow)
            for line in self.lineArr:
                line.setSymbol(None)

    def onMouseMove(self, pos):
        if self.btnInfo.isChecked() is False:
            return

        if self.plot.sceneBoundingRect().contains(pos):
            if len(self.lineArr) == 0:
                return

            pt = self.plot.getViewBox().mapSceneToView(pos)
            index = int(pt.x() * 100)
            temp = ''

            y_degree=self.plot.viewRect().height()/5
            isFirst = True
            for i in range(0, len(self.lineArr)):
                if self.lineArr[i].property('hide'):
                    continue

                xSam, ySam = self.lineArr[i].getData()
                if xSam is None or len(xSam) < 10:
                    continue

                if isFirst:
                    isFirst = False
                    index = index - int((xSam[0] + 0.0001) * 100)

                if 0 <= index < len(xSam):
                    if pt.y() - y_degree <= ySam[index] <= pt.y() + y_degree:
                        temp = f'{xSam[index]:0.2f}, {ySam[index]:0.2f}'
                        break

            if globalvar.isStrNoneOrEmpty(temp):
                self.text.hide()
                self.arrow.hide()

            else:
                self.text.show()
                self.arrow.show()
                self.text.setText(temp)
                self.arrow.setPos(xSam[index], ySam[index])
                self.text.setPos(xSam[index], ySam[index])

    def addNewLine(self, isLegend=True, info=None):
        # arr = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'd', 'l', 's']
        _len = len(self.lineArr)
        arr = [(100, 149, 237), (255, 165, 0), (255, 62, 150), (0, 0, 205), (50, 205, 50),
               (147, 112, 219), (130, 57, 53), (78, 119, 69), (255, 99, 71), (193, 205, 193)]
        color = arr[_len % len(arr)]
        line = self.plot.plot(pen={'color': color, 'width': 2}, symbolBrush=color, symbol=None, symbolSize=6)
        self.lineArr.append(line)
        if isLegend:  # 加图例
            if info is None:
                name = '初始' if _len == 0 else f'样品{_len}'
                self.legend.addItem(self.lineArr[-1], name)
                self.lineArr[-1].setProperty('name', name)
                self.lineArr[-1].setProperty('thick', None)
                self.lineArr[-1].setProperty('hide', False)
            else:
                self.legend.addItem(self.lineArr[-1], info[0])
                self.lineArr[-1].setProperty('name', info[0])
                self.lineArr[-1].setProperty('thick', info[1])
                self.lineArr[-1].setProperty('hide', info[2])

    def onBtnClicked(self, btn):
        if btn == self.btn1:
            print(btn.text())
            if btn.isChecked():
                self.btn3.setEnabled(True)
                self.plot.getViewBox().setMouseMode(pg.ViewBox.RectMode)
            else:
                self.btn3.setEnabled(False)
                self.btn3.setChecked(False)
                self.plot.getViewBox().setMouseMode(pg.ViewBox.PanMode)
                self.plot.setMouseEnabled(x=False, y=False)
                self.plot.enableAutoRange()
        elif btn == self.btn2:
            # if btn.isChecked():
            #    self.line1 = self.plot.plot(clear=True, symbolBrush=(255, 0, 0), antialias=True, symbolPen='w', pen='r')
            #    self.line2 = self.plot.plot(symbolBrush=(0, 0, 255), antialias=True, symbolPen='w', pen='g')
            # else:
            #    self.line1 = self.plot.plot(clear=True, pen='r')
            #    self.line2 = self.plot.plot(pen='g')
            # self.line1.setData(self.x, self.y, )
            # self.line2.setData(self.x1, self.y1, )
            pass
        else:
            if btn.isChecked():
                if self.btn1.isChecked():
                    self.plot.getViewBox().setMouseMode(pg.ViewBox.PanMode)
                self.plot.setMouseEnabled(x=True, y=True)
            else:
                if self.btn1.isChecked():
                    self.plot.getViewBox().setMouseMode(pg.ViewBox.RectMode)
                self.plot.setMouseEnabled(x=False, y=False)

    def resetView(self):
        self.plot.autoBtnClicked()

    def setCurveHide(self, index, isHide):
        if isHide is True:
            self.lineArr[index].opts['pen'] = None
        else:
            arr = [(100, 149, 237), (255, 165, 0), (255, 62, 150), (0, 0, 205), (50, 205, 50),
                   (147, 112, 219), (130, 57, 53), (78, 119, 69), (255, 99, 71), (193, 205, 193)]
            color = arr[index % len(arr)]
            self.lineArr[index].opts['pen'] = {'color': color, 'width': 2}
            self.lineArr[index].opts['symbolBrush'] = color
        self.lineArr[index].updateItems()

    def setChartInfo(self, title, xAxis, yAxis):
        self.title.setText(title)
        self.plot.setLabel(axis='left', text=yAxis)
        self.plot.setLabel(axis='bottom', text=xAxis)

    def setChartTitle(self, title):
        self.title.setText(title)

    def setChartRange(self, xMin, xMax, yMin, yMax):
        self.plot.setXRange(max=xMax, min=xMin)
        self.plot.setYRange(max=yMax, min=yMin)

    def clearLine(self, index=8080):
        self.x.clear()
        self.y.clear()

        rLen = len(self.lineArr)
        if rLen == 0 or index >= rLen or index < -rLen:
            for l in self.lineArr:
                l.clear()
            self.lineArr.clear()
            self.legend.clear()
            self.plot.clear()
            self.btnInfo.setChecked(False)
            self.turnOnLineInfo()
        else:
            self.legend.removeItem(self.lineArr[index])
            self.plot.removeItem(self.lineArr[index])
            del self.lineArr[index]

    def updateLine(self, index, x, y):
        rLen = len(self.lineArr)
        if rLen == 0 or index >= rLen or index < -rLen:
            return None

        if isinstance(x, int) or \
                isinstance(x, float):  # 单个点
            self.x.append(x)
            self.y.append(y)
        elif isinstance(x, np.ndarray):  # 点集
            self.x = list(x)
            self.y = list(y)
        elif isinstance(x, list):  # 点集
            self.x = x
            self.y = y
        else:
            return None

        self.lineArr[index].setData(self.x, self.y)

    def getAnalysisData(self, index):
        rLen = len(self.lineArr)
        if rLen == 0 or index >= rLen or index < -rLen:
            return None

        xRef, yRef = self.lineArr[0].getData()
        xSam, ySam = self.lineArr[index].getData()
        if (ySam is None) or len(xRef) == 0 or len(yRef) == 0 or \
                len(ySam) == 0 or len(ySam) != len(yRef):
            return None
        return [xRef, yRef, ySam]

    def getLineData(self, index):
        rLen = len(self.lineArr)
        if rLen == 0 or index >= rLen or index < -rLen:
            return None

        xArr, yArr = self.lineArr[index].getData()
        return [xArr, yArr]

    def getData(self):
        data = {'y': []}
        size = self.getLineCount()
        for i in range(size):
            x, y = self.lineArr[i].getData()
            if i == 0:
                data['x'] = list(x)
            temp = {'name': self.lineArr[i].property('name'),
                    'thick': self.lineArr[i].property('thick'),
                    'hide': self.lineArr[i].property('hide'),
                    'data': list(y)}
            data['y'].append(temp)
        return data

    def isDataEnable(self):
        if len(self.lineArr) == 0:
            return False
        xRef, yRef = self.lineArr[0].getData()
        return xRef is not None and len(xRef) >= 10

    def isSamEnable(self):
        if len(self.lineArr) >= 2:
            return True
        else:
            return False

    def getLineCount(self):
        return len(self.lineArr)

    def clipLines(self, si, ei):
        count = self.getLineCount()
        for i in range(count):
            xArr, yArr = self.lineArr[i].getData()
            self.x = list(xArr[si:ei])
            self.y = list(yArr[si:ei])
            self.lineArr[i].setData(self.x, self.y)

