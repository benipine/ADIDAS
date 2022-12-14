import os
import sys
import time
import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import *

conn = sqlite3.connect("adidas.db")
cur = conn.cursor()

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
        cmd= os.popen("cd ~/ADIDAS/ADIDAS/GUI/fullimage && ls")
        result_old = cmd.read().strip()
        while(1):
            cmd= os.popen("cd ~/ADIDAS/ADIDAS/GUI/fullimage && ls")
            result_new = cmd.read().strip()
            time.sleep(1)
            if result_new != result_old:
                fname = result_new.replace(result_old, "").strip()
                result_old = result_new
                os.system("python imgdtndb.py "+fname)
                self.new_image.emit(fname)
        
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("LogWindow.ui", self)
        self.setscroll()

        self.button_logs.clicked.connect(self.tostatus)
        self.check_image = ImageThread()
        self.check_image.start()
        self.check_image.new_image.connect(self.new_image)
        
    def setscroll(self):
        self.scroll_log.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_log)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_log.setWidget(self.inner)
        cur.execute("SELECT * FROM detection_data")
        rows= cur.fetchall()
        
        for i in reversed(rows):
            buttonname = str(i[1])
            button=QPushButton(objectName=buttonname)
            button.setMinimumSize(1, 30)
            button.setMaximumSize(100000, 30)
            button.setStyleSheet("font: 75 12pt 'PibotoLt';"
"background-color: rgb(255, 255, 255);"
"text-align: left;")
            button.clicked.connect(self.printnum)
            
            date=i[1]
            date_a=date[0:4]+"-"+date[4:6]+"-"+date[6:8]+" "+date[8:10]+":"+date[10:12]+":"+date[12:14]
            button.setText(" "*60+"Log # "+str(i[0])+" "*80+date_a+" "*80+i[2])
            
            self.inner.layout().addWidget(button)
            
            date_b=date[0:4]+"-"+date[4:6]+"-"+date[6:8]+" "+date[8:10]+":"+date[10:12]+":"+date[12:14]
            self.log_title.setText("Log #"+" "+str(i[0])+"       Time : "+date_b+" (KST)")
                  
    def tostatus(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def new_image(self, fname):
        self.image_before.setPixmap(QtGui.QPixmap("fullimage/"+fname))
        self.image_before.repaint()
        self.image_after.setPixmap(QtGui.QPixmap("cropimage/"+fname))
        self.image_after.repaint()
        self.setscroll()
        
    def printnum(self):
        sending_button = self.sender()
        self.new_image(str(sending_button.objectName())+".jpg")
        
        
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
