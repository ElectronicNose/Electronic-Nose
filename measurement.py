from PyQt5 import QtCore, QtGui, QtWidgets
import sys,csv
from measurement_gui import Ui_Measurement
from PyQt5.QtWidgets import QFileDialog
import serial,itertools

class Measurement(QtWidgets.QMainWindow, Ui_Measurement):
    def __init__(self,parent = None):
        super(Measurement,self).__init__(parent)
        self.setupUi(self)
        self.pushButton_save.clicked.connect(self.save)
        self.ser = serial.Serial('/dev/ttyUSB0')


    def save(self):
        line = b''
        header = []
        self.data = []
        self.s0 = []
        self.s1 = []
        self.s2 = []
        self.s3 = []
        self.s4 = []
        self.s5 = []
        self.s6 = []
        self.s7 = []
        self.s8 = []
        self.s9 = []
        self.s10 = []
        self.s11 = []
        self.s12, self.s13, self.s14, self.s15, self.s16 = [], [], [], [], []
        self.s17, self.s18, self.s19, self.s20, self.s21 = [], [], [], [], []
        self.s22, self.s23, self.s24, self.s25, self.s26 = [], [], [], [], []
        self.s27, self.s28, self.s29, self.s30, self.s31 = [], [], [], [], []
        self.s32, self.s33, self.s34, self.s35, self.s36 = [], [], [], [], []
        self.s37, self.s38, self.s39, self.s40, self.s41 = [], [], [], [], []
        self.s42, self.s43, self.s44, self.s45, self.s46 = [], [], [], [], []
        self.s47, self.s48, self.s49, self.s50, self.s51 = [], [], [], [], []
        self.s52, self.s53, self.s54, self.s55, self.s56 = [], [], [], [], []
        self.s57, self.s58, self.s59, self.s60, self.s61 = [], [], [], [], []
        self.s62, self.s63 = [], []

        if self.lineEdit_repetitions.text() == '' or self.lineEdit_sampleTime.text() == '' or self.lineEdit_purgeTime.text() == '':
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Please enter some value")
            msg.setWindowTitle("Measurement")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.show()
        else:
            filename = QFileDialog.getSaveFileName(self, 'Save as', '', "CSV Files (*.csv)")
            if filename == ('', ''):
                print("Cancel")
            else:
                with open(filename[0] + str(".csv"), 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    repetitions = [self.label_reptitions.text(), self.lineEdit_repetitions.text()]
                    sampleTime = [self.label_sampleTime.text(), self.lineEdit_sampleTime.text()]
                    purgeTime = [self.label_purgeTime.text(), self.lineEdit_purgeTime.text()]

                    writer.writerow(repetitions)
                    writer.writerow(sampleTime)
                    writer.writerow(purgeTime)

                self.ser.write(b'START\n')
                self.ser.write(self.lineEdit_repetitions.text().encode() + b'\n')
                self.ser.write(self.lineEdit_sampleTime.text().encode() + b'\n')
                self.ser.write(self.lineEdit_purgeTime.text().encode() + b'\n')
                self.ser.write(b'STOP\n')

                for i in range(64):
                    header.append("s" + str(i))

                while True:
                    line = self.ser.readline()
                    if line==b'END\n':
                        print(self.s1)
                        print(self.s2)
                        print(self.s3)
                        self.data = [self.s0, self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7, self.s8, self.s9,
                                     self.s10, self.s11, self.s12, self.s13, self.s14, self.s15, self.s16, self.s17,
                                     self.s18, self.s19, self.s20, self.s21, self.s22, self.s23, self.s24, self.s25, self.s26,
                                     self.s27, self.s28, self.s29, self.s30, self.s31, self.s32, self.s33, self.s34,
                                     self.s35, self.s36, self.s37, self.s38, self.s39, self.s40, self.s41, self.s42, self.s43,
                                     self.s44, self.s45, self.s46, self.s47, self.s48, self.s49, self.s50, self.s51, self.s52,
                                     self.s53, self.s54, self.s55, self.s56, self.s57, self.s58, self.s59, self.s60, self.s61,
                                     self.s62, self.s63]
                        self.data = [list(i) for i in itertools.zip_longest(*self.data)]
                        print(self.data)
                        with open(filename[0] + str(".csv"), 'a', newline='') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow(header)
                            writer.writerows(self.data)
                            Measurement.close(self)
                            print("Data written")
                            msg1 = QtWidgets.QMessageBox(self)
                            msg1.setIcon(QtWidgets.QMessageBox.Information)
                            msg1.setText("Data received and saved")
                            msg1.setWindowTitle("Measurement")
                            msg1.setStandardButtons(QtWidgets.QMessageBox.Ok)
                            msg1.show()
                            self.ser.close()
                            break
                    else:
                        line = str(line).split()
                        if line[0]=="b's0":
                            self.s0.append(float(line[1]))
                        elif line[0]=="b's1":
                            self.s1.append(float(line[1]))
                        elif line[0]=="b's2":
                            self.s2.append(float(line[1]))
                        elif line[0]=="b's3":
                            self.s3.append(float(line[1]))
                        elif line[0]=="b's4":
                            self.s4.append(float(line[1]))
                        elif line[0]=="b's5":
                            self.s5.append(float(line[1]))
                        elif line[0]=="b's6":
                            self.s6.append(float(line[1]))
                        elif line[0]=="b's7":
                            self.s7.append(float(line[1]))
                        elif line[0]=="b's8":
                            self.s8.append(float(line[1]))
                        elif line[0]=="b's9":
                            self.s9.append(float(line[1]))
                        elif line[0]=="b's10":
                            self.s10.append(float(line[1]))
                        elif line[0]=="b's11":
                            self.s11.append(float(line[1]))
                        elif line[0]=="b's12":
                            self.s12.append(float(line[1]))
                        elif line[0]=="b's13":
                            self.s13.append(float(line[1]))
                        elif line[0]=="b's14":
                            self.s14.append(float(line[1]))
                        elif line[0]=="b's15":
                            self.s15.append(float(line[1]))
                        elif line[0]=="b's16":
                            self.s16.append(float(line[1]))
                        elif line[0]=="b's17":
                            self.s17.append(float(line[1]))
                        elif line[0]=="b's18":
                            self.s18.append(float(line[1]))
                        elif line[0]=="b's19":
                            self.s19.append(float(line[1]))
                        elif line[0]=="b's20":
                            self.s20.append(float(line[1]))
                        elif line[0]=="b's21":
                            self.s21.append(float(line[1]))
                        elif line[0]=="b's22":
                            self.s22.append(float(line[1]))
                        elif line[0]=="b's23":
                            self.s23.append(float(line[1]))
                        elif line[0]=="b's24":
                            self.s24.append(float(line[1]))
                        elif line[0]=="b's25":
                            self.s25.append(float(line[1]))
                        elif line[0]=="b's26":
                            self.s26.append(float(line[1]))
                        elif line[0]=="b's27":
                            self.s27.append(float(line[1]))
                        elif line[0]=="b's28":
                            self.s28.append(float(line[1]))
                        elif line[0]=="b's29":
                            self.s29.append(float(line[1]))
                        elif line[0]=="b's30":
                            self.s30.append(float(line[1]))
                        elif line[0]=="b's31":
                            self.s31.append(float(line[1]))
                        elif line[0]=="b's32":
                            self.s32.append(float(line[1]))
                        elif line[0]=="b's33":
                            self.s33.append(float(line[1]))
                        elif line[0]=="b's34":
                            self.s34.append(float(line[1]))
                        elif line[0]=="b's35":
                            self.s35.append(float(line[1]))
                        elif line[0]=="b's36":
                            self.s36.append(float(line[1]))
                        elif line[0]=="b's37":
                            self.s37.append(float(line[1]))
                        elif line[0]=="b's38":
                            self.s38.append(float(line[1]))
                        elif line[0]=="b's39":
                            self.s39.append(float(line[1]))
                        elif line[0]=="b's40":
                            self.s40.append(float(line[1]))
                        elif line[0]=="b's41":
                            self.s41.append(float(line[1]))
                        elif line[0]=="b's42":
                            self.s42.append(float(line[1]))
                        elif line[0]=="b's43":
                            self.s43.append(float(line[1]))
                        elif line[0]=="b's44":
                            self.s44.append(float(line[1]))
                        elif line[0]=="b's45":
                            self.s45.append(float(line[1]))
                        elif line[0]=="b's46":
                            self.s46.append(float(line[1]))
                        elif line[0]=="b's47":
                            self.s47.append(float(line[1]))
                        elif line[0]=="b's48":
                            self.s48.append(float(line[1]))
                        elif line[0]=="b's49":
                            self.s49.append(float(line[1]))
                        elif line[0]=="b's50":
                            self.s50.append(float(line[1]))
                        elif line[0]=="b's51":
                            self.s51.append(float(line[1]))
                        elif line[0]=="b's52":
                            self.s52.append(float(line[1]))
                        elif line[0]=="b's53":
                            self.s53.append(float(line[1]))
                        elif line[0]=="b's54":
                            self.s54.append(float(line[1]))
                        elif line[0]=="b's55":
                            self.s55.append(float(line[1]))
                        elif line[0]=="b's56":
                            self.s56.append(float(line[1]))
                        elif line[0]=="b's57":
                            self.s57.append(float(line[1]))
                        elif line[0]=="b's58":
                            self.s58.append(float(line[1]))
                        elif line[0]=="b's59":
                            self.s59.append(float(line[1]))
                        elif line[0]=="b's60":
                            self.s60.append(float(line[1]))
                        elif line[0]=="b's61":
                            self.s61.append(float(line[1]))
                        elif line[0]=="b's62":
                            self.s62.append(float(line[1]))
                        elif line[0]=="b's63":
                            self.s63.append(float(line[1]))



