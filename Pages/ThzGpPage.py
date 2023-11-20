import datetime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Core.WorkFlow import *
from Entity.models import *
from ThirdLib.Algorithm import *
from Ui.UiThzGpPage import Ui_UiThzGpPage
from Common.DialogEx import DialogEx
from Common.MessageBoxEx import MessageBoxEx
from Common.LineChart import LineChart
from Pages.SaveDialog import SaveDialog
from Pages.LineEditDialog import LineEditDialog
from Pages.DataEditDialog import DataEditDialog
from Pages.GpSetMoreDialog import GpSetMoreDialog


class ThzGpPage(QWidget, Ui_UiThzGpPage):
    signalNotify = pyqtSignal(QWidget, int, object)

    def __init__(self, parent=None):
        super(ThzGpPage, self).__init__(parent)
        self.thread = None
        self.setupUi(self)
        self.isSamSuccess = False
        self.retranslateUi(self)
        self.workFlow = SysConf.gpFlow
        SysConf.appData.isFastScan = False
        self.signalNotify.connect(self.signalNotifyProc)
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.verticalLayout2.setContentsMargins(9, 9, 9, 9)
        self.buttonGroup.setExclusive(True)
        self.ledBtn1.setText("激光器")
        self.ledBtn2.setText("偏压源")
        self.ledBtn3.setText("锁项")
        self.ledBtn4.setText("激光器")
        self.ledBtn5.setText("偏压源")
        self.ledBtn6.setText("快延迟线")
        self.ledBtn7.setText("扫描电机")
        self.gridLayout = QGridLayout(self.chartWidget)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setContentsMargins(0, 0, 0, -1)

        self.chart1 = LineChart(self.chartWidget)
        self.chart1.setChartInfo("时域波形(极值差为 0 mV)", "位置(ps)", "幅值(mV)")
        self.chart1.setChartRange(0, 600, -10, 10)

        self.chart2 = LineChart(self.chartWidget)
        self.chart2.setChartInfo("频域波形", "频率(THz)", "幅值(dB)")
        self.chart2.setChartRange(0, 10, -60, 0)

        self.chart3 = LineChart(self.chartWidget)
        self.chart3.setVisible(False)
        self.chart3.setChartInfo("折射率", "频率(THz)", " ")
        self.chart3.setChartRange(0, 10, 0, 10)

        self.chart4 = LineChart(self.chartWidget)
        self.chart4.setVisible(False)
        self.chart4.setChartInfo("吸收系数", "频率(THz)", "1/cm")
        self.chart4.setChartRange(0, 10, -20, 20)
        self.cbxScanArr.setView(QListView())
        self.cbxNumArr.setView(QListView())
        self.txtScanTime.setValidator(QIntValidator(0, 2000, self))
        self.buttonGroup.buttonClicked.connect(lambda data: self.onScanModelSel(data))
        self.btnGpAuto.clicked.connect(self.onBtnAutoAnalysis)
        self.btnCxAuto.clicked.connect(self.onBtnAutoAnalysis)
        self.btnGpEdit.clicked.connect(self.onBtnLineEdit)
        self.btnCxEdit.clicked.connect(self.onBtnLineEdit)
        self.btnGpAnalysis.clicked.connect(self.onBtnAnalysis)
        self.btnCxAnalysis.clicked.connect(self.onBtnAnalysis)
        for item in SysConf.devCxMode.kuaiYan.scanArr:
            self.cbxScanArr.addItem(f'频率:{item.freq}Hz / 扫描时间范围:{item.time}ps', item)

        for item in SysConf.devCxMode.kuaiYan.RefDivideFreqArr:
            self.cbxNumArr.addItem(item)
        self.BtnGPEnable()
        self.BtnCGEnable()
        if SysConf.appData.gpMode.isAutoAnalysis:
            self.btnGpAuto.setChecked(True)
            self.on4ChartLayout()
        else:
            self.on2ChartLayout()

    def BtnGPEnable(self):
        self.btnGpOpenDev.setEnabled(True)
        self.btnGpInit.setEnabled(False)
        self.btnGpRef.setEnabled(False)
        self.btnGpSam.setEnabled(False)
        self.btnGpStop.setEnabled(False)
        self.btnGpSave.setEnabled(False)
        self.btnGpEdit.setEnabled(False)
        self.btnGpImport.setEnabled(True)
        self.btnGpAnalysis.setEnabled(False)
        self.btnGpMore.setEnabled(False)
        self.on_btnGpInit_clicked()

    def BtnCGEnable(self):
        self.btnCxOpenDev.setEnabled(True)
        self.btnCxInit.setEnabled(False)
        self.btnCxRef.setEnabled(False)
        self.btnCxSam.setEnabled(False)
        self.btnCxStop.setEnabled(False)
        self.btnCxSave.setEnabled(False)
        self.btnCxEdit.setEnabled(False)
        self.btnCxImport.setEnabled(True)
        self.btnCxAnalysis.setEnabled(False)
        self.on_btnCxInit_clicked()

    def onScanModelSel(self, btn):
        if btn is self.btnSpectral:
            SysConf.appData.isFastScan = False
            self.gpWidget.setVisible(True)
            self.cxWidget.setVisible(False)
            self.workFlow = SysConf.gpFlow
            if SysConf.appData.gpMode.isAutoAnalysis:
                self.btnGpAuto.setChecked(True)
                self.on4ChartLayout()
            else:
                self.on2ChartLayout()
        else:
            SysConf.appData.isFastScan = True
            self.gpWidget.setVisible(False)
            self.cxWidget.setVisible(True)
            self.workFlow = SysConf.cgFlow
            if SysConf.appData.cgMode.isAutoAnalysis:
                self.btnCxAuto.setChecked(True)
                self.on4ChartLayout()
            else:
                self.on2ChartLayout()

        self.workFlow.calcFreq = self.calFreqProc
        self.workFlow.asyncNotify = self.signalNotify

    def setVisibleModel(self, isGPOk, isCGOk):
        if isGPOk is False:
            self.btnSpectral.setVisible(False)

        if isCGOk is False:
            self.btnImage.setVisible(False)
        elif isGPOk is False:
            self.onScanModelSel(self.btnImage)

    def onBtnAutoAnalysis(self):
        self.gridLayout.removeWidget(self.chart1)
        self.gridLayout.removeWidget(self.chart2)
        self.gridLayout.removeWidget(self.chart3)
        self.gridLayout.removeWidget(self.chart4)
        if SysConf.appData.isFastScan:
            if self.btnCxAuto.isChecked():
                self.on4ChartLayout()
                SysConf.appData.cgMode.isAutoAnalysis = True
                if self.chart1.getLineCount() >= 2:
                    self.onAnalysisLine()
            else:
                self.on2ChartLayout()
                SysConf.appData.cgMode.isAutoAnalysis = False
        else:
            if self.btnGpAuto.isChecked():
                self.on4ChartLayout()
                SysConf.appData.gpMode.isAutoAnalysis = True
            else:
                self.on2ChartLayout()
                SysConf.appData.gpMode.isAutoAnalysis = False

    def onBtnLineEdit(self):
        if self.chart1.isSamEnable() is False:
            return

        dlg = LineEditDialog()
        _len = len(self.chart1.lineArr)
        for i in range(1, _len):
            txtName = QLineEdit(dlg.content)
            txtName.setText(self.chart1.lineArr[i].property('name'))
            dlg.gridLayout.addWidget(txtName, i, 0, 1, 1)
            txtThk = QLineEdit(dlg.content)
            if self.chart1.lineArr[i].property('thick') is not None:
                txtThk.setText(f"{self.chart1.lineArr[i].property('thick')}")
            elif SysConf.appData.isFastScan:
                txtThk.setText(self.txtCxThickness.text())
            else:
                txtThk.setText(self.txtGpThickness.text())
            dlg.gridLayout.addWidget(txtThk, i, 1, 1, 1)
            btnDel = QPushButton('删除', dlg.content)
            btnDel.setFixedSize(56, 26)
            btnDel.setProperty("index", i)
            btnDel.clicked.connect(dlg.delSamLine)
            dlg.gridLayout.addWidget(btnDel, i, 2, 1, 1)
            cbxSel = QCheckBox('', dlg.content)
            if self.chart1.lineArr[i].property('hide') is not None:
                cbxSel.setChecked(self.chart1.lineArr[i].property('hide'))
            dlg.gridLayout.addWidget(cbxSel, i, 3, 1, 1)

        if dlg.showDialog() is False:
            return

        for i in range(1, _len):
            item = dlg.gridLayout.itemAtPosition(_len - i, 0)
            if item is None:
                self.chart1.clearLine(_len - i)
                self.chart2.clearLine(_len - i)
                self.chart3.clearLine(_len - i)
                self.chart4.clearLine(_len - i)
                continue

            name = dlg.gridLayout.itemAtPosition(_len - i, 0).widget().text()
            self.chart1.legend.getLabel(self.chart1.lineArr[_len - i]).setText(name)
            self.chart2.legend.getLabel(self.chart2.lineArr[_len - i]).setText(name)
            self.chart3.legend.getLabel(self.chart3.lineArr[_len - i]).setText(name)
            self.chart4.legend.getLabel(self.chart4.lineArr[_len - i]).setText(name)
            self.chart1.lineArr[_len - i].setProperty('name', name)
            ctrl2 = dlg.gridLayout.itemAtPosition(_len - i, 1).widget()
            self.chart1.lineArr[_len - i].setProperty('thick', ctrl2.text())
            ctrl3 = dlg.gridLayout.itemAtPosition(_len - i, 3).widget()
            self.chart1.lineArr[_len - i].setProperty('hide', ctrl3.isChecked())
            self.setCurveHide(_len - i, ctrl3.isChecked())
        self.chart1.lineArr[_len - i].update()

    def onBtnAnalysis(self):
        if self.chart1.isDataEnable() is False:
            MessageBoxEx.show('当前无数据！')
            return

        ref = self.chart1.getLineData(0)
        if ref is None:
            return
        _min = int(min(ref[0]))
        _max = int(max(ref[0]))

        # 暂存原始数据用于恢复
        origin = []
        size = self.chart1.getLineCount()
        for i in range(size):
            temp = self.chart1.getLineData(i)
            origin.append(temp)

        dlg = DataEditDialog()
        dlg.setRange(_min, _max)
        dlg.onOtherBtnEvent = self.onAnalysisConfirm
        code = dlg.exec_()
        if code == DialogEx.NONE or code == DialogEx.CANCEL:
            self.onAnalysisReset(len(origin[0][0]), size, origin)
        elif code == DialogEx.OK:
            rCode = MessageBoxEx.show('被截的数据将丢失是否继续保存？', '温馨提示', '是', '否')
            if rCode != QDialog.Accepted:
                self.onAnalysisReset(len(origin[0][0]), size, origin)
            else:
                xStart, xEnd = dlg.getRange()
                if SysConf.appData.isFastScan is False:
                    self.txtStart.setText(f'{xStart}')
                    self.txtEnd.setText(f'{xEnd}')
        del origin

    def onAnalysisConfirm(self, start, end):
        ref = self.chart1.getLineData(0)
        si = list(ref[0]).index(start)
        ei = list(ref[0]).index(end)
        if ei == -1:
            ei = len(ref[0])
        else:
            ei += 1
        self.chart1.clipLines(si, ei)
        thread = threading.Thread(target=self.onAnalysisLine)
        thread.start()

    def onAnalysisReset(self, orLen, size, origin):
        newSam = self.chart1.getLineData(0)
        if orLen == len(newSam[0]):
            return

        for i in range(size):
            self.chart1.updateLine(i, origin[i][0], origin[i][1])

        thread = threading.Thread(target=self.onAnalysisLine)
        thread.start()

    def onAnalysisLine(self):
        size = self.chart1.getLineCount()
        for i in range(0, size):
            data = self.chart1.getAnalysisData(i)
            xfArr, yfArr = Algorithm.get_freq(data[0], data[2])
            self.signalNotify.emit(None, 8081, (i, xfArr, yfArr))
            if i == 0:
                continue

            isCxAnalysis = SysConf.appData.isFastScan and SysConf.appData.cgMode.isAutoAnalysis
            isGpAnalysis = SysConf.appData.isFastScan is False and SysConf.appData.gpMode.isAutoAnalysis
            if isGpAnalysis or isCxAnalysis:
                thick = SysConf.appData.cgMode.thickness if SysConf.appData.isFastScan else SysConf.appData.gpMode.thickness
                _freq, _abs, _ref = Algorithm.get_absorption_refractive(data[0], data[1], data[2], thick)
                self.signalNotify.emit(None, 8080, [i, _freq, _abs, _ref])

    def setCurveHide(self, index, isHide):
        self.chart1.setCurveHide(index, isHide)
        self.chart2.setCurveHide(index, isHide)
        self.chart3.setCurveHide(index, isHide)
        self.chart4.setCurveHide(index, isHide)

    def setCurveHide(self, index, isHide):
        self.chart1.setCurveHide(index, isHide)
        self.chart2.setCurveHide(index, isHide)
        self.chart3.setCurveHide(index, isHide)
        self.chart4.setCurveHide(index, isHide)

    def on2ChartLayout(self):
        self.chart3.setVisibleEx(False)
        self.chart4.setVisibleEx(False)
        self.gridLayout.addWidget(self.chart1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.chart2, 1, 0, 1, 1)
        self.chart1.setLegendOffset((800, 5))
        self.chart2.setLegendOffset((800, 5))
        self.chart3.setLegendOffset((800, 5))
        self.chart4.setLegendOffset((800, 5))

    def on4ChartLayout(self):
        self.chart3.setVisibleEx(True)
        self.chart4.setVisibleEx(True)
        self.chart1.setLegendOffset((320, 5))
        self.chart2.setLegendOffset((320, 5))
        self.chart3.setLegendOffset((320, 5))
        self.chart4.setLegendOffset((320, 5))
        self.gridLayout.addWidget(self.chart1, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.chart2, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.chart3, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.chart4, 1, 1, 1, 1)

    def initCharts(self, start, end, _range=10):
        fMax = 6 if _range > 6 else _range
        fMax = 6
        self.chart1.clearLine()
        self.chart1.setChartRange(start, end, -10, 10)
        self.chart2.clearLine()
        self.chart2.setChartRange(0.1, fMax, -60, 0)
        self.chart3.clearLine()
        self.chart3.setChartRange(0, fMax, 0, 10)
        self.chart4.clearLine()
        self.chart4.setChartRange(0, fMax, -20, 20)
        self.addNewLine(None, False)

    def addNewLine(self, info, isSam=True):
        self.chart1.addNewLine(True, info)
        self.chart2.addNewLine(True, info)
        self.chart3.addNewLine(isSam, info)
        self.chart4.addNewLine(isSam, info)

    def importCharts(self, jMap):
        xArr = jMap['x']
        yArr = jMap['y']
        size = len(yArr)
        SysConf.appData.gpMode.samIndex = size - 2
        self.chart1.updateLine(0, xArr, yArr[0]['data'])
        for i in range(1, size):
            self.addNewLine((yArr[i]['name'], yArr[i]['thick'], yArr[i]['hide']))
            self.chart1.updateLine(i, xArr, yArr[i]['data'])
            #self.setCurveHide(i, yArr[i]['hide'])
        thread = threading.Thread(target=self.onAnalysisLine)
        thread.start()

    def resetCharts(self):
        self.chart1.resetView()
        self.chart2.resetView()
        self.chart3.resetView()
        self.chart4.resetView()
    ##############################光谱扫描#################################
    @pyqtSlot()
    def on_btnGpOpenDev_clicked(self):
        print('开启硬件')
        self.btnGpOpenDev.setEnabled(False)
        self.btnGpInit.setEnabled(False)
        self.btnGpRef.setEnabled(False)
        self.btnGpSam.setEnabled(False)
        self.btnGpStop.setEnabled(False)
        self.btnGpSave.setEnabled(False)
        self.btnGpEdit.setEnabled(False)
        self.btnGpImport.setEnabled(False)
        self.btnGpAnalysis.setEnabled(False)
        self.btnGpMore.setEnabled(False)
        if SysConf.appData.cgMode.isDeviceOn:
            action = self.closeProc
            self.btnCxOpenDev.setText('正在关闭硬件')
        else:
            action = self.openProc
            self.btnCxOpenDev.setText('正在开启硬件')

        self.thread = threading.Thread(target=action)
        self.thread.start()

    def onGpOpenDevOver(self, code):
        if code == gl.SUCCESS:
            self.btnGpOpenDev.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            SysConf.appData.cgMode.isDeviceOn = True
            self.btnGpOpenDev.setEnabled(True)
            self.btnGpInit.setEnabled(True)
            self.btnGpRef.setEnabled(False)
            self.btnGpSam.setEnabled(False)
            self.btnGpStop.setEnabled(False)
            self.btnGpSave.setEnabled(False)
            self.btnGpEdit.setEnabled(False)
            self.btnGpImport.setEnabled(True)
            self.btnGpAnalysis.setEnabled(False)
            self.btnGpMore.setEnabled(False)
            self.btnCxOpenDev.setText('关闭硬件')
            MessageBoxEx.show('成像光谱设备开启成功!')
        else:
            self.btnGpOpenDev.setEnabled(True)
            self.btnGpInit.setEnabled(False)
            self.btnGpRef.setEnabled(False)
            self.btnGpSam.setEnabled(False)
            self.btnGpStop.setEnabled(False)
            self.btnGpSave.setEnabled(False)
            self.btnGpEdit.setEnabled(False)
            self.btnGpImport.setEnabled(True)
            self.btnGpAnalysis.setEnabled(False)
            self.btnGpMore.setEnabled(False)
            MessageBoxEx.show(f'打开设备失败，错误代码{code}!')

    def onCxCloseDevOver(self, code):
        if code == gl.SUCCESS:
            print('光谱扫描设备关闭成功！')
        else:
            print('光谱扫描设备关闭失败！')

        self.btnGpOpenDev.setEnabled(True)
        self.btnGpImport.setEnabled(True)
        self.btnGpOpenDev.setText('开启硬件')
        self.btnGpOpenDev.setStyleSheet(
            'QPushButton{background-color:#FF00A3DA;border:none;} QPushButton:hover{background-color:#8F00A3DA;}')

    @pyqtSlot()
    def on_btnGpInit_clicked(self):
        self.txtStart.setText(f'{SysConf.appData.gpMode.start}')
        self.txtEnd.setText(f'{SysConf.appData.gpMode.end}')
        self.txtStep.setText(f'{SysConf.appData.gpMode.step}')
        self.txtGpHz.setText('0')  # 激光器频率
        self.txtNumOfPt.setText('0')  # 数据点个数
        self.txtMaxHz.setText('0')  # 最大频率
        self.txtCurrent.setText('0')  # 当前位置
        self.txtResolution.setText('0')  # 频谱分辨率
        self.txtGpThickness.setText(f'{SysConf.appData.gpMode.thickness}')  # 厚度值

    @pyqtSlot()
    def on_btnGpRef_clicked(self):
        if QDialog.Accepted != MessageBoxEx.show("采集的样品信息将被清除，确定继续操作？", "温馨提示", '是', '否'):
            return
        if self.chart1.isDataEnable() and \
                QDialog.Accepted != MessageBoxEx.show("采集的样品信息将被清除，确定继续操作？", "温馨提示", '是', '否'):
            return

        SysConf.appData.gpMode.start = float(self.txtStart.text())
        SysConf.appData.gpMode.end = float(self.txtEnd.text())
        SysConf.appData.gpMode.step = float(self.txtStep.text())
        if SysConf.appData.gpMode.start >= SysConf.appData.gpMode.end:
            MessageBoxEx.show('起始位置必须小于结束位置！')
            return
        elif SysConf.appData.gpMode.step <= 0:
            MessageBoxEx.show('步长必须在设定的行程范围内！')
            return
        maxThz = 1 / (2 * SysConf.appData.gpMode.step)
        resolution = 1 / (SysConf.appData.gpMode.end - SysConf.appData.gpMode.start)  # 分辨率
        self.txtMaxHz.setText(f'{maxThz}')
        self.txtResolution.setText(f'{resolution:.3f}')
        self.initCharts(SysConf.appData.gpMode.start, SysConf.appData.gpMode.end, maxThz)
        self.btnGpRef.setText('正在采集')
        self.btnGpOpenDev.setEnabled(False)
        self.btnGpInit.setEnabled(False)
        self.btnGpRef.setEnabled(False)
        self.btnGpSam.setEnabled(False)
        self.btnGpStop.setEnabled(True)
        self.btnGpSave.setEnabled(False)
        self.btnGpEdit.setEnabled(False)
        self.btnGpImport.setEnabled(False)
        self.btnGpAnalysis.setEnabled(False)
        self.btnGpMore.setEnabled(False)
        SysConf.appData.cgMode.samIndex = 0
        self.resetCharts()
        self.thread = threading.Thread(target=self.collProc)
        self.thread.start()

    @pyqtSlot()
    def on_btnGpSam_clicked(self):
        if SysConf.appData.cgMode.isAutoAnalysis:
            if gl.isStrNoneOrEmpty(self.txtGpThickness.text()):
                MessageBoxEx.show('选择自动分析，请填写厚度值！')
                return
            else:
                SysConf.appData.cgMode.thickness = float(self.txtGpThickness.text())
        print('样品采集')
        self.btnGpSam.setText('正在采集')
        self.btnGpOpenDev.setEnabled(False)
        self.btnGpInit.setEnabled(False)
        self.btnGpRef.setEnabled(False)
        self.btnGpSam.setEnabled(False)
        self.btnGpStop.setEnabled(True)
        self.btnGpSave.setEnabled(False)
        self.btnGpEdit.setEnabled(False)
        self.btnGpImport.setEnabled(False)
        self.btnGpAnalysis.setEnabled(False)
        self.btnGpMore.setEnabled(False)
        SysConf.appData.cgMode.samIndex += 1
        self.addNewLine(None)
        self.resetCharts()
        self.thread = threading.Thread(target=self.collProc)
        self.thread.start()

    def onGpCollDataOver(self, code):
        isSample = SysConf.appData.gpMode.samIndex != 0
        self.btnGpSam.setEnabled('样品采集') if isSample else self.btnGpRef.setText('开始采集')
        self.btnGpOpenDev.setEnabled(True)
        self.btnGpInit.setEnabled(True)
        self.btnGpRef.setEnabled(True)
        self.btnGpStop.setEnabled(False)
        self.btnGpImport.setEnabled(True)
        self.btnGpMore.setEnabled(True)
        self.btnGpAnalysis.setEnabled(True)
        if code == gl.SUCCESS:
            self.btnGpSam.setEnabled(True)
            self.btnGpSave.setEnabled(isSample)
            self.btnGpEdit.setEnabled(isSample)
            print('数据采集完成！')
        elif code == gl.MANUAL_EXIT:
            self.btnGpSam.setEnabled(isSample)
            isEnable = self.chart1.isDataEnable()
            self.btnGpSave.setEnabled(isEnable)
            self.btnGpEdit.setEnabled(isEnable)
        else:
            MessageBoxEx.show(f'光谱扫描数据采集失败，错误代码{code}！')
            self.btnGpSam.setEnabled(isSample)

    @pyqtSlot()
    def on_btnGpStop_clicked(self):
        print('中断采集')
        gl.set()

    @pyqtSlot()
    def on_btnGpSave_clicked(self):
        if self.chart1.isDataEnable() is False:
            MessageBoxEx.show('当前没有数据需要保存！')
            return
        dlg = SaveDialog()
        if dlg.showDialog() is False:
            return

        dt = GPData()
        dt.Start = float(self.txtStart.text())
        dt.end = float(self.txtEnd.text())
        dt.step = float(self.txtStep.text())
        dt.thickness = SysConf.appData.gpMode.thickness
        dt.Operator = SysConf.appData.loginUser
        dt.AddDate = datetime.datetime.now()
        dt.SampleType = dlg.txtType.currentText()
        dt.SampleTypeId = dlg.txtType.property('id')
        dt.SampleName = dlg.txtName.text()
        dt.Data = json.dumps(self.chart1.getData()).encode('utf8')
        dt.save()

    @pyqtSlot()
    def on_btnGpImport_clicked(self):
        fileName, type = QFileDialog.getOpenFileName(caption='选择光谱数据文件', filter='光谱数据(*.dat);;All Files (*)')
        if gl.isFileExist(fileName) is False:
            return
        with open(fileName, "r", encoding='utf-8') as f:
            jMap = json.load(f)

        if jMap is None:
            return

        if 'start' not in jMap or \
           'end' not in jMap or \
           'step' not in jMap:
            MessageBoxEx.show('文件数据格式不正确！')
            return

        SysConf.appData.pgMode.start = jMap['start']
        SysConf.appData.pgMode.end = jMap['end']
        SysConf.appData.pgMode.step = jMap['step']
        SysConf.appData.pgMode.thickness = jMap['thickness']
        self.on_btnGpInit_clicked()
        maxThz = 1 / (2 * SysConf.appData.gpMode.step)
        resolution = 1 / (SysConf.appData.gpMode.end - SysConf.appData.gpMode.start)  # 分辨率
        self.txtMaxHz.setText(f'{maxThz}')
        self.txtResolution.setText(f'{resolution:.3f}')
        self.initCharts(SysConf.appData.gpMode.start, SysConf.appData.gpMode.end, maxThz)

        self.importCharts(jMap['data'])
        self.btnGpEdit.setEnabled(True)
        self.btnGpSave.setEnabled(True)
        self.btnGpAnalysis.setEnabled(True)

    def displayGpData(self, dt):
        self.btnSpectral.setChecked(True)
        self.onScanModelSel(self.btnSpectral)
        SysConf.appData.pgMode.start = dt.Start
        SysConf.appData.pgMode.end = dt.End
        SysConf.appData.pgMode.step = dt.Step
        SysConf.appData.pgMode.thickness = dt.Thickness
        self.on_btnGpInit_clicked()
        maxThz = 1 / (2 * SysConf.appData.gpMode.step)
        resolution = 1 / (SysConf.appData.gpMode.end - SysConf.appData.gpMode.start)  # 分辨率
        self.txtMaxHz.setText(f'{maxThz}')
        self.txtResolution.setText(f'{resolution:.3f}')
        self.initCharts(SysConf.appData.gpMode.start, SysConf.appData.gpMode.end, maxThz)
        jMap = json.loads(dt.Data.decode('utf8'))
        self.importCharts(jMap)
        self.btnGpEdit.setEnabled(True)
        self.btnGpSave.setEnabled(True)
        self.btnGpAnalysis.setEnabled(True)

    @pyqtSlot()
    def on_btnGpMore_clicked(self):
        dlg = GpSetMoreDialog()
        dlg.showDialog()

    ##############################成像光谱#################################
    @pyqtSlot()
    def on_btnCxOpenDev_clicked(self):
        print('开启硬件')
        self.btnCxOpenDev.setEnabled(False)
        self.btnCxInit.setEnabled(False)
        self.btnCxRef.setEnabled(False)
        self.btnCxSam.setEnabled(False)
        self.btnCxStop.setEnabled(False)
        self.btnCxSave.setEnabled(False)
        self.btnCxEdit.setEnabled(False)
        self.btnCxImport.setEnabled(False)
        self.btnCxAnalysis.setEnabled(False)

        if SysConf.appData.cgMode.isDeviceOn:
            action = self.closeProc
            self.btnCxOpenDev.setText('正在关闭硬件')
        else:
            action = self.openProc
            self.btnCxOpenDev.setText('正在开启硬件')

        self.thread = threading.Thread(target=action)
        self.thread.start()

    def onCxOpenDevOver(self, code):
        if code == gl.SUCCESS:
            self.btnCxOpenDev.setStyleSheet('QPushButton{background-color:#FF4EBE44;border:none;}')
            SysConf.appData.cgMode.isDeviceOn = True
            self.btnCxOpenDev.setEnabled(True)
            self.btnCxInit.setEnabled(True)
            self.btnCxRef.setEnabled(True)
            self.btnCxSam.setEnabled(False)
            self.btnCxStop.setEnabled(False)
            self.btnCxSave.setEnabled(False)
            self.btnCxEdit.setEnabled(False)
            self.btnCxImport.setEnabled(True)
            self.btnCxAnalysis.setEnabled(False)
            self.btnCxOpenDev.setText('关闭硬件')
            MessageBoxEx.show('成像光谱设备开启成功!')
        else:
            SysConf.appData.cgMode.isDeviceOn = False
            self.btnCxOpenDev.setText('开启硬件')
            self.btnCxOpenDev.setEnabled(True)
            self.btnCxInit.setEnabled(False)
            self.btnCxRef.setEnabled(False)
            self.btnCxSam.setEnabled(False)
            self.btnCxStop.setEnabled(False)
            self.btnCxSave.setEnabled(False)
            self.btnCxEdit.setEnabled(False)
            self.btnCxImport.setEnabled(True)
            self.btnCxAnalysis.setEnabled(False)
            MessageBoxEx.show(f'打开设备失败，错误代码{code}!')

    def onCxCloseDevOver(self, code):
        if code == gl.SUCCESS:
            print('成像光谱设备关闭成功！')
        else:
            print('成像光谱设备关闭失败！')
        SysConf.appData.cgMode.isDeviceOn = False
        self.btnCxOpenDev.setEnabled(True)
        self.btnCxImport.setEnabled(True)
        self.btnCxOpenDev.setText('开启硬件')
        self.btnCxOpenDev.setStyleSheet(
            'QPushButton{background-color:#FF00A3DA;border:none;} QPushButton:hover{background-color:#8F00A3DA;}')

    @pyqtSlot()
    def on_btnCxInit_clicked(self):
        self.txtCxHz.setText('0')
        self.txtRunTime.setText('0')
        self.txtAngle.setText(f'{SysConf.appData.cgMode.angle}')
        self.txtCalTimes.setText(f'{SysConf.appData.cgMode.avgNum}')
        self.txtScanTime.setText(f'{SysConf.appData.cgMode.scanTime}')
        self.txtCxThickness.setText(f'{SysConf.appData.cgMode.thickness}')
        self.txtRefraction.setText(f'{SysConf.appData.cgMode.refraction}')
        self.cbxScanArr.setCurrentIndex(SysConf.devCxMode.kuaiYan.index)
        self.cbxNumArr.setCurrentIndex(SysConf.devCxMode.kuaiYan.freqDivision)

    @pyqtSlot()
    def on_btnCxRef_clicked(self):
        if self.chart1.isSamEnable() and \
                QDialog.Accepted != MessageBoxEx.show("采集的样品信息将被清除，确定继续操作？", "温馨提示", '是', '否'):
            return

        SysConf.appData.cgMode.angle = int(float(self.txtAngle.text()))
        SysConf.appData.cgMode.avgNum = int(float(self.txtCalTimes.text()))
        SysConf.appData.cgMode.scanTime = int(float(self.txtScanTime.text()))
        SysConf.devCxMode.kuaiYan.index = self.cbxScanArr.currentIndex()
        SysConf.devCxMode.kuaiYan.freqDivision = self.cbxNumArr.currentIndex()
        if SysConf.appData.cgMode.scanTime <= 0:
            MessageBoxEx.show("请设置成像光谱扫描时间！")
            return
        else:
            self.txtRunTime.setText('0')
            self.btnCxRef.setText('正在采集')
            self.btnCxOpenDev.setEnabled(False)
            self.btnCxInit.setEnabled(False)
            self.btnCxSam.setEnabled(False)
            self.btnCxRef.setEnabled(False)
            self.btnCxStop.setEnabled(True)
            self.btnCxImport.setEnabled(False)
            self.btnCxSave.setEnabled(False)
            self.btnCxEdit.setEnabled(False)
            self.btnCxAnalysis.setEnabled(False)
            SysConf.appData.cgMode.samIndex = 0
            _range = 1.0 / SysConf.devCxMode.kuaiYan.getStep() / 2
            self.initCharts(0, SysConf.devCxMode.kuaiYan.getPs(), _range)
            self.resetCharts()
            self.thread = threading.Thread(target=self.collProc)
            self.thread.start()

    @pyqtSlot()
    def on_btnCxSam_clicked(self):
        SysConf.appData.cgMode.avgNum = int(self.txtCalTimes.text())
        if SysConf.appData.cgMode.isAutoAnalysis:
            if gl.isStrNoneOrEmpty(self.txtCxThickness.text()):
                MessageBoxEx.show('选择自动分析，请填写厚度值！')
                return
            else:
                SysConf.appData.cgMode.thickness = float(self.txtCxThickness.text())

            if gl.isStrNoneOrEmpty(self.txtRefraction.text()):
                MessageBoxEx.show('选择自动分析，请填写厚度值！')
                return
            else:
                SysConf.appData.cgMode.refraction = float(self.txtRefraction.text())

        self.btnCxSam.setText('正在采集')
        self.btnCxOpenDev.setEnabled(False)
        self.btnCxInit.setEnabled(False)
        self.btnCxRef.setEnabled(False)
        self.btnCxSam.setEnabled(False)
        self.btnCxEdit.setEnabled(False)
        self.btnCxSave.setEnabled(False)
        self.btnCxStop.setEnabled(True)
        self.btnCxImport.setEnabled(False)
        SysConf.appData.cgMode.samIndex += 1
        self.addNewLine(None)
        self.resetCharts()
        self.thread = threading.Thread(target=self.collProc)
        self.thread.start()

    def onCxCollDataOver(self, code):
        isSample = SysConf.appData.cgMode.samIndex != 0
        self.btnCxSam.setText('样品采集') if isSample else self.btnCxRef.setText('开始采集')
        self.btnCxOpenDev.setEnabled(True)
        self.btnCxInit.setEnabled(True)
        self.btnCxRef.setEnabled(True)
        self.btnCxStop.setEnabled(False)
        self.btnCxImport.setEnabled(True)
        self.btnCxAnalysis.setEnabled(True)
        isEnable = self.chart1.isDataEnable()
        isSam = self.chart1.isSamEnable()
        self.btnCxSave.setEnabled(isEnable)
        self.btnCxEdit.setEnabled(isSam)
        self.btnCxSam.setEnabled(isEnable)
        if code == gl.SUCCESS:
            print('数据采集完成！')
        elif code == gl.MANUAL_EXIT:
            print('数据采集中断！')
        else:
            MessageBoxEx.show(f'成像光谱数据采集失败，错误代码{code}！')

    @pyqtSlot()
    def on_btnCxStop_clicked(self):
        print('中断采集')
        gl.set()
        self.workFlow.decoder.stop()

    @pyqtSlot()
    def on_btnCxSave_clicked(self):
        #if self.workFlow.isFlowStopped() is False:
        #    MessageBoxEx.show('数据未解码完成请等待！')
        #    return
        if self.chart1.isDataEnable() is False:
            MessageBoxEx.show('当前没有数据需要保存！')
            return

        dlg = SaveDialog()
        if dlg.showDialog() is False:
            return

        dt = CXGPData()
        dt.ScanTime = float(eval(self.txtScanTime.text()))
        dt.RunTime = float(eval(self.txtRunTime.text()))
        dt.Index = SysConf.devCxMode.kuaiYan.index
        dt.DivFreq = SysConf.devCxMode.kuaiYan.freqDivision
        dt.Angle = SysConf.appData.cgMode.angle
        dt.AvgNum = SysConf.appData.cgMode.avgNum
        dt.Thickness = SysConf.appData.cgMode.thickness
        dt.Refraction = SysConf.appData.cgMode.refraction
        dt.Operator = SysConf.appData.loginUser
        dt.AddDate = datetime.datetime.now()
        dt.SampleName = dlg.txtName.text()
        dt.SampleType = dlg.txtType.currentText()
        dt.SampleTypeId = dlg.txtType.property('id')
        dt.Data = json.dumps(self.chart1.getData()).encode('utf8')
        dt.save()

    @pyqtSlot()
    def on_btnCxImport_clicked(self):
        fileName, _type = QFileDialog.getOpenFileName(caption='选择成像光谱数据文件', filter='成像光谱数据(*.qda);;All Files (*)')
        print(fileName)
        if gl.isFileExist(fileName) is False:
            return
        with open(fileName, "r", encoding='utf-8') as f:
            jMap = json.load(f)

        if jMap is None:
            return

        if 'scanTime' not in jMap or \
           'index' not in jMap or \
           'freqDivision' not in jMap or \
           'angle' not in jMap:
            MessageBoxEx.show('文件数据格式不正确！')
            return

        SysConf.appData.cgMode.scanTime = jMap['scanTime']
        SysConf.appData.cgMode.thickness = jMap['thickness']
        SysConf.devCxMode.kuaiYan.index = jMap['index']
        SysConf.devCxMode.kuaiYan.freqDivision = int(jMap['freqDivision'])
        SysConf.appData.cgMode.angle = jMap['angle']
        SysConf.appData.cgMode.avgNum = jMap['avgNum']
        self.on_btnCxInit_clicked()
        _range = 1.0 / SysConf.devCxMode.kuaiYan.getStep() / 2
        self.initCharts(0, SysConf.devCxMode.kuaiYan.getPs(), _range)

        self.importCharts(jMap['data'])
        self.btnCxEdit.setEnabled(True)
        self.btnCxSave.setEnabled(True)
        self.btnCxAnalysis.setEnabled(True)

    def displayCgData(self, dt):
        self.btnImage.setChecked(True)
        self.onScanModelSel(self.btnImage)
        SysConf.appData.cgMode.scanTime = dt.ScanTime
        SysConf.appData.cgMode.thickness = dt.Thickness
        SysConf.devCxMode.kuaiYan.index = dt.Index
        SysConf.devCxMode.kuaiYan.freqDivision = dt.DivFreq
        SysConf.appData.cgMode.angle = 20
        SysConf.appData.cgMode.avgNum = 10
        self.on_btnCxInit_clicked()
        _range = 1.0 / SysConf.devCxMode.kuaiYan.getStep() / 2
        self.initCharts(0, SysConf.devCxMode.kuaiYan.getPs(), _range)
        jMap = json.loads(dt.Data.decode('utf8'))
        self.importCharts(jMap)
        self.btnCxEdit.setEnabled(True)
        self.btnCxSave.setEnabled(True)
        self.btnCxAnalysis.setEnabled(True)

     # =================================================================
    def openProc(self):
        gl.reset()
        code = self.workFlow.turnOn()
        gl.set()
        mode = 2000 if SysConf.appData.isFastScan else 1000
        self.signalNotify.emit(None, mode, code)

    def closeProc(self):
        gl.reset()
        code = self.workFlow.turnOff()
        gl.set()
        mode = 2001 if SysConf.appData.isFastScan else 1001
        self.signalNotify.emit(None, mode, code)

    def collProc(self):
        gl.reset()
        code = self.workFlow.collRun()
        gl.set()
        mode = 2002 if SysConf.appData.isFastScan else 1002
        self.signalNotify.emit(None, mode, code)

    def calFreqProc(self):
        while gl.waitOne(1) is False:
            # 计算频域
            data = self.chart1.getLineData(SysConf.appData.cgMode.samIndex)
            if data[0] is not None:
                xfArr, yfArr = Algorithm.get_freq(data[0], data[1])
                self.signalNotify.emit(None, 8081, (SysConf.appData.cgMode.samIndex, xfArr, yfArr))

            isCGAnalysis = SysConf.appData.isFastScan and SysConf.appData.cgMode.isAutoAnalysis \
                           and SysConf.appData.cgMode.samIndex != 0
            isGPAnalysis = SysConf.appData.isFastScan is False and SysConf.appData.gpMode.isAutoAnalysis \
                           and SysConf.appData.gpMode.samIndex != 0

            if isGPAnalysis or isCGAnalysis:
                data = self.chart1.getAnalysisData(SysConf.appData.cgMode.samIndex)
                if data is None:
                    continue

                thick = SysConf.appData.cgMode.thickness if SysConf.appData.isFastScan else SysConf.appData.gpMode.thickness

                _freq, _abs, _ref = Algorithm.get_absorption_refractive(data[0], data[1], data[2], thick)
                self.signalNotify.emit(None, 8080, [SysConf.appData.cgMode.samIndex, _freq, _abs, _ref])

    def signalNotifyProc(self, widget, mode, value):
        # print(f'====>>{mode}\t{value}')
        if mode == 1:
            widget.setText(value)
        elif mode == 2:
            widget.setEnabled(value)
        elif mode == 1000:
            self.onGpOpenDevOver(value)
        elif mode == 1001:
            self.onGpCloseDevOver(value)
        elif mode == 1002:
            self.onGpCollDataOver(value)
        elif mode == 1003:
            self.ledBtn1.setState(value)
        elif mode == 1004:
            self.ledBtn2.setState(value)
        elif mode == 1005:
            self.ledBtn3.setState(value)
        elif mode == 1007:
            mV = np.ptp(value[2])
            self.chart1.setChartTitle(f'时域波形（极值差为 {mV:.2f} mV）')
            self.chart1.updateLine(value[0], value[1], value[2])
        elif mode == 2000:
            self.onCxOpenDevOver(value)
        elif mode == 2001:
            self.onCxCloseDevOver(value)
        elif mode == 2002:
            self.onCxCollDataOver(value)
        elif mode == 2003:
            self.ledBtn4.setState(value)
        elif mode == 2004:
            self.ledBtn5.setState(value)
        elif mode == 2005:
            self.ledBtn6.setState(value)
        elif mode == 2006:
            self.txtRunTime.setText(f'{value:.1f}')
        elif mode == 2009:
            self.txtCxHz.setText(f'{value:.1f}')
        elif mode == 2007:
            mV = np.ptp(value[2])
            self.chart1.setChartTitle(f'时域波形（极值差为 {mV:.2f} mV）')
            self.chart1.updateLine(value[0], value[1], value[2])
        elif mode == 8081:
            self.chart2.updateLine(value[0], value[1], value[2])
            pass
        elif mode == 8080:
            self.chart3.updateLine(value[0], value[1], value[2])
            self.chart4.updateLine(value[0], value[1], value[3])
            pass
        else:
            return None
