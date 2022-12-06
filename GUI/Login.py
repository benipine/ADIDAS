# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1440, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1440, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1440, 720))
        MainWindow.setSizeIncrement(QtCore.QSize(0, 0))
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1421, 701))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.master_grid = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.master_grid.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.master_grid.setContentsMargins(60, 20, 60, 20)
        self.master_grid.setObjectName("master_grid")
        self.sub_hori = QtWidgets.QHBoxLayout()
        self.sub_hori.setSpacing(0)
        self.sub_hori.setObjectName("sub_hori")
        self.logo = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(700, 600))
        self.logo.setMaximumSize(QtCore.QSize(700, 600))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("logo_adidas.png"))
        self.logo.setScaledContents(False)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setObjectName("logo")
        self.sub_hori.addWidget(self.logo)
        self.login_frame = QtWidgets.QFrame(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.login_frame.sizePolicy().hasHeightForWidth())
        self.login_frame.setSizePolicy(sizePolicy)
        self.login_frame.setMaximumSize(QtCore.QSize(500, 600))
        self.login_frame.setStyleSheet("background-color: rgb(226, 226, 226);")
        self.login_frame.setObjectName("login_frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.login_frame)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.login_layout = QtWidgets.QVBoxLayout()
        self.login_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.login_layout.setContentsMargins(50, 50, 50, 80)
        self.login_layout.setSpacing(0)
        self.login_layout.setObjectName("login_layout")
        self.top = QtWidgets.QLabel(self.login_frame)
        self.top.setMaximumSize(QtCore.QSize(16777215, 100))
        self.top.setStyleSheet("font: 75 32pt \"PibotoLt\";")
        self.top.setTextFormat(QtCore.Qt.AutoText)
        self.top.setAlignment(QtCore.Qt.AlignCenter)
        self.top.setObjectName("top")
        self.login_layout.addWidget(self.top)
        self.text_id = QtWidgets.QLabel(self.login_frame)
        self.text_id.setMaximumSize(QtCore.QSize(16777215, 50))
        self.text_id.setStyleSheet("font: 18pt \"PibotoLt\";")
        self.text_id.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.text_id.setObjectName("text_id")
        self.login_layout.addWidget(self.text_id)
        self.lineEdit = QtWidgets.QLineEdit(self.login_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMaximumSize(QtCore.QSize(500, 50))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 18pt \"PibotoLt\";")
        self.lineEdit.setObjectName("lineEdit")
        self.login_layout.addWidget(self.lineEdit)
        self.text_pw = QtWidgets.QLabel(self.login_frame)
        self.text_pw.setMaximumSize(QtCore.QSize(16777215, 50))
        self.text_pw.setStyleSheet("font: 18pt \"PibotoLt\";")
        self.text_pw.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.text_pw.setObjectName("text_pw")
        self.login_layout.addWidget(self.text_pw)
        self.input_pw = QtWidgets.QLineEdit(self.login_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_pw.sizePolicy().hasHeightForWidth())
        self.input_pw.setSizePolicy(sizePolicy)
        self.input_pw.setMaximumSize(QtCore.QSize(500, 50))
        self.input_pw.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 18pt \"PibotoLt\";")
        self.input_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_pw.setObjectName("input_pw")
        self.login_layout.addWidget(self.input_pw)
        self.change_pw = QtWidgets.QLabel(self.login_frame)
        self.change_pw.setMaximumSize(QtCore.QSize(16777215, 100))
        self.change_pw.setStyleSheet("color: rgb(255, 97, 24);")
        self.change_pw.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.change_pw.setObjectName("change_pw")
        self.login_layout.addWidget(self.change_pw)
        self.button_login = QtWidgets.QPushButton(self.login_frame)
        self.button_login.setMaximumSize(QtCore.QSize(16777215, 50))
        self.button_login.setStyleSheet("background-color: rgb(255, 97, 24);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 24pt \"PibotoLt\";")
        self.button_login.setObjectName("button_login")
        self.login_layout.addWidget(self.button_login)
        self.gridLayout_3.addLayout(self.login_layout, 0, 0, 1, 1)
        self.sub_hori.addWidget(self.login_frame)
        self.master_grid.addLayout(self.sub_hori, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.top.setText(_translate("MainWindow", "Administrator Login"))
        self.text_id.setText(_translate("MainWindow", "ID"))
        self.lineEdit.setText(_translate("MainWindow", "KAFA04"))
        self.text_pw.setText(_translate("MainWindow", "PASSWORD"))
        self.input_pw.setText(_translate("MainWindow", "asdf"))
        self.change_pw.setText(_translate("MainWindow", "Change Password"))
        self.button_login.setText(_translate("MainWindow", "LOGIN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())