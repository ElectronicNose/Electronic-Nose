from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from analysis_gui import Ui_Analysis
import numpy as np
import matplotlib,math,csv
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None):
        fig = Figure()
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class Radar(FigureCanvas):
    def __init__(self, titles, rect=None, parent=None):
        fig = Figure()
        if rect is None:
            rect = [0.05, 0.05, 0.8, 0.8]
        self.n = len(titles)
        self.angles = np.arange(90, 90 + 360, 360.0 / self.n)
        self.angles = [a % 360 for a in self.angles]
        self.axes = [fig.add_axes(rect, projection="polar", label="axes%d" % i)
                     for i in range(self.n)]


        #FigureCanvas.setSizePolicy(self,
                                   #QtWidgets.QSizePolicy.Expanding,
                                   #QtWidgets.QSizePolicy.Expanding)
        #FigureCanvas.updateGeometry(self)

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles,labels=titles, fontsize=14)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)

        for ax, angle in zip(self.axes, self.angles):
            ax.set_rgrids([0.2,0.4,0.6,0.8,1.0], angle=angle)
            ax.spines["polar"].set_visible(False)
            ax.set_ylim(auto=True)
            ax.set_xlim(auto=True)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)


    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)



class Analysis(QtWidgets.QMainWindow, Ui_Analysis):
    def __init__(self,parent = None):
        super(Analysis,self).__init__(parent)
        self.setupUi(self)

        self.XY_widget = QtWidgets.QWidget(self.tab_XY)
        self.Radar_widget = QtWidgets.QWidget(self.tab_Radar)
        self.Box_widget = QtWidgets.QWidget(self.tab_Box)
        self.Table_widget = QtWidgets.QWidget(self.tab_Table)

        self.XY_Layout = QtWidgets.QVBoxLayout(self.XY_widget)
        self.XY = MyMplCanvas(self.XY_widget)
        self.XY_Layout.addWidget(self.XY)
        self.mpl_toolbar = NavigationToolbar(self.XY, self.XY_widget)
        self.XY_Layout.addWidget(self.mpl_toolbar)


        self.Box_Layout = QtWidgets.QVBoxLayout(self.Box_widget)
        self.box = MyMplCanvas(self.Box_widget)
        self.Box_Layout.addWidget(self.box)
        self.box_toolbar = NavigationToolbar(self.box, self.Box_widget)
        self.Box_Layout.addWidget(self.box_toolbar)


        #self.tabWidget.setFocus()
        #self.setCentralWidget(self.tabWidget)
        #self.XY_widget.setFocus()
        #self.Radar_widget.setFocus()
        #self.Box_widget.setFocus()
        #self.tabWidget.setFocus()
        #self.setCentralWidget(self.tabWidget)

        self.actionOpen.triggered.connect(self.open)
        self.actionMax_min.triggered.connect(self.max_min)
        self.actionStandardization_M_0_S_1.triggered.connect(self.standardization)
        self.actionBaseline_Correction.triggered.connect(self.baseline)
        self.actionPeak_Detection.triggered.connect(self.peak_detection)
        self.actionFWHM.triggered.connect(self.FWHM)
        self.actionRise_Time.triggered.connect(self.rise_time)
        self.actionFall_Time.triggered.connect(self.fall_time)
        self.sensor_name = []
        self.sensor_sn = []
        self.time = []
        self.s1, self.s2, self.s3, self.s4, self.s5 = [], [], [], [], []
        self.s6, self.s7, self.s8, self.s9, self.s10 = [], [], [], [], []
        self.s11, self.s12, self.s13, self.s14, self.s15 = [], [], [], [], []
        self.s16, self.s17, self.s18 = [], [], []

    def open(self):
        self.data = []
        self.sensor_name = []
        self.sensor_sn = []
        self.time = []
        self.s1, self.s2, self.s3, self.s4, self.s5 = [], [], [], [], []
        self.s6, self.s7, self.s8, self.s9, self.s10 = [], [], [], [], []
        self.s11, self.s12, self.s13, self.s14, self.s15 = [], [], [], [], []
        self.s16, self.s17, self.s18 = [], [], []
        self.s1_normalized = []
        self.s2_normalized = []
        self.s3_normalized = []
        self.s4_normalized = []
        self.s5_normalized = []
        self.s6_normalized = []
        self.s7_normalized = []
        self.s8_normalized = []
        self.s9_normalized = []
        self.s10_normalized = []
        self.s11_normalized = []
        self.s12_normalized = []
        self.s13_normalized = []
        self.s14_normalized = []
        self.s15_normalized = []
        self.s16_normalized = []
        self.s17_normalized = []
        self.s18_normalized = []

        filename = QFileDialog.getOpenFileName(self, 'Open',filter="CSV Files (*.csv);;FOX Files (*.txt)",
                                               initialFilter= "CSV Files (*.csv)")
        if filename[0]=='':
            print("Cancel")
        elif filename[1]=='FOX Files (*.txt)':
            file = open(filename[0])
            lines = file.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("[SENSOR NAME]"):
                    i += 1
                    self.sensor_name = lines[i].split()
                if lines[i].startswith("[SENSOR SN]"):
                    i += 1
                    self.sensor_sn = lines[i].split()
                if lines[i].startswith("[SENSOR DATA]"):
                    j = i + 1
                    self.data = []
                    for i in range(121):
                        self.data.append(lines[j].split())
                        j += 1
            print(self.sensor_name)
            print(self.sensor_sn)
            print(self.data)

            for i in range(len(self.data)):
                for j in range(19):
                    if j==0:
                        self.time.append(self.data[i][j])
                    if j==1:
                        self.s1.append(float(self.data[i][j]))
                    if j==2:
                        self.s2.append(float(self.data[i][j]))
                    if j==3:
                        self.s3.append(float(self.data[i][j]))
                    if j==4:
                        self.s4.append(float(self.data[i][j]))
                    if j==5:
                        self.s5.append(float(self.data[i][j]))
                    if j==6:
                        self.s6.append(float(self.data[i][j]))
                    if j==7:
                        self.s7.append(float(self.data[i][j]))
                    if j==8:
                        self.s8.append(float(self.data[i][j]))
                    if j==9:
                        self.s9.append(float(self.data[i][j]))
                    if j==10:
                        self.s10.append(float(self.data[i][j]))
                    if j==11:
                        self.s11.append(float(self.data[i][j]))
                    if j==12:
                        self.s12.append(float(self.data[i][j]))
                    if j==13:
                        self.s13.append(float(self.data[i][j]))
                    if j==14:
                        self.s14.append(float(self.data[i][j]))
                    if j==15:
                        self.s15.append(float(self.data[i][j]))
                    if j==16:
                        self.s16.append(float(self.data[i][j]))
                    if j==17:
                        self.s17.append(float(self.data[i][j]))
                    if j==18:
                        self.s18.append(float(self.data[i][j]))



            self.XY.axes.cla()
            self.XY.axes.plot(self.time, self.s1,label=self.sensor_name[0])
            self.XY.axes.plot(self.time, self.s2,label=self.sensor_name[1])
            self.XY.axes.plot(self.time, self.s3,label=self.sensor_name[2])
            self.XY.axes.plot(self.time, self.s4,label=self.sensor_name[3])
            self.XY.axes.plot(self.time, self.s5,label=self.sensor_name[4])
            self.XY.axes.plot(self.time, self.s6,label=self.sensor_name[5])
            self.XY.axes.plot(self.time, self.s7,label=self.sensor_name[6])
            self.XY.axes.plot(self.time, self.s8,label=self.sensor_name[7])
            self.XY.axes.plot(self.time, self.s9,label=self.sensor_name[8])
            self.XY.axes.plot(self.time, self.s10,label=self.sensor_name[9])
            self.XY.axes.plot(self.time, self.s11,label=self.sensor_name[10])
            self.XY.axes.plot(self.time, self.s12,label=self.sensor_name[11])
            self.XY.axes.plot(self.time, self.s13,label=self.sensor_name[12])
            self.XY.axes.plot(self.time, self.s14,label=self.sensor_name[13])
            self.XY.axes.plot(self.time, self.s15,label=self.sensor_name[14])
            self.XY.axes.plot(self.time, self.s16,label=self.sensor_name[15])
            self.XY.axes.plot(self.time, self.s17,label=self.sensor_name[16])
            self.XY.axes.plot(self.time, self.s18,label=self.sensor_name[17])
            self.XY.axes.set_xlabel("Time")
            self.XY.axes.set_ylabel("Impedance")
            self.XY.axes.legend(loc='best')
            self.XY.draw()
            self.menuNormalization.setEnabled(True)

            for item in self.s1:
                self.s1_normalized.append((item - min(self.s1)) / (max(self.s1) - min(self.s1)))
            for item in self.s2:
                self.s2_normalized.append((item - min(self.s2)) / (max(self.s2) - min(self.s2)))
            for item in self.s3:
                self.s3_normalized.append((item - min(self.s3)) / (max(self.s3) - min(self.s3)))
            for item in self.s4:
                self.s4_normalized.append((item - min(self.s4)) / (max(self.s4) - min(self.s4)))
            for item in self.s5:
                self.s5_normalized.append((item - min(self.s5)) / (max(self.s5) - min(self.s5)))
            for item in self.s6:
                self.s6_normalized.append((item - min(self.s6)) / (max(self.s6) - min(self.s6)))
            for item in self.s7:
                self.s7_normalized.append((item - min(self.s7)) / (max(self.s7) - min(self.s7)))
            for item in self.s8:
                self.s8_normalized.append((item - min(self.s8)) / (max(self.s8) - min(self.s8)))
            for item in self.s9:
                self.s9_normalized.append((item - min(self.s9)) / (max(self.s9) - min(self.s9)))
            for item in self.s10:
                self.s10_normalized.append((item - min(self.s10)) / (max(self.s10) - min(self.s10)))
            for item in self.s11:
                self.s11_normalized.append((item - min(self.s11)) / (max(self.s11) - min(self.s11)))
            for item in self.s12:
                self.s12_normalized.append((item - min(self.s12)) / (max(self.s12) - min(self.s12)))
            for item in self.s13:
                self.s13_normalized.append((item - min(self.s13)) / (max(self.s13) - min(self.s13)))
            for item in self.s14:
                self.s14_normalized.append((item - min(self.s14)) / (max(self.s14) - min(self.s14)))
            for item in self.s15:
                self.s15_normalized.append((item - min(self.s15)) / (max(self.s15) - min(self.s15)))
            for item in self.s16:
                self.s16_normalized.append((item - min(self.s16)) / (max(self.s16) - min(self.s16)))
            for item in self.s17:
                self.s17_normalized.append((item - min(self.s17)) / (max(self.s17) - min(self.s17)))
            for item in self.s18:
                self.s18_normalized.append((item - min(self.s18)) / (max(self.s18) - min(self.s18)))
            self.radar_plot()
            self.box_plot()

        elif filename[1] == "CSV Files (*.csv)":
            with open(filename[0], 'r') as csvfile:
                lines = csv.reader(csvfile)
                data = list(lines)
                self.tableWidget.setRowCount(len(data))
                self.tableWidget.setColumnCount(64)
                for i in range(3):
                    for j in range(2):
                        self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(data[i][j]))
                for i in range(3,len(data)):
                    for j in range(64):
                        self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(data[i][j]))


    def max_min(self):

        self.XY.axes.cla()
        self.XY.axes.plot(self.time, self.s1_normalized, label=self.sensor_name[0])
        '''
        self.sc.axes.plot(self.time, self.s2_normalized, label=self.sensor_name[1])
        self.sc.axes.plot(self.time, self.s3_normalized, label=self.sensor_name[2])
        self.sc.axes.plot(self.time, self.s4_normalized, label=self.sensor_name[3])
        self.sc.axes.plot(self.time, self.s5_normalized, label=self.sensor_name[4])
        self.sc.axes.plot(self.time, self.s6_normalized, label=self.sensor_name[5])
        self.sc.axes.plot(self.time, self.s7_normalized, label=self.sensor_name[6])
        self.sc.axes.plot(self.time, self.s8_normalized, label=self.sensor_name[7])
        self.sc.axes.plot(self.time, self.s9_normalized, label=self.sensor_name[8])
        self.sc.axes.plot(self.time, self.s10_normalized, label=self.sensor_name[9])
        self.sc.axes.plot(self.time, self.s11_normalized, label=self.sensor_name[10])
        self.sc.axes.plot(self.time, self.s12_normalized, label=self.sensor_name[11])
        self.sc.axes.plot(self.time, self.s13_normalized, label=self.sensor_name[12])
        self.sc.axes.plot(self.time, self.s14_normalized, label=self.sensor_name[13])
        self.sc.axes.plot(self.time, self.s15_normalized, label=self.sensor_name[14])
        self.sc.axes.plot(self.time, self.s16_normalized, label=self.sensor_name[15])
        self.sc.axes.plot(self.time, self.s17_normalized, label=self.sensor_name[16])
        self.sc.axes.plot(self.time, self.s18_normalized, label=self.sensor_name[17])
        '''
        self.XY.axes.set_xlabel("Time")
        self.XY.axes.set_ylabel("Impedance")
        self.XY.axes.legend(loc='best')
        self.XY.draw()
        self.actionPeak_Detection.setEnabled(True)
        self.actionRise_Time.setEnabled(True)
        self.actionFall_Time.setEnabled(True)
        self.actionFWHM.setEnabled(True)

    def standardization(self):
        z1,z2,z3,z4,z5,z6,z7,z8,z9,z10,z11,z12,z13,z14,z15,z16,z17,z18 = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
        m1 = sum(self.s1) / len(self.s1)
        m2 = sum(self.s2) / len(self.s2)
        m3 = sum(self.s3) / len(self.s3)
        m4 = sum(self.s4) / len(self.s4)
        m5 = sum(self.s5) / len(self.s5)
        m6 = sum(self.s6) / len(self.s6)
        m7 = sum(self.s7) / len(self.s7)
        m8 = sum(self.s8) / len(self.s8)
        m9 = sum(self.s9) / len(self.s9)
        m10 = sum(self.s10) / len(self.s10)
        m11 = sum(self.s11) / len(self.s11)
        m12 = sum(self.s12) / len(self.s12)
        m13 = sum(self.s13) / len(self.s13)
        m14 = sum(self.s14) / len(self.s14)
        m15 = sum(self.s15) / len(self.s15)
        m16 = sum(self.s16) / len(self.s16)
        m17 = sum(self.s17) / len(self.s17)
        m18 = sum(self.s18) / len(self.s18)

        sd1 = self.calculate_sd(self.s1, m1)
        sd2 = self.calculate_sd(self.s2, m2)
        sd3 = self.calculate_sd(self.s3, m3)
        sd4 = self.calculate_sd(self.s4, m4)
        sd5 = self.calculate_sd(self.s5, m5)
        sd6 = self.calculate_sd(self.s6, m6)
        sd7 = self.calculate_sd(self.s7, m7)
        sd8 = self.calculate_sd(self.s8, m8)
        sd9 = self.calculate_sd(self.s9, m9)
        sd10 = self.calculate_sd(self.s10, m10)
        sd11 = self.calculate_sd(self.s11, m11)
        sd12 = self.calculate_sd(self.s12, m12)
        sd13 = self.calculate_sd(self.s13, m13)
        sd14 = self.calculate_sd(self.s14, m14)
        sd15 = self.calculate_sd(self.s15, m15)
        sd16 = self.calculate_sd(self.s16, m16)
        sd17 = self.calculate_sd(self.s17, m17)
        sd18 = self.calculate_sd(self.s18, m18)

        for item in self.s1:
            z1.append((item-m1)/sd1)
        for item in self.s2:
            z2.append((item-m2)/sd2)
        for item in self.s3:
            z3.append((item-m3)/sd3)
        for item in self.s4:
            z4.append((item-m4)/sd4)
        for item in self.s5:
            z5.append((item-m5)/sd5)
        for item in self.s6:
            z6.append((item-m6)/sd6)
        for item in self.s7:
            z7.append((item-m7)/sd7)
        for item in self.s8:
            z8.append((item-m8)/sd8)
        for item in self.s9:
            z9.append((item-m9)/sd9)
        for item in self.s10:
            z10.append((item-m10)/sd10)
        for item in self.s11:
            z11.append((item-m11)/sd11)
        for item in self.s12:
            z12.append((item-m12)/sd12)
        for item in self.s13:
            z13.append((item-m13)/sd13)
        for item in self.s14:
            z14.append((item-m14)/sd14)
        for item in self.s15:
            z15.append((item-m15)/sd15)
        for item in self.s16:
            z16.append((item-m16)/sd16)
        for item in self.s17:
            z17.append((item-m17)/sd17)
        for item in self.s18:
            z18.append((item-m18)/sd18)

        '''
        mz1 = sum(z1) / len(z1)
        mz2 = sum(z2) / len(z2)
        mz3 = sum(z3) / len(z3)
        mz4 = sum(z4) / len(z4)
        mz5 = sum(z5) / len(z5)
        mz6 = sum(z6) / len(z6)
        mz7 = sum(z7) / len(z7)
        mz8 = sum(z8) / len(z8)
        mz9 = sum(z9) / len(z9)
        mz10 = sum(z10) / len(z10)
        mz11 = sum(z11) / len(z11)
        mz12 = sum(z12) / len(z12)
        mz13 = sum(z13) / len(z13)
        mz14 = sum(z14) / len(z14)
        mz15 = sum(z15) / len(z15)
        mz16 = sum(z16) / len(z16)
        mz17 = sum(z17) / len(z17)
        mz18 = sum(z18) / len(z18)

        sdz1 = self.calculate_sd(z1, mz1)
        sdz2 = self.calculate_sd(z2, mz2)
        sdz3 = self.calculate_sd(z3, mz3)
        sdz4 = self.calculate_sd(z4, mz4)
        sdz5 = self.calculate_sd(z5, mz5)
        sdz6 = self.calculate_sd(z6, mz6)
        sdz7 = self.calculate_sd(z7, mz7)
        sdz8 = self.calculate_sd(z8, mz8)
        sdz9 = self.calculate_sd(z9, mz9)
        sdz10 = self.calculate_sd(z10, mz10)
        sdz11 = self.calculate_sd(z11, mz11)
        sdz12 = self.calculate_sd(z12, mz12)
        sdz13 = self.calculate_sd(z13, mz13)
        sdz14 = self.calculate_sd(z14, mz14)
        sdz15 = self.calculate_sd(z15, mz15)
        sdz16 = self.calculate_sd(z16, mz16)
        sdz17 = self.calculate_sd(z17, mz17)
        sdz18 = self.calculate_sd(z18, mz18)

        print(mz1,sdz1)
        print(mz2, sdz2)
        print(mz3, sdz3)
        print(mz4, sdz4)
        print(mz5, sdz5)
        print(mz6, sdz6)
        print(mz7, sdz7)
        print(mz8, sdz8)
        print(mz9, sdz9)
        print(mz10, sdz10)
        print(mz11, sdz11)
        print(mz12, sdz12)
        print(mz13, sdz13)
        print(mz14, sdz14)
        print(mz15, sdz15)
        print(mz16, sdz16)
        print(mz17, sdz17)
        print(mz18, sdz18)
        '''

        self.XY.axes.cla()
        self.XY.axes.plot(self.time, z1, label=self.sensor_name[0])
        '''
        self.sc.axes.plot(self.time, z2, label=self.sensor_name[1])
        self.sc.axes.plot(self.time, z3, label=self.sensor_name[2])
        self.sc.axes.plot(self.time, z4, label=self.sensor_name[3])
        self.sc.axes.plot(self.time, z5, label=self.sensor_name[4])
        self.sc.axes.plot(self.time, z6, label=self.sensor_name[5])
        self.sc.axes.plot(self.time, z7, label=self.sensor_name[6])
        self.sc.axes.plot(self.time, z8, label=self.sensor_name[7])
        self.sc.axes.plot(self.time, z9, label=self.sensor_name[8])
        self.sc.axes.plot(self.time, z10, label=self.sensor_name[9])
        self.sc.axes.plot(self.time, z11, label=self.sensor_name[10])
        self.sc.axes.plot(self.time, z12, label=self.sensor_name[11])
        self.sc.axes.plot(self.time, z13, label=self.sensor_name[12])
        self.sc.axes.plot(self.time, z14, label=self.sensor_name[13])
        self.sc.axes.plot(self.time, z15, label=self.sensor_name[14])
        self.sc.axes.plot(self.time, z16, label=self.sensor_name[15])
        self.sc.axes.plot(self.time, z17, label=self.sensor_name[16])
        self.sc.axes.plot(self.time, z18, label=self.sensor_name[17])
        '''
        self.XY.axes.set_xlabel("Time")
        self.XY.axes.set_ylabel("Impedance")
        self.XY.axes.legend(loc='best')
        self.XY.draw()


    def calculate_sd(self,list,mean):
        sd = 0.0
        for item in list:
            sd += (item-mean) ** 2
        sd = sd/(len(list)-1)
        sd = sd ** (1/2)
        return sd

    def baseline(self):
        '''
        s1 = np.array(self.s1)
        base = peakutils.baseline(s1, deg=3, max_it=100, tol=0.001)

        #self.sc.axes.cla()
        self.sc.axes.plot(self.time, base, label="baseline",c='red')
        self.sc.axes.legend(loc='best')
        self.sc.draw()
        '''

    def peak_detection(self):
        s1_diff = []
        self.s1_indexes = []
        for i in range(len(self.s1_normalized)-1):
            s1_diff.append(self.s1_normalized[i+1]-self.s1_normalized[i])
        print("diff=" + str(s1_diff))
        print(len(s1_diff))
        for i in range(len(s1_diff)-1):
            if s1_diff[i]>0 and s1_diff[i+1]<0:
                self.s1_indexes.append(i+1)
        print(self.s1_indexes)
        for i in range(len(self.s1_indexes)-1):
            if self.s1_normalized[self.s1_indexes[i]]>0.5 and (self.s1_indexes[i+1]-self.s1_indexes[i])>=5:
                self.XY.axes.scatter(self.time[self.s1_indexes[i]], self.s1_normalized[self.s1_indexes[i]],c='red')
                self.XY.draw()
        self.actionRise_Time.setEnabled(True)


    def rise_time(self):
        upper_limit = 0
        lower_limit = 0
        max_index = 0
        rel_tol = 0.05
        abs_tol = 0.1
        peak_values = []
        #for i in range(len(self.s1_indexes)):
            #peak_values.append(self.s1_normalized[self.s1_indexes[i]])
        for i in range(len(self.s1_normalized)):
            if self.s1_normalized[i]==max(self.s1_normalized):
                max_index = i
        print("max index=" + str(max_index))
        for i in range(max_index):
            #if math.isclose(self.s1_normalized[i],0.9*self.s1_normalized[peak_index],rel_tol=0.05):
            if abs(self.s1_normalized[i]-0.9*max(self.s1_normalized)) <= abs_tol:
                upper_limit = i
            #if math.isclose(self.s1_normalized[i], 0.1*self.s1_normalized[peak_index], rel_tol=0.05):
            if abs(self.s1_normalized[i]-0.1*max(self.s1_normalized)) <= abs_tol:
                lower_limit = i
        print(upper_limit)
        print(lower_limit)
        self.XY.axes.text(100,0.9,"Rise Time = " + str(upper_limit-lower_limit)+'s')
        self.XY.draw()


    def fall_time(self):
        upper_limit = 0
        lower_limit = 0
        max_index = 0
        rel_tol = 0.05
        abs_tol = 0.1
        for i in range(len(self.s1_normalized)):
            if self.s1_normalized[i]==max(self.s1_normalized):
                max_index = i
        print("max index="+ str(max_index))
        for i in range(max_index,len(self.s1_normalized)):
            if abs(self.s1_normalized[i] - 0.9 * max(self.s1_normalized)) <= abs_tol:
                lower_limit = i
            if abs(self.s1_normalized[i] - 0.1 * max(self.s1_normalized)) <= abs_tol:
                upper_limit = i
                break
        print(upper_limit)
        print(lower_limit)
        self.XY.axes.text(100,0.8,"Fall Time = " + str(upper_limit - lower_limit) + 's')
        self.XY.draw()

    def FWHM(self):
        upper_limit = 0
        lower_limit = 0
        max_index = 0
        rel_tol = 0.15
        abs_tol = 0.1
        for i in range(len(self.s1_normalized)):
            if self.s1_normalized[i] == max(self.s1_normalized):
                max_index = i
        print("max index=" + str(max_index))
        for i in range(max_index):
            if abs(self.s1_normalized[i] - 0.5 * max(self.s1_normalized)) <= abs_tol:
                lower_limit = i
        for i in range(max_index, len(self.s1_normalized)):
            if abs(self.s1_normalized[i] - 0.5 * max(self.s1_normalized)) <= abs_tol:
                upper_limit = i
                break
        print(upper_limit)
        print(lower_limit)
        x = [lower_limit,upper_limit]
        y = [self.s1_normalized[lower_limit],self.s1_normalized[upper_limit]]
        self.XY.axes.plot(x,y,c='red')
        self.XY.axes.text(100,0.7, "FWHM = " + str(upper_limit - lower_limit) + 's')
        self.XY.draw()

    def radar_plot(self):

        titles = self.sensor_name

        self.Radar_Layout = QtWidgets.QVBoxLayout(self.Radar_widget)
        self.radar = Radar(titles, rect=None, parent=self.Radar_widget)
        self.Radar_Layout.addWidget(self.radar)
        self.radar_toolbar = NavigationToolbar(self.radar, self.Radar_widget)
        self.Radar_Layout.addWidget(self.radar_toolbar)

        for i in range(121):
            self.radar.plot([self.s1_normalized[i],self.s2_normalized[i],self.s3_normalized[i],self.s4_normalized[i],self.s5_normalized[i],self.s6_normalized[i],self.s7_normalized[i],self.s8_normalized[i],self.s9_normalized[i],self.s10_normalized[i],self.s11_normalized[i],self.s12_normalized[i],self.s13_normalized[i],self.s14_normalized[i],self.s15_normalized[i],self.s16_normalized[i],self.s17_normalized[i],self.s18_normalized[i]])
        self.radar.draw()
        self.actionRadar_Plot.setEnabled(False)


    def box_plot(self):
        labels = self.sensor_name
        data = [self.s1_normalized,self.s2_normalized,self.s3_normalized,self.s4_normalized,self.s5_normalized,self.s6_normalized,self.s7_normalized,self.s8_normalized,self.s9_normalized,self.s10_normalized,self.s11_normalized,self.s12_normalized,self.s13_normalized,self.s14_normalized,self.s15_normalized,self.s16_normalized,self.s17_normalized,self.s18_normalized]

        self.box.axes.cla()
        self.box.axes.boxplot(data,labels=labels)
        self.box.axes.set_ylabel("Impedance")
        self.box.draw()


