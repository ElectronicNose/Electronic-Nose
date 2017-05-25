from PyQt5 import QtCore, QtGui, QtWidgets
import sys,csv
from mainwindow_gui import Ui_MainWindow
import analysis, measurement
from PyQt5.QtWidgets import QFileDialog


class ElectronicNose(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self,parent = None):
        super(ElectronicNose,self).__init__(parent)
        MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self)

        self.menu = QtWidgets.QMenu(self.pushButton_measurement)

        open = QtWidgets.QAction("Open", self.menu)
        self.menu.addAction(open)
        new = QtWidgets.QAction("New", self.menu)
        self.menu.addAction(new)
        open.triggered.connect(self.open)
        new.triggered.connect(self.new)

        self.pushButton_measurement.clicked.connect(self.measurement)
        self.pushButton_analysis.clicked.connect(self.analysis)

    def measurement(self):
        print("Measurement Clicked")

        #print('leftClicked', QPos)
        parentPosition = self.pushButton_measurement.mapToGlobal(QtCore.QPoint(0,0))
        #menuPosition = parentPosition + QPos

        self.menu.move(parentPosition)
        self.menu.show()

    def open(self):
        filename = QFileDialog.getOpenFileName(self,'Open','', "CSV Files (*.csv)")
        if filename== ('',''):
            print("Cancel")
        else:
            with open(filename[0], newline='') as csvfile:
                reader = csv.reader(csvfile)
                data = list(reader)
                repetitions = data[0][1]
                sampleTime = data[1][1]
                purgeTime = data[2][1]

                #print(repetitions,sampleTime,purgeTime)

    def new(self):
        measure = measurement.Measurement(self)
        measure.show()

    def analysis(self):
        analyse = analysis.Analysis(self)
        analyse.showMaximized()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ElectronicNose()
    ui.showMaximized()
    sys.exit(app.exec_())