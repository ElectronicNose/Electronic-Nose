# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'measurement.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Measurement(object):
    def setupUi(self, Measurement):
        Measurement.setObjectName("Measurement")
        Measurement.resize(337, 229)
        self.label_reptitions = QtWidgets.QLabel(Measurement)
        self.label_reptitions.setGeometry(QtCore.QRect(20, 30, 161, 21))
        self.label_reptitions.setObjectName("label_reptitions")
        self.lineEdit_repetitions = QtWidgets.QLineEdit(Measurement)
        self.lineEdit_repetitions.setGeometry(QtCore.QRect(200, 30, 113, 20))
        self.lineEdit_repetitions.setObjectName("lineEdit_repetitions")
        self.label_sampleTime = QtWidgets.QLabel(Measurement)
        self.label_sampleTime.setGeometry(QtCore.QRect(20, 60, 161, 21))
        self.label_sampleTime.setObjectName("label_sampleTime")
        self.lineEdit_sampleTime = QtWidgets.QLineEdit(Measurement)
        self.lineEdit_sampleTime.setGeometry(QtCore.QRect(200, 60, 113, 20))
        self.lineEdit_sampleTime.setObjectName("lineEdit_sampleTime")
        self.label_purgeTime = QtWidgets.QLabel(Measurement)
        self.label_purgeTime.setGeometry(QtCore.QRect(20, 90, 161, 21))
        self.label_purgeTime.setObjectName("label_purgeTime")
        self.lineEdit_purgeTime = QtWidgets.QLineEdit(Measurement)
        self.lineEdit_purgeTime.setGeometry(QtCore.QRect(200, 90, 113, 20))
        self.lineEdit_purgeTime.setObjectName("lineEdit_purgeTime")
        self.pushButton_advanced = QtWidgets.QPushButton(Measurement)
        self.pushButton_advanced.setGeometry(QtCore.QRect(170, 190, 75, 23))
        self.pushButton_advanced.setObjectName("pushButton_advanced")
        self.pushButton_save = QtWidgets.QPushButton(Measurement)
        self.pushButton_save.setGeometry(QtCore.QRect(250, 190, 75, 23))
        self.pushButton_save.setObjectName("pushButton_save")

        self.retranslateUi(Measurement)
        QtCore.QMetaObject.connectSlotsByName(Measurement)

    def retranslateUi(self, Measurement):
        _translate = QtCore.QCoreApplication.translate
        Measurement.setWindowTitle(_translate("Measurement", "Measurement"))
        self.label_reptitions.setText(_translate("Measurement", "Number of repetitions"))
        self.label_sampleTime.setText(_translate("Measurement", "Sample time (seconds)"))
        self.label_purgeTime.setText(_translate("Measurement", "Purge time (seconds)"))
        self.pushButton_advanced.setText(_translate("Measurement", "Advanced"))
        self.pushButton_save.setText(_translate("Measurement", "Save"))

'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Measurement = QtWidgets.QWidget()
    ui = Ui_Measurement()
    ui.setupUi(Measurement)
    Measurement.show()
    sys.exit(app.exec_())
'''
