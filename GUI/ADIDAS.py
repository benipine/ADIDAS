import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import *

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("LoginWindow.ui", self)
        
        self.button_login.clicked.connect(self.loginclick)
        
    def loginclick(self):
        login_id = self.input_id.text()
        login_pw = self.input_pw.text()
        id_list = ["KAFA04"]
        pw_list = ["1234"]
        if login_id not in id_list:
            self.loginwrong()
        else:
            if login_pw != pw_list[id_list.index(login_id)]:
                self.loginwrong()
            else:
                widget.setCurrentIndex(widget.currentIndex()+1)
    
    def loginwrong(self):
        QMessageBox.critical(self, 'Login Failed', 'ID or PASSWORD is wrong')
        
class ImageThread(QThread):
    new_image = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        cmd= os.popen("cd ~/adidas/ADIDAS/GUI/log && ls")
        result_old = cmd.read().strip()
        while(1):
            cmd= os.popen("cd ~/adidas/ADIDAS/GUI/log && ls")
            result_new = cmd.read().strip()
            time.sleep(1)
            if result_new != result_old:
                fname = result_new.replace(result_old, "").strip()
                result_old = result_new
                self.new_image.emit(fname)
        
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("LogWindow.ui", self)
        
        self.scroll_log.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_log)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_log.setWidget(self.inner)
        
        for i in range(0, 10):
            labelname = "label"+str(i)
            label=QLabel(objectName=labelname)
            label.setAlignment(Qt.AlignCenter)
            label.setMinimumSize(1, 30)
            label.setMaximumSize(100000, 30)
            label.setStyleSheet("font: 75 12pt 'PibotoLt';"
"background-color: rgb(255, 255, 255)")
            label.mousePressEvent = self.tostatus
            label.setText("Log # 225"+" "*80+"2022-10-01 09:22:08"+" "*80+"Drone")
            self.inner.layout().addWidget(label)
            
        select = self.findChild(QLabel, "label0")
        select.setStyleSheet("font: 75 20pt 'PibotoLt';"
"background-color: rgb(255, 255, 255)")

        self.button_logs.clicked.connect(self.tostatus)
        self.check_image = ImageThread()
        self.check_image.start()
        self.check_image.new_image.connect(self.new_image)
        
    def tostatus(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def new_image(self, fname):
        self.image_before.setPixmap(QtGui.QPixmap("log/"+fname))
        self.image_before.repaint()
        self.log_title.setText(fname)
        
    def add_log(self, num, time, dronetype):
        
class StatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("StatusWindow.ui", self)
        
        self.button_stat.clicked.connect(self.tolog)
        
    def tolog(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        
    
if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    
    loginwindow = LoginWindow()
    logwindow = LogWindow()
    statwindow = StatWindow()
    
    widget.addWidget(loginwindow)
    widget.addWidget(logwindow)
    widget.addWidget(statwindow)
    
    widget.show()
    
    app.exec_()
