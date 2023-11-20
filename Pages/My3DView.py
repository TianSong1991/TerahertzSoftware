from PyQt5.QtWidgets import QMainWindow,QMessageBox
from Ui.My3D import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5 import Qt
from ThirdLib.AlgFunctions import ImageFunctions
from mpl_toolkits.mplot3d import Axes3D
import time
import os
from mpldatacursor import datacursor
from ThirdLib.AlgConfig import ImageConfig
from ThirdLib.AlgImageVisualization import Visualization
import matplotlib as mpl
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
mpl.rcParams.update(
{
'text.usetex': False,
'font.family': 'stixgeneral',
'mathtext.fontset': 'stix',
}
)
os.environ['QT_API'] = 'pyqt5'


class My3DView(QMainWindow, Ui_MainWindow,ImageConfig):
    def __init__(self,parent=None):
        super(My3DView, self).__init__(parent)
        self.x_start =1
        self.x_step =0.1
        self.x_end =100
        self.y_start = 1
        self.y_step = 0.1
        self.y_end = 100
        self.z_step = 0.1
        self.points = 9000
        self.python_values = []
        self.fp = 1
        self.setupUi(self)
        self.init_ui()

    def initParams(self,params,robot):
        self.x_start = params[0]
        self.x_step = params[1]
        self.x_end = params[2]
        self.y_start = params[3]
        self.y_step = params[4]
        self.y_end = params[5]
        self.z_step = params[6]
        self.points = params[7]
        self.M_thz_sig = params[8]
        self.fast_thz_time = params[9]
        self.robot = robot
        self.running()

    def running(self):
        try:
            if len(self.M_thz_sig) > 0 :
                self.init_data()
        except Exception as e:
            with open(self.log_path, 'a+') as ff:
                ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} 3D Image Run Error！ \n')
                ff.write(f'{time.strftime("%Y-%m-%d %X", time.localtime())} The error is :{e} \n')

    def init_data(self):
        ImageConfig.updateParams(self)

        unpack_params = [self.x_start,self.x_step,self.x_end,self.y_start,self.y_step,self.y_end,self.delete_d]
        self.xlists = self.M_thz_sig[0,:]
        self.ylists = self.M_thz_sig[1,:]
        self.M_thz_sig = self.M_thz_sig[4:,:]

        if self.robot == 0:
            self.M_thz_sig = ImageFunctions.convertData(self.xlists, self.ylists, self.M_thz_sig,unpack_params)
            self.M_thz_sig = ImageFunctions.ImageChoose(self.ref_path, self.image_choose, self.fast_thz_time, self.M_thz_sig)
            self.M_thz_sig = ImageFunctions.image_filter(self.M_thz_sig, self.image_filter)
            self.THzsig_intp = ImageFunctions.New_3DImage(self.points,self.M_thz_sig,self.platform,self.compress)
        else:
            self.THzsig_intp = ImageFunctions.Robot3DImage(self.M_thz_sig,self.compress,int(self.ylists[0]))

        self.shapey,self.shapex,self.shapez = self.THzsig_intp.shape
        self.x_min = self.x_start
        self.y_min = self.y_start
        self.x_max = self.x_end
        self.y_max = self.y_end
        self.x_min0 = self.x_start
        self.y_min0 = self.y_start
        self.x_max0 = self.x_end
        self.y_max0 = self.y_end
        self.z_max = np.max(self.fast_thz_time)
        self.z_min = 0
        self.dx = round(self.x_step,2)
        self.dy = round(self.y_step,2)
        self.dz = round(self.z_step,2)
        self.xyscroll.setMinimum(0)
        self.xyscroll.setMaximum(self.shapex - 1)
        self.xzscroll.setMinimum(0)
        self.xzscroll.setMaximum(self.shapey - 1)
        self.yzscroll.setMinimum(0)
        self.yzscroll.setMaximum(self.shapez - 1)
        self.xyscroll.setValue(0)
        self.xysliderval()
        self.xzscroll.setValue(0)
        self.xzsliderval()
        self.yzscroll.setValue(0)
        self.yzsliderval()
        self.updateButton(self.volumtype)

    def init_ui(self):
        ImageConfig.init(self)
        ImageConfig.updateParams(self)
        self.compresslineEdit.setText(str(self.compress))

        self.setWindowTitle('My3D')
        self.setWindowFlags(Qt.Qt.FramelessWindowHint|Qt.Qt.Tool)
        self.xyfig = plt.figure()
        self.xycanvas = FC(self.xyfig)
        self.xyscroll = QtWidgets.QScrollBar()
        self.xyscroll.valueChanged.connect(self.xysliderval)
        xylayout = QHBoxLayout()
        xylayout.addWidget(self.xycanvas)
        xylayout.addWidget(self.xyscroll)
        self.xy_box.setLayout(xylayout)
        self.xzfig = plt.figure()
        self.xzcanvas = FC(self.xzfig)
        self.xzscroll = QtWidgets.QScrollBar()
        self.xzscroll.valueChanged.connect(self.xzsliderval)
        xzlayout = QHBoxLayout()
        xzlayout.addWidget(self.xzcanvas)
        xzlayout.addWidget(self.xzscroll)
        self.xz_box.setLayout(xzlayout)
        self.yzfig = plt.figure()
        self.yzcanvas = FC(self.yzfig)
        self.yzscroll = QtWidgets.QScrollBar()
        self.yzscroll.valueChanged.connect(self.yzsliderval)
        yzlayout = QHBoxLayout()
        yzlayout.addWidget(self.yzcanvas)
        yzlayout.addWidget(self.yzscroll)
        self.yz_box.setLayout(yzlayout)
        self.sigfig = plt.figure()
        self.sigcanvas = FC(self.sigfig)
        siglayout = QHBoxLayout()
        siglayout.addWidget(self.sigcanvas)
        self.time_box.setLayout(siglayout)
        self.xysliderval()
        self.xzsliderval()
        self.yzsliderval()
        self.timeliderval()
        mainlayout = QVBoxLayout()
        self.visualization = Visualization(self.THzsig_intp,self.use_mayavi)
        self.mainui = self.visualization.edit_traits(parent=self.main_groupBox, kind='subpanel').control
        mainlayout.addWidget(self.mainui)
        self.main_groupBox.setLayout(mainlayout)
        self.mainui.setParent(self.main_groupBox)
        self.updateButton(0)
        self.refresh_pushButton.clicked.connect(self.refreshbtn_click)
        self.volum_pushButton.clicked.connect(lambda :self.updateButton(0))
        self.slice_pushButton.clicked.connect(lambda :self.updateButton(1))
        self.color_comboBox.currentIndexChanged.connect(self.selectionchange)
        self.alpha_horizontalScrollBar.setMaximum(100)
        self.alpha_horizontalScrollBar.valueChanged.connect(self.alphasliderval)


    def selectionchange(self):
        self.mode = self.color_comboBox.currentText()
        self.visualization.update(self.THzsig_intp, self.mode,("volum" if self.volumtype == 0 else "slice"))
        self.xysliderval()
        self.yzsliderval()
        self.xzsliderval()


    def updateButton(self,type):
        self.volumtype = type
        if self.volumtype == 0:
            self.volum_pushButton.setEnabled(False)
            self.slice_pushButton.setEnabled(True)
        else:
            self.volum_pushButton.setEnabled(True)
            self.slice_pushButton.setEnabled(False)
        self.visualization.update(self.THzsig_intp, self.mode, ("volum" if self.volumtype == 0 else "slice"))

    def alphasliderval(self):
        if len(self.THzsig_intp) > 0:
            self.visualization.updatealpha(self.alpha_horizontalScrollBar.value())



    def xysliderval(self):
        if self.M_thz_sig.shape[0] > 0:
            self.z_lineEdit.setText(
                str(round(self.z_min + (self.z_max - self.z_min) / (self.shapex - 1) * self.xyscroll.value(), 2)))
        else:
            self.z_lineEdit.setText(str(1))
        arr_xy = self.xyfig.gca()
        arr_xy.cla()
        if len(self.THzsig_intp) > 0:
            arr_xy.axis('on')
            data_xy = ImageFunctions.xyz_orientation(self.THzsig_intp[:, self.xyscroll.value() - 1, :],self.xy)
            arr_xy.imshow(data_xy, cmap=self.mode,extent=(self.x_min,self.x_max,self.y_min,self.y_max))
            arr_xy.set_xticks(np.arange(self.x_min,self.x_max + 1,5))
            arr_xy.set_yticks(np.arange(self.y_min,self.y_max + 1,5))
            arr_xy.invert_yaxis()
            if mpl.__version__ == '3.2.0':
                datacursor(arr_xy, display='multiple', draggable=True)
            self.xycanvas.draw()
        else:
            arr_xy.set_xticks([])
            arr_xy.set_yticks([])
            arr_xy.axis('off')

    def xzsliderval(self):
        self.timeliderval()
        if self.M_thz_sig.shape[0] > 0:
            self.y_lineEdit.setText(str(round(self.y_min + (self.y_max - self.y_min)/(self.shapey - 1)*self.xzscroll.value(),2)))
        else:
            self.y_lineEdit.setText(str(1))
        arr_xz = self.xzfig.gca()
        arr_xz.cla()

        if len(self.THzsig_intp) > 0:
            if self.use_qda == 1:
                arr_xz.axis('on')
                data_xz = ImageFunctions.xyz_orientation(self.THzsig_intp[self.xzscroll.value() - 1, :, :],self.xz)
                arr_xz.imshow(data_xz, cmap=self.mode,interpolation='bicubic')
                if mpl.__version__ == '3.2.0':
                    datacursor(arr_xz,display='multiple',draggable=True)
                self.xzcanvas.draw()
            else:
                arr_xz.axis('on')
                data_xz = ImageFunctions.xyz_orientation(self.THzsig_intp[self.xzscroll.value() - 1, :, :],self.xz)
                arr_xz.imshow(data_xz, cmap=self.mode,interpolation='bicubic',extent=(self.x_min,self.x_max,self.z_min,self.z_max))
                arr_xz.set_xticks(np.arange(self.x_min,self.x_max + 1,10))
                arr_xz.set_yticks(np.arange(self.z_min,self.z_max + 1,10))
                arr_xz.invert_yaxis()
                if mpl.__version__ == '3.2.0':
                    datacursor(arr_xz, display='multiple', draggable=True)
                self.xzcanvas.draw()
        else:
            arr_xz.set_xticks([])
            arr_xz.set_yticks([])
            arr_xz.axis('off')

    def yzsliderval(self):
        self.timeliderval()
        if self.M_thz_sig.shape[0] > 0:
            self.x_lineEdit.setText(str(round(self.x_min + (self.x_max - self.x_min)/(self.shapez - 1)*self.yzscroll.value(),2)))
        else:
            self.x_lineEdit.setText(str(1))
        arr_yz=self.yzfig.gca()
        arr_yz.cla()

        if len(self.THzsig_intp) > 0:
            if self.use_qda == 1:
                arr_yz.axis('on')
                data_yz = ImageFunctions.xyz_orientation(self.THzsig_intp[:, :, self.yzscroll.value() - 1].T,self.yz)
                arr_yz.imshow(data_yz, cmap=self.mode, interpolation='bicubic')
                if mpl.__version__ == '3.2.0':
                    datacursor(arr_yz,display='multiple',draggable=True)
                self.yzcanvas.draw()
            else:
                arr_yz.axis('on')
                data_yz = ImageFunctions.xyz_orientation(self.THzsig_intp[:, :, self.yzscroll.value() - 1].T,self.yz)
                arr_yz.imshow(data_yz, cmap=self.mode, interpolation='bicubic',extent=(self.y_min,self.y_max,self.z_min,self.z_max))
                arr_yz.set_xticks(np.arange(self.y_min,self.y_max + 1,10))
                arr_yz.set_yticks(np.arange(self.z_min,self.z_max + 1,10))
                arr_yz.invert_yaxis()
                if mpl.__version__ == '3.2.0':
                    datacursor(arr_yz, display='multiple', draggable=True)
                self.yzcanvas.draw()
        else:
            arr_yz.set_xticks([])
            arr_yz.set_yticks([])
            arr_yz.axis('off')

    def refreshbtn_click(self):
        if self.THzsig_intp.shape[0] > 0:
            try:
                xvalue = (float(self.x_lineEdit.text())-self.x_min)/(self.x_max - self.x_min)*(self.shapez - 1)
                yvalue = (float(self.y_lineEdit.text())-self.y_min)/(self.y_max - self.y_min)*(self.shapey - 1)
                zvalue = (float(self.z_lineEdit.text())-self.z_min)/(self.z_max - self.z_min)*(self.shapex - 1)
                if xvalue < 0 or xvalue >= self.shapez:
                    QMessageBox.warning(self, "警告", "输入的x不在范围内,x范围{}到{}之间".format(self.x_min,self.x_max), QMessageBox.Ok)
                    return
                if yvalue < 0 or yvalue >= self.shapey:
                    QMessageBox.warning(self, "警告", "输入的y不在范围内,y范围{}到{}之间".format(self.y_min,self.y_max), QMessageBox.Ok)
                    return
                if zvalue < 0 or zvalue >= self.shapex:
                    QMessageBox.warning(self, "警告", "输入的z不在范围内,z范围{}到{}之间".format(self.z_min,self.z_max), QMessageBox.Ok)
                    return
                self.xyscroll.setValue(zvalue)
                self.yzscroll.setValue(xvalue)
                self.xzscroll.setValue(yvalue)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e), QMessageBox.Ok)

    def timeliderval(self):
        plt.clf()
        arr = self.sigfig.gca()
        arr.cla()
        arr.axis('off')
        if len(self.THzsig_intp) > 0:
            arr.axis('on')
            sigThzxy = ImageFunctions.xyThzsgl(self.dx * self.yzscroll.value(), self.dy * self.xzscroll.value(), self.M_thz_sig)
            arr.plot(self.fast_thz_time,sigThzxy)
            if mpl.__version__ == '3.2.0':
                datacursor(arr,display='multiple')
        self.sigcanvas.draw()


