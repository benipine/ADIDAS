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
        loadUi("UI/LoginWindow.ui", self)
        
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
    refresh_window = pyqtSignal(str, int)
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
                self.refresh_window.emit(fname, 1)
        
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/LogWindow.ui", self)
        
        self.button_logs.clicked.connect(self.tostatus)
        
        db = self.get_db()
        self.refresh_window(str(db[-1][1])+".jpg", 1)
        
        self.check_image = ImageThread()
        self.check_image.start()
        self.check_image.refresh_window.connect(self.refresh_window)
        
    def setscroll(self):
        self.scroll_log.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_log)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_log.setWidget(self.inner)

        rows= self.get_db()
        for i in reversed(rows):
            buttonname = str(i[1])
            button=QPushButton(objectName=buttonname)
            button.setMinimumSize(1, 30)
            button.setMaximumSize(100000, 30)
            button.setStyleSheet("font: 75 12pt 'PibotoLt';"
            "background-color: rgb(255, 255, 255);"
            "text-align: left;")
            date_a=self.adjust_date(i[1])
            button.setText(" "*60+"Log # "+str(i[0])+" "*80+date_a+" "*80+i[2])
            button.clicked.connect(self.button_work)
            self.inner.layout().addWidget(button)
            
    def tostatus(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def refresh_window(self, fname, isnew):
        self.image_before.setPixmap(QtGui.QPixmap("fullimage/"+fname))
        self.image_before.repaint()
        self.image_after.setPixmap(QtGui.QPixmap("cropimage/"+fname))
        self.image_after.repaint()
        
        db = self.get_db()
        index=0
        for i in db:
            if i[1] == fname.strip(".jpg"):
                index = i[0]
                break
        date_a = self.adjust_date(fname)
        self.log_title.setText("Log # "+str(index)+" "*10+"Time : "+date_a+" (KST)")
        
        if isnew == 1:
            self.setscroll()
        
    def adjust_date(self, date):
        return date[0:4]+"-"+date[4:6]+"-"+date[6:8]+" "+date[8:10]+":"+date[10:12]+":"+date[12:14]
        
    def button_work(self):
        sending_button = self.sender()
        self.refresh_window(str(sending_button.objectName())+".jpg", 0)
        
    def get_db(self):
        cur.execute("SELECT * FROM detection_data")
        rows= cur.fetchall()
        return rows
        
class StatThread(QThread):
    refresh_graph = pyqtSignal()
    def __init__(self, date_from, date_to, parent=None):
        super().__init__(parent)
        self.date_from = date_from
        self.date_to = date_to
        
    def run(self):
        cmd = os.popen("python mkgraph.py "+self.date_from+" "+self.date_to)
        print(cmd.read())
        self.refresh_graph.emit()
                
    def stop(self):
        self.quit()
                
class StatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/StatusWindow.ui", self)
        
        self.button_stat.clicked.connect(self.tolog)
        self.button_period.clicked.connect(self.setperiod)
        self.setscroll([])
        
    def setscroll(self, data):
        self.scroll_stat.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_stat)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_stat.setWidget(self.inner)
        for i in data:
            label=QLabel()
            label.setMinimumSize(1, 30)
            label.setMaximumSize(100, 30)
            label.setText(data[1])
            self.inner.layout().addWidget(label)
            
    def setperiod(self):
        date_from=self.date_from.text().replace("-","")
        date_to=self.date_to.text().replace("-","")
        
        self.calc = StatThread(date_from, date_to)
        self.calc.start()
        self.calc.refresh_graph.connect(self.refresh_graph)
        self.calc.stop()
        
    def refresh_graph(self):
        self.graph_detected.setPixmap(QtGui.QPixmap("graph/date.jpg"))
        self.graph_detected.repaint()
        self.graph_type.setPixmap(QtGui.QPixmap("graph/type.jpg"))
        self.graph_type.repaint()

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
