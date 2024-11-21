#!/bin/python
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from subprocess import run, Popen


class Ui_PowerOptions(object):
    def setupUi(self, PowerOptions):
        PowerOptions.setObjectName("PowerOptions")
        PowerOptions.resize(448, 324)
        PowerOptions.setMinimumSize(QtCore.QSize(300, 300))
        icon = QtGui.QIcon.fromTheme("system-shutdown-panel")
        PowerOptions.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(PowerOptions)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(PowerOptions)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 4)
        self.sleepButton = QtWidgets.QPushButton(PowerOptions)
        icon = QtGui.QIcon.fromTheme("weather-clear-night")
        self.sleepButton.setIcon(icon)
        self.sleepButton.setObjectName("sleepButton")
        self.gridLayout.addWidget(self.sleepButton, 1, 1, 1, 4)
        self.rebootButton = QtWidgets.QPushButton(PowerOptions)
        icon = QtGui.QIcon.fromTheme("system-restart-panel")
        self.rebootButton.setIcon(icon)
        self.rebootButton.setObjectName("rebootButton")
        self.gridLayout.addWidget(self.rebootButton, 2, 1, 1, 4)
        self.shutdownButton = QtWidgets.QPushButton(PowerOptions)
        icon = QtGui.QIcon.fromTheme("system-shutdown-panel")
        self.shutdownButton.setIcon(icon)
        self.shutdownButton.setObjectName("shutdownButton")
        self.gridLayout.addWidget(self.shutdownButton, 3, 1, 1, 4)
        self.logoutButton = QtWidgets.QPushButton(PowerOptions)
        icon = QtGui.QIcon.fromTheme("avatar-default")
        self.logoutButton.setIcon(icon)
        self.logoutButton.setObjectName("logoutButton")
        self.gridLayout.addWidget(self.logoutButton, 4, 1, 1, 4)
        self.verticalLayout.addLayout(self.gridLayout)
        self.connectUi()
        self.retranslateUi(PowerOptions)
        QtCore.QMetaObject.connectSlotsByName(PowerOptions)
    def connectUi(self):
        self.rebootButton.clicked.connect(self.rebootClicked)
        self.shutdownButton.clicked.connect(self.shutdownClicked)
        self.logoutButton.clicked.connect(self.logoutClicked)
        self.sleepButton.clicked.connect(self.sleepClicked)
    def rebootClicked(self):
        self.setBigLabel("Rebooting...")
        run(["systemctl", "reboot"])
    def shutdownClicked(self):
        self.setBigLabel("Shutting down...")
        run(["systemctl", "poweroff"])
    def logoutClicked(self):
        self.setBigLabel("Logging out...")
        run(["qtile", "cmd-obj", "-o", "cmd", "-f", "shutdown"])
    def sleepClicked(self):
        self.setBigLabel("Sleeping...")
        Popen(["betterlockscreen", "--lock"])
        Popen(["systemctl", "suspend"])
        PowerOptions.close() 
    def setBigLabel(self, text):
        self.label.setText(f"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">{text}</span></p></body></html>")
    def retranslateUi(self, PowerOptions):
        _translate = QtCore.QCoreApplication.translate
        PowerOptions.setWindowTitle(_translate("PowerOptions", "Power Options"))
        self.label.setText(_translate("PowerOptions", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">What do you want to do?</span></p></body></html>"))
        self.sleepButton.setText(_translate("PowerOptions", "Sleep"))
        self.rebootButton.setText(_translate("PowerOptions", "Restart"))
        self.shutdownButton.setText(_translate("PowerOptions", "Shutdown"))
        self.logoutButton.setText(_translate("PowerOptions", "Logout"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PowerOptions = QtWidgets.QDialog()
    ui = Ui_PowerOptions()
    ui.setupUi(PowerOptions)
    PowerOptions.show()
    sys.exit(app.exec_())
