import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import *

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
                
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("LoginWindow.ui", self)
        
        self.button_login.clicked.connect(self.loginclick)
        
    def loginclick(self):
        login_id = self.input_id.text()
        print(login_id)
        login_pw = self.input_pw.text()
        print(login_pw)
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
        
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("LogWindow.ui", self)
        
        vbox = QVBoxLayout()
        self.scroll_area.addLayout(vbox)
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
        
        self.add_log("1", fname, "phantom")
        
    def add_log(self, num, time, dronetype):
        label = QLabel(time)
        
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
