import math
import struct
import numpy
import datetime
import pyqtgraph as pg
import globalvar as gl
from AppData import *
from Entity.models import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ThirdLib.Algorithm import *
from ThirdLib.AlgImageAlgorithem import *
from Pages.SaveDialog import SaveDialog
from Ui.UiThzCxPage import Ui_UiThzCxPage
from Common.LineChart import LineChart
from Common.MessageBoxEx import MessageBoxEx
from Common.LoadingWidget import LoadingWidget
from Pages.My3DView import My3DView
import json


class ThzCxPage(QWidget, Ui_UiThzCxPage):
    signalNotify = pyqtSignal(QWidget, int, object)

    def __init__(self, parent=None):
        super(ThzCxPage, self).__init__(parent)
        self.setupUi(self)
        self.retranslateUi(self)
        pg.setConfigOption('background', QColor(255, 255, 255, 255))
        pg.setConfigOption('imageAxisOrder', 'row-major')
        self.item1 = pg.ImageItem()
        self.bar1, self.plot1, chart1 = self.AddTabContent(self.item1, self.tabLayout1, self.cbxColor1)
        self.item2 = pg.ImageItem()
        self.item1.hoverEvent = self.onMouseHover1
        self.item2.hoverEvent = self.onMouseHover2
        self.createExternalChart(chart1)
        self.bar2, self.plot2, chart2 = self.AddTabContent(self.item2, self.tabLayout3, self.cbxColor2)
        self.item3d = My3DView()
        self.tabLayout2.addWidget(self.item3d)
        self.workFlow = SysConf.cxFlow
        self.workFlow.asyncNotify = self.signalNotify
        self.disableAllBtn()
        self.btnOpenDev.setEnabled(True)
        self.ledBtn1.setText("激光器")
        self.ledBtn2.setText("偏压源")
        self.ledBtn3.setText("快延迟线")
        self.ledBtn4.setText("扫描电机")
        self.cbxScanArr.setView(QListView())
        self.cbxNumArr.setView(QListView())
        self.signalNotify.connect(self.signalNotifyProc)
        self.btnWaitTime.clicked.connect(self.onBtnWaitTime)
        arr = ['cool', 'gray', 'hot', 'hsv', 'jet', 'parula', 'spring', 'summer']
        for _iter in arr:
            self.cbxColor1.addItem(_iter)
            self.cbxColor2.addItem(_iter)
            self.cbxColor3.addItem(_iter)

        self.cbxColor1.setCurrentIndex(3)
        self.cbxColor2.setCurrentIndex(3)
        self.cbxColor3.setCurrentIndex(3)
        self.cbxColor1.currentTextChanged.connect(self.onTextChanged1)
        self.cbxColor2.currentTextChanged.connect(self.onTextChanged2)
        self.cbxColor3.currentTextChanged.connect(self.onTextChanged3)
        self.ledBtn3.hide()
        self.label_18.hide()
        self.cbxScanArr.hide()

    def createExternalChart(self, parent):
        vLayout = QVBoxLayout(parent)
        vLayout.setContentsMargins(0, 0, 0, 0)
        vSpacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        vLayout.addItem(vSpacer1)
        hLayout = QHBoxLayout()
        hSpacer1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        hLayout.addItem(hSpacer1)

        self.btnShow = QPushButton(parent)
        self.btnShow.setFixedSize(32, 32)
        self.btnShow.setStyleSheet("QPushButton{border-image: url(:/Image/linemax_white.png)}")
        self.btnShow.clicked.connect(self.btnLineVisible)
        hLayout.addWidget(self.btnShow)

        self.chart1 = LineChart(parent)
        self.chart1.setFixedSize(500, 400)
        self.chart1.setChartInfo("               二维曲线图表", "", "")
        self.chart1.setChartRange(0, 100, 0, 100)
        self.chart1.setVisible(False)
        self.btnHide = QPushButton(self.chart1)
        self.btnHide.setFixedSize(32, 32)
        self.btnHide.setStyleSheet("QPushButton{border-image: url(:/Image/linemin_white.png)}")
        self.btnHide.clicked.connect(self.btnLineHide)
        hLayout.addWidget(self.chart1)

        hSpacer2 = QSpacerItem(85, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        hLayout.addItem(hSpacer2)
        vLayout.addLayout(hLayout)
        vSpacer2 = QSpacerItem(20, 29, QSizePolicy.Minimum, QSizePolicy.Fixed)
        vLayout.addItem(vSpacer2)

    def btnLineVisible(self):
        self.btnShow.setVisible(False)
        self.chart1.setVisible(True)

    def btnLineHide(self):
        self.btnShow.setVisible(True)
        self.chart1.setVisible(False)

    def onTextChanged1(self, text):
        file = f'config/color/{text}.json'
        clrMap = self.loadColorBar(text, file)
        self.bar1.setColorMap(clrMap)

    def onTextChanged2(self, text):
        pass

    def onTextChanged3(self, text):
        file = f'config/color/{text}.json'
        clrMap = self.loadColorBar(text, file)
        self.bar2.setColorMap(clrMap)

    def loadColorBar(self, text, file):
        if os.path.exists(file):
            with open(file, "r", encoding='utf-8') as f:
                color_list = json.load(f, object_hook=SysConf.convertBack)

        if color_list is None or len(color_list) == 0:
            return pg.colormap.get('CET-L9')

        return pg.ColorMap(name=text,
                           pos=numpy.linspace(0.0, 1.0, len(color_list)),
                           color=color_list)

    def onBtnWaitTime(self):
        self.txtWaitTime.setEnabled(self.btnWaitTime.isChecked())
        SysConf.appData.cxMode.stepMove = self.btnWaitTime.isChecked()

    def AddTabContent(self, item, layout, cbxColor):
        chart = pg.GraphicsLayoutWidget(self, show=True)
        plot = chart.addPlot(title="")
        plot.addItem(item)
        plot.autoBtn.clicked.connect(self.plotRefresh)

        file = f'config/color/hsv.json'
        clrMap = self.loadColorBar('hsv', file)
        bar = pg.ColorBarItem(interactive=False, values=(0, 600), colorMap=clrMap)
        bar.setImageItem(item, insert_in=plot)
        layout.addWidget(chart)
        return bar, plot, chart

    def onMouseHover1(self, event):
        if event.isExit():
            self.plot1.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.item1.image.shape[0] - 1))
        j = int(np.clip(j, 0, self.item1.image.shape[1] - 1))
        val = self.item1.image[i][j]
        ppos = self.item1.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.plot1.setTitle(f"x = {x:.1f} y = {y:.1f} value = {val:.3f}")

    def onMouseHover2(self, event):
        if event.isExit():
            self.plot2.setTitle("")
            return
        pos = event.pos()
        i, j = pos.y(), pos.x()
        i = int(np.clip(i, 0, self.item2.image.shape[0] - 1))
        j = int(np.clip(j, 0, self.item2.image.shape[1] - 1))
        val = self.item2.image[i][j]
        ppos = self.item2.mapToParent(pos)
        x, y = ppos.x(), ppos.y()
        self.plot2.setTitle(f"x = {x:.1f} y = {y:.1f} value = {val:.3f}")

    def contentResize(self):
        self.tabWidget.setGeometry(0, 0, self.graphwidget.width(), self.graphwidget.height())

    def disableAllBtn(self):
        self.on_btnInit_clicked()
        self.btnOpenDev.setEnabled(False)
        self.btnInit.setEnabled(False)
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(False)
        self.btnSave.setEnabled(False)
        # self.btnImport.setEnabled(False)

    @pyqtSlot()
    def on_btnOpenDev_clicked(self):
        print('开启硬件')
        self.disableAllBtn()
        if SysConf.appData.cxMode.isDeviceOn:
            action = self.closeProc
            self.btnOpenDev.setText('正在关闭硬件')
        else:
            action = self.openProc
            self.btnOpenDev.setText('正在开启硬件')

        thread = threading.Thread(target=action)
        thread.start()

    def onOpenDevOver(self, code):
        if code == gl.SUCCESS:
            self.btnOpenDev.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            SysConf.appData.cxMode.isDeviceOn = True
            self.btnStart.setEnabled(True)
            self.btnOpenDev.setEnabled(True)
            self.btnInit.setEnabled(True)
            self.btnOpenDev.setText('关闭硬件')
            MessageBoxEx.show('成像设备开启成功!')
        else:
            self.btnStart.setEnabled(False)
            self.btnOpenDev.setEnabled(True)
            self.btnImport.setEnabled(True)
            self.btnOpenDev.setText('开启硬件')
            MessageBoxEx.show(f'打开设备失败，错误代码{code}!')

    def onCloseDevOver(self, code):
        if code == gl.SUCCESS:
            print('成像光谱设备关闭成功！')
        else:
            print('成像光谱设备关闭失败！')
        SysConf.appData.cxMode.isDeviceOn = False
        self.btnOpenDev.setEnabled(True)
        self.btnImport.setEnabled(True)
        self.btnStart.setEnabled(False)
        self.btnOpenDev.setText('开启硬件')
        self.btnOpenDev.setStyleSheet(
            'QPushButton{background-color:#FF00A3DA;border:none;} QPushButton:hover{background-color:#8F00A3DA;}')

    @pyqtSlot()
    def on_btnInit_clicked(self):
        self.cbxScanArr.clear()
        for item in SysConf.devCxMode.kuaiYan.scanArr:
            self.cbxScanArr.addItem(f'频率:{item.freq}Hz / 扫描时间范围:{item.time}ps', item)

        self.cbxNumArr.clear()
        for item in SysConf.devCxMode.kuaiYan.RefDivideFreqArr:
            self.cbxNumArr.addItem(item)

        self.item1.clear()
        self.item2.clear()
        self.workFlow.samArr.clear()
        self.btnStart.setEnabled(True)
        self.txtWaitTime.setText(f'{SysConf.appData.cxMode.stepTime}')
        self.txtXStart.setText(f'{SysConf.appData.cxMode.xStart}')
        self.txtXEnd.setText(f'{SysConf.appData.cxMode.xEnd}')
        self.txtXStep.setText(f'{SysConf.appData.cxMode.xStep}')
        self.txtYStart.setText(f'{SysConf.appData.cxMode.yStart}')
        self.txtYEnd.setText(f'{SysConf.appData.cxMode.yEnd}')
        self.txtYStep.setText(f'{SysConf.appData.cxMode.yStep}')
        self.txtAngle.setText(f'{SysConf.appData.cxMode.angle}')
        self.txtRefraction.setText(f'{SysConf.appData.cxMode.refraction}')
        self.txtScanTime.setText('0')
        self.cbxScanArr.setCurrentIndex(SysConf.devCxMode.kuaiYan.index)
        self.cbxNumArr.setCurrentIndex(SysConf.devCxMode.kuaiYan.freqDivision)

    @pyqtSlot()
    def on_btnStart_clicked(self):
        if gl.isStrNoneOrEmpty(self.txtXStart.text()) \
                or gl.isStrNoneOrEmpty(self.txtXEnd.text()) \
                or gl.isStrNoneOrEmpty(self.txtXStep.text()) \
                or gl.isStrNoneOrEmpty(self.txtYStart.text()) \
                or gl.isStrNoneOrEmpty(self.txtYEnd.text()) \
                or gl.isStrNoneOrEmpty(self.txtYStep.text()) \
                or gl.isStrNoneOrEmpty(self.txtAngle.text()) \
                or gl.isStrNoneOrEmpty(self.txtRefraction.text()):
            MessageBoxEx.show('参数未填写完整，请填写完整！')
            return
        self.chart1.clearLine()
        self.chart1.addNewLine(True, None)
        SysConf.appData.cxMode.xStart = float(self.txtXStart.text())
        SysConf.appData.cxMode.xEnd = float(self.txtXEnd.text())
        SysConf.appData.cxMode.xStep = float(self.txtXStep.text())
        SysConf.appData.cxMode.yStart = float(self.txtYStart.text())
        SysConf.appData.cxMode.yEnd = float(self.txtYEnd.text())
        SysConf.appData.cxMode.yStep = float(self.txtYStep.text())
        SysConf.appData.cxMode.angle = float(self.txtAngle.text())
        SysConf.appData.cxMode.refraction = float(self.txtRefraction.text())
        SysConf.devCxMode.kuaiYan.index = self.cbxScanArr.currentIndex()
        SysConf.devCxMode.kuaiYan.freqDivision = self.cbxNumArr.currentIndex()
        self.cbxNumArr.setCurrentIndex(SysConf.devCxMode.kuaiYan.freqDivision)
        datalen=(SysConf.appData.cxMode.xEnd-SysConf.appData.cxMode.xStart)*(SysConf.appData.cxMode.yEnd-SysConf.appData.cxMode.yStart)/SysConf.appData.cxMode.xStep/SysConf.appData.cxMode.yStep/SysConf.devCxMode.compress_signal
        # if datalen*SysConf.devCxMode.kuaiYan.getSampleNumber()*2>200000000:
        #     fp=math.ceil((datalen*SysConf.devCxMode.kuaiYan.getSampleNumber()*2/200000000))
        #     MessageBoxEx.show('数据量太大，需要采集点数<=1/{0}'.format(fp))
        #     return
        self.plotRefresh()
        if SysConf.appData.cxMode.xStart >= SysConf.appData.cxMode.xEnd \
                or SysConf.appData.cxMode.xStep == 0 or SysConf.appData.cxMode.xEnd == 0 \
                or SysConf.appData.cxMode.yStart >= SysConf.appData.cxMode.yEnd \
                or SysConf.appData.cxMode.yStep == 0 or SysConf.appData.cxMode.yEnd == 0:
            MessageBoxEx.show('参数填写不正确，请正确填写参数！')
            return

        self.disableAllBtn()
        self.btnStop.setEnabled(True)
        self.btnStart.setText('正在采集')

        self.plotTransformSet()
        thread = threading.Thread(target=self.collProc)
        thread.start()

    def plotTransformSet(self):
        tr = QTransform()
        xOffset = SysConf.appData.cxMode.xStart / SysConf.appData.cxMode.xStep
        yOffset = SysConf.appData.cxMode.yStart / SysConf.appData.cxMode.yStep
        tr.scale(SysConf.appData.cxMode.xStep, SysConf.appData.cxMode.yStep)
        tr.translate(xOffset, yOffset)
        self.item1.setTransform(tr)
        self.item2.setTransform(tr)

    def plotRefresh(self):
        x = SysConf.appData.cxMode.xStart
        y = SysConf.appData.cxMode.yStart
        w = SysConf.appData.cxMode.xEnd - x
        h = SysConf.appData.cxMode.yEnd - y

        ratio = self.plot1.getViewBox().width() / self.plot1.getViewBox().height()
        if w / h > ratio:
            h = w / ratio
        else:
            w = h * ratio
        self.plot1.setXRange(x, x + w)
        self.plot1.setYRange(y, y + h)
        self.plot2.setXRange(x, x + w)
        self.plot2.setYRange(y, y + h)

    @pyqtSlot()
    def on_btnStop_clicked(self):
        print('中断采集')
        gl.set()
        self.workFlow.decoder.stop()

    def onCollDataOver(self, code):
        self.btnStart.setText('开始采集')
        self.btnOpenDev.setEnabled(True)
        self.btnInit.setEnabled(True)
        self.btnStart.setEnabled(True)
        self.btnStop.setEnabled(False)
        if code == gl.SUCCESS:
            print('数据采集完成！')

            if self.workFlow.signalAll.shape[0]== 0:
                MessageBoxEx.show('成像扫描未采集到数据！')
                return

            self.btnSave.setEnabled(True)
            r = MessageBoxEx.show('成像数据采集完成,继续解码计算生成图片(解码计算\n将用较长时间)？', "温馨提示", '是', '否')
            if QDialog.Accepted != r:
                return

            # if SysConf.appData.cxMode.isPeakTrough is False \
            #         and SysConf.appData.cxMode.isSection is False \
            #         and SysConf.appData.cxMode.isSection is False:
            #     return
            thread = threading.Thread(target=self.analysisProc)
            thread.start()
            self.load = LoadingWidget('成像数据分析计算中，请稍后...')
            self.load.showDialog()
        elif code == gl.MANUAL_EXIT:
            MessageBoxEx.show('成像数据采集已中断！')
        else:
            print(f'成像数据采集失败，错误代码：{code}')

    @pyqtSlot()
    def on_btnSave_clicked(self):
        if self.workFlow.isDataEnable() is False:
            MessageBoxEx.show('数据未解码完成请等待！')

        dlg = SaveDialog()
        if dlg.showDialog() is False:
            return

        dt = CXData()
        dt.XStart = SysConf.appData.cxMode.xStart
        dt.XStep = SysConf.appData.cxMode.xStep
        dt.XEnd = SysConf.appData.cxMode.xEnd
        dt.YStart = SysConf.appData.cxMode.yStart
        dt.YStep = SysConf.appData.cxMode.yStep
        dt.YEnd = SysConf.appData.cxMode.yEnd
        dt.Angle = SysConf.appData.cxMode.angle
        dt.Refraction = SysConf.appData.cxMode.refraction
        dt.Index = SysConf.devCxMode.kuaiYan.index
        dt.DivFreq = SysConf.devCxMode.kuaiYan.freqDivision
        dt.SampleType = dlg.txtType.currentText()
        dt.SampleName = dlg.txtName.text()
        dt.SampleTypeID = dlg.txtType.property('id')
        dt.Operator = SysConf.appData.loginUser
        dt.AddDate = datetime.datetime.now()
        dt.save()
        dt.FilePath = f'./data/CX_{dt.Id}_{dt.SampleName}.qda'
        dt.save()

        nLen = 1 + len(dt.SampleName.encode('utf8'))
        tLen = 1 + len(dt.SampleType.encode('utf8'))
        try:
            ff = f"8f2iq{nLen}p{tLen}p"
            with open(dt.FilePath, 'w+b') as f:
                var = struct.pack(ff, dt.XStart, dt.XStep, dt.XEnd, dt.YStart, dt.YStep, dt.YEnd,
                                  dt.Angle, dt.Refraction, dt.Index, dt.DivFreq, dt.SampleTypeID,
                                  dt.SampleName.encode('utf8'), dt.SampleType.encode('utf8'))
                f.write(var)
                # for i in self.workFlow.samArr:
                #     f.write(bytes(i))
                #     f.flush()
                signalAll=self.workFlow.signalAll.flatten()
                # bs = struct.pack('d' * len(signalAll), *signalAll)
                # for i in bs:
                blen=2000000
                for i in range(400):
                    if len(signalAll)<=i*blen:
                        break
                    ss=signalAll[i*blen:i*blen+blen]
                    bs = struct.pack('d' * len(ss), *ss)
                    f.write(bs)
                f.flush()
                # f.write(struct.pack('5i', nLen, tLen, len(var), len(self.workFlow.samArr[0]), len(self.workFlow.samArr)))
                f.write(struct.pack('4i', nLen, tLen, len(var),  len(signalAll)))
        except Exception as err:
            pass

    @pyqtSlot()
    def on_btnImport_clicked(self):
        fileName, _type = QFileDialog.getOpenFileName(caption='选择成像数据文件', filter='成像数据(*.qda);;All Files (*)')

        if gl.isFileExist(fileName) is False:
            return

        thread = threading.Thread(target=self.loadDataProc, args=[1, fileName])
        thread.start()
        self.load = LoadingWidget('成像数据分析计算中，请稍后...')
        self.load.showDialog()

    def displayData(self, dat):
        SysConf.appData.cxMode.xStart = dat.XStart
        SysConf.appData.cxMode.xStep = dat.XStep
        SysConf.appData.cxMode.xEnd = dat.XEnd
        SysConf.appData.cxMode.yStart = dat.YStart
        SysConf.appData.cxMode.yStep = dat.YStep
        SysConf.appData.cxMode.yEnd = dat.YEnd
        SysConf.appData.cxMode.angle = dat.Angle
        SysConf.appData.cxMode.refraction = dat.Refraction
        SysConf.devCxMode.kuaiYan.index = dat.Index
        SysConf.devCxMode.kuaiYan.freqDivision = dat.DivFreq
        self.setProperty('name', dat.SampleName)
        self.setProperty('type', dat.SampleType)
        self.setProperty('typeId', dat.SampleTypeID)
        self.on_btnInit_clicked()
        thread = threading.Thread(target=self.loadDataProc, args=[0, dat.FilePath])
        thread.start()
        self.load = LoadingWidget('成像数据分析计算中，请稍后...')
        self.load.showDialog()

    def loadDataProc(self, mode, fileName,current=False):
        compress_signal = SysConf.devCxMode.compress_signal
        # 计算并更新图片
        if current:
            # dataArr=self.workFlow.samArr
            signalAll = self.workFlow.signalAll
        else:
            dataArr = []
            with open(fileName, "rb") as f:
                f.seek(-16, 2)
                buff = f.read(16)
                var = struct.unpack('4i', buff)
                f.seek(0, 0)
                buff = f.read(var[2])
                param = struct.unpack(f'8f2iq{var[0]}p{var[1]}p', buff)
                f.seek(var[2], 0)
                # for i in range(var[4]):
                #     dataArr.append(f.read(var[3]))
                SysConf.devCxMode.kuaiYan.index = param[8]
                SysConf.devCxMode.kuaiYan.freqDivision = param[9]
                num=int(SysConf.devCxMode.kuaiYan.getSampleNumber()/compress_signal+2)
                buff=f.read(var[3]*8)
                signalAll=np.array(struct.unpack('d'*(var[3]),buff))
                signalAll=np.asarray(signalAll).reshape(num, int(signalAll.shape[0]/num))
            # if len(dataArr) != var[4]:
            #     self.signalNotify.emit(None, 3010, None)
            #     return

        if mode == 1:
            SysConf.appData.cxMode.xStart = param[0]
            SysConf.appData.cxMode.xStep = round(param[1], 2)
            SysConf.appData.cxMode.xEnd = param[2]
            SysConf.appData.cxMode.yStart = param[3]
            SysConf.appData.cxMode.yStep = round(param[4], 2)
            SysConf.appData.cxMode.yEnd = param[5]
            SysConf.appData.cxMode.angle = param[6]
            SysConf.appData.cxMode.refraction = param[7]
            SysConf.devCxMode.kuaiYan.index = param[8]
            SysConf.devCxMode.kuaiYan.freqDivision = param[9]
            self.setProperty('typeId', param[10])
            self.setProperty('name', param[11])
            self.setProperty('type', param[12])
            self.signalNotify.emit(None, 3011, None)
        self.signalNotify.emit(None, 3013, None)

        self.robot = 0
        if self.robot == 0:
            pvData, thkData = Algorithm.cx_calcPVAndThick1(SysConf.appData.cxMode, SysConf.devCxMode, signalAll)
        else:
            pvData, thkData = robotPPThick(signalAll,int(signalAll[1, 0]))

        t = np.array(
            Algorithm.get_times(SysConf.devCxMode.kuaiYan.getPs(), int(SysConf.devCxMode.kuaiYan.getSampleNumber()/compress_signal)))
        params = [SysConf.appData.cxMode.xStart, SysConf.appData.cxMode.xStep, SysConf.appData.cxMode.xEnd, SysConf.appData.cxMode.yStart
            , SysConf.appData.cxMode.yStep, SysConf.appData.cxMode.yEnd, 1,int(SysConf.devCxMode.kuaiYan.getSampleNumber()/compress_signal), signalAll, t]

        self.signalNotify.emit(None, 3009, (pvData, thkData))
        self.signalNotify.emit(None, 3031,params)
        self.signalNotify.emit(None, 3012, None)
    def openProc(self):
        gl.reset()
        code = self.workFlow.turnOn()
        gl.set()
        self.signalNotify.emit(None, 3000, code)

    def closeProc(self):
        gl.reset()
        code = self.workFlow.turnOff()
        gl.set()
        self.signalNotify.emit(None, 3001, code)

    def collProc(self):
        gl.reset()
        code = self.workFlow.collRun()
        gl.set()
        self.signalNotify.emit(None, 3002, code)

    def analysisProc(self):
        self.loadDataProc(0,None,True)
        # if SysConf.appData.cxMode.isPeakTrough:
        #     pass
        # if SysConf.appData.cxMode.isSection:
        #     pass
        # if SysConf.appData.cxMode.isThickness:
        #     pass

    def signalNotifyProc(self, widget, mode, value):
        if mode == 3000:
            self.onOpenDevOver(value)
        elif mode == 3001:
            self.onCloseDevOver(value)
        elif mode == 3002:
            self.onCollDataOver(value)
        elif mode == 3003:
            self.ledBtn1.setState(value)
        elif mode == 3004:
            self.ledBtn2.setState(value)
        elif mode == 3005:
            self.ledBtn3.setState(value)
        elif mode == 3006:
            self.ledBtn4.setState(value)
        elif mode == 3007:
            self.txtScanTime.setText(f'{value:.1f}')
        elif mode == 3008:
            self.txtLaserHz.setText(f'{value:.1f}')
        elif mode == 3009:
            ThzCxPage.updateImageChart(self.item1, self.bar1, value[0])
            ThzCxPage.updateImageChart(self.item2, self.bar2, value[1])
            if len(value)>=4:
                self.chart1.updateLine(0,value[2],value[3])
        elif mode == 3010:
            MessageBoxEx.show('成像数据文件打开失败！')
        elif mode == 3011:
            self.on_btnInit_clicked()
        elif mode==3013:
            self.plotRefresh()
            self.plotTransformSet()
        elif mode == 3031:
            self.item3d.initParams(value,self.robot)
            # self.item3d.initParams(value)
            # self.item3d.running1()
            # cxmode=SysConf.appData.cxMode
            # d=[]
            # for v in value:
            #     d.extend(v)
            # params = [cxmode.xStart, cxmode.xStep, cxmode.xEnd, cxmode.yStart, cxmode.yStep, cxmode.yEnd, 1, SysConf.devCxMode.kuaiYan.getSampleNumber(), d, 2**SysConf.devCxMode.kuaiYan.freqDivision]
            #
            # self.item3d.initParams(params)
            # self.item3d.running()
        elif mode == 3012:
            self.load.close()
            del self.load
        else:
            pass

    @staticmethod
    def updateImageChart(item, bar, data):
        try:
            data = np.array(data)

            if data.shape[0] <= 0:
                return
            _min = data.min()
            _max = data.max()
            _len = data.ptp()
            if abs(_len) < 0.1:
                _min = _min - 125
                if _min < 0:
                    _min = 0
                _max = _min + 255
            bar.setLevels((int(_min), int(_max)))
            item.setImage(np.array(data), False)
        except Exception as err:
            pass
