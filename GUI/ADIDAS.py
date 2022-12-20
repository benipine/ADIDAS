import os
import sys
import time
import sqlite3
import hashlib
import RPi.GPIO as GPIO

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.uic import *

conn = sqlite3.connect("adidas.db")
cur = conn.cursor()
id_list = list()
pw_list = list()
PWDialog = uic.loadUiType("UI/ChangePW.ui")[0]
buzzer = 18
led=17

def GPIO_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(led, GPIO.OUT)
    GPIO.setwarnings(False)
    GPIO.output(buzzer, GPIO.LOW)
    GPIO.output(led, False)
    GPIO.cleanup()
    
def getidpw():
    idfile = open("UI/id.txt", 'r')
    pwfile = open("UI/pw.txt", 'r')
    tmp_id = idfile.readlines()
    tmp_pw = pwfile.readlines()
    for i in range(len(tmp_id)):
        id_list.append(tmp_id[i].strip())
        pw_list.append(tmp_pw[i].strip())
    idfile.close()
    pwfile.close()
    
def encrypt(tmp):
    return hashlib.sha256(tmp.encode()).hexdigest()

class ChangePW(QtWidgets.QDialog, PWDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.button_save.clicked.connect(self.save)
        
    def save(self):
        cur_id = encrypt(self.input_id.text())
        cur_pw = encrypt(self.input_oldpw.text())
        new_pw = encrypt(self.input_newpw.text())
        con_pw = encrypt(self.confirm_newpw.text())
        
        if cur_id not in id_list:
            QMessageBox.critical(self, 'Changing Password Failed', 'Current ID or Current PASSWORD is wrong')
        else:
            if cur_pw != pw_list[id_list.index(cur_id)]:
                QMessageBox.critical(self, 'Changing Password Failed', 'Current ID or Current PASSWORD is wrong')
            else:
                if con_pw != new_pw:
                     QMessageBox.critical(self, 'Changing Password Failed', 'New Password does not match with Confirm Password')
                else:
                    pw_list[id_list.index(cur_id)] = new_pw
                    pwfile = open("UI/pw.txt", 'w')
                    for i in range(len(pw_list)):
                        pwfile.write(str(pw_list[i])+"\n")
                    QMessageBox.information(self, 'Password Changed', 'Your password has been changed!')
                    pwfile.close()
                    self.close()
        
class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        loadUi("UI/LoginWindow.ui", self)

        self.button_login.clicked.connect(self.loginclick)
        self.button_changepw.clicked.connect(self.changepw)
        
    def loginclick(self):
        login_id = encrypt(self.input_id.text())
        login_pw = encrypt(self.input_pw.text())

        if login_id not in id_list:
            self.loginwrong()
        else:
            if login_pw != pw_list[id_list.index(login_id)]:
                self.loginwrong()
            else:
                widget.setCurrentIndex(widget.currentIndex()+1)
    
    def changepw(self):
        changepw = ChangePW()
        changepw.exec_()
        
    def loginwrong(self):
        QMessageBox.critical(self, 'Login Failed', 'ID or PASSWORD is wrong')

class BLThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(buzzer, GPIO.OUT)
        GPIO.setup(led, GPIO.OUT)
        GPIO.setwarnings(False)
    
    def run(self):
        try:
            for i in range(30):
                GPIO.output(buzzer, GPIO.HIGH)
                GPIO.output(led, True)
                time.sleep(0.05)
                GPIO.output(buzzer, GPIO.LOW)
                GPIO.output(led, False)
                time.sleep(0.05)
        except:
            print("error")
    
        finally:
            GPIO.cleanup()
            self.quit()
            
class ImageThread(QThread):
    refresh_window = pyqtSignal(str, int)
    new_detection = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        
        cmd= os.popen("cd ~/adidas/ADIDAS/GUI/fullimage && ls")
        result_old = cmd.read().strip()
        while(1):
            cmd= os.popen("cd ~/adidas/ADIDAS/GUI/fullimage && ls")
            result_new = cmd.read().strip()
            time.sleep(1)
            if result_new != result_old:
                self.new_detection.emit()
                fname = result_new.replace(result_old, "").strip()
                result_old = result_new
                os.system("python imgdtndb.py "+fname)
                self.blthread = BLThread()
                self.blthread.start()
                self.refresh_window.emit(fname, 1)
        
class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/LogWindow.ui", self)
        
        self.button_logs.clicked.connect(self.tostatus)
        self.button_download.clicked.connect(self.download)
        
        self.db = self.get_db()
        try:
            self.refresh_window(str(self.db[-1][1])+".jpg", 1)
        except:
            print("")
        
        self.check_image = ImageThread()
        self.check_image.start()
        self.check_image.refresh_window.connect(self.refresh_window)
        self.check_image.new_detection.connect(self.new_detection)
        
    def refresh_window(self, fname, isnew):
        if isnew == 1:
            self.setscroll()
            
        index = 0
        det_type = ""
        for i in self.db:
            if i[1] == fname.strip(".jpg"):
                index = i[0]
                det_type = i[2].upper()
                det_name = i[3].upper()
                break
        date_a = self.adjust_date(fname)
        self.log_title.setText("Log # "+str(index)+" "*10+"Time : "+date_a+" (KST)")
        self.type_text.setText("TYPE : "+det_type)
        self.drone_name.setText(det_name)
        self.image_before.setPixmap(QtGui.QPixmap("fullimage/"+fname))
        self.image_after.setPixmap(QtGui.QPixmap("cropimage/"+fname))
        self.drone_image.setPixmap(QtGui.QPixmap("UI/GUI_basicimage/drone_image.png"))
        self.image_before.repaint()
        self.image_after.repaint()
        self.drone_image.repaint()
        self.button_download.setObjectName("d"+fname)
        
    def setscroll(self):
        self.scroll_log.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_log)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_log.setWidget(self.inner)
        self.db = self.get_db()
        for i in reversed(self.db):
            buttonname = str(i[1])
            button=QPushButton(objectName=buttonname)
            button.setMinimumSize(1, 30)
            button.setMaximumSize(100000, 30)
            button.setStyleSheet("font: 75 12pt 'PibotoLt';"
            "background-color: rgb(255, 255, 255);"
            "text-align: left;")
            date_a=self.adjust_date(i[1])
            button.setText(" "*60+"Log # "+str(i[0])+" "*80+date_a+" "*80+i[2].upper())
            button.clicked.connect(self.button_work)
            self.inner.layout().addWidget(button)
            
    def button_work(self):
        sending_button = self.sender()
        self.refresh_window(str(sending_button.objectName())+".jpg", 0)
        
    def new_detection(self):
        self.log_title.setText("Loading New Log ...")
        self.type_text.setText("TYPE : Detecting ...")
        self.drone_name.setText("Detecting ...")
        self.image_before.clear()
        self.image_after.clear()
        self.drone_image.clear()
        self.image_before.setText("New Image Detected and Loading ...")
        self.image_after.setText("New Image Detected and Loading ...")
        self.drone_image.setText("New Image\nDetected and Loading ...")
            
    def adjust_date(self, date):
        return date[0:4]+"-"+date[4:6]+"-"+date[6:8]+" "+date[8:10]+":"+date[10:12]+":"+date[12:14]
        
    def get_db(self):
        cur.execute("SELECT * FROM detection_data")
        rows= cur.fetchall()
        return rows
        
    def download(self):
        sending_button = self.sender().objectName().replace("d","")
        os.system("cp "+"~/adidas/ADIDAS/GUI/fullimage/"+sending_button+" ~/Desktop/"+self.adjust_date(sending_button).replace(" ","_")+".jpg")
        QMessageBox.information(self, 'Download Success', 'Your image file has been successfully downloaded to\n~/Desktop folder')
        
    def tostatus(self):
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class StatThread(QThread):
    refresh_graph = pyqtSignal(list)
    def __init__(self, date_from, date_to, parent=None):
        super().__init__(parent)
        self.date_from = date_from
        self.date_to = date_to
        
    def run(self):
        cmd = os.popen("python mkgraph.py "+self.date_from+" "+self.date_to+" 0")
        cmdlist = cmd.read().split(";")
        finallist = list()
        for i in cmdlist:
            finallist.append(i.strip().strip("[").strip("]").split(", "))
        self.refresh_graph.emit(finallist)
                
    def stop(self):
        self.quit()
        
class DownThread(QThread):
    complete_alert = pyqtSignal()
    def __init__(self, date_from, date_to, parent=None):
        super().__init__(parent)
        self.date_from = date_from
        self.date_to = date_to
        
    def run(self):
        os.system("python mkgraph.py "+self.date_from+" "+self.date_to+" 1")
        self.complete_alert.emit()
                
    def stop(self):
        self.quit()
                
class StatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("UI/StatusWindow.ui", self)
        
        self.button_stat.clicked.connect(self.tolog)
        self.button_period.clicked.connect(self.setperiod)
        self.button_csv.clicked.connect(self.downloadcsv)
        self.setscroll([])
        
    def setperiod(self):
        self.date_f=self.date_from.text().replace("-","")
        self.date_t=self.date_to.text().replace("-","")
        self.loading()
        self.calc = StatThread(self.date_f, self.date_t)
        self.calc.start()
        self.calc.refresh_graph.connect(self.refresh_graph)
        self.calc.stop()
        
    def loading(self):
        self.graph_detected.clear()
        self.graph_type.clear()
        self.graph_detected.setText("Loading ...")
        self.graph_type.setText("Loading ...")
        
        self.scroll_stat.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_stat)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_stat.setWidget(self.inner)
        label=QLabel()
        label.setMinimumSize(1100, 30)
        label.setMaximumSize(1100, 30)
        label.setText("Loading ...")
        label.setAlignment(Qt.AlignCenter)
        self.inner.layout().addWidget(label)
        
    def refresh_graph(self, data):
        self.graph_detected.setPixmap(QtGui.QPixmap("graph/date.jpg"))
        self.graph_type.setPixmap(QtGui.QPixmap("graph/type.jpg"))
        self.graph_detected.repaint()
        self.graph_type.repaint()
        self.setscroll(data)
        
    def setscroll(self, data):
        self.scroll_stat.setWidgetResizable(True)
        self.inner = QFrame(self.scroll_stat)
        self.inner.setLayout(QVBoxLayout())
        self.scroll_stat.setWidget(self.inner)
        try:
            for j in range(len(data[0])):
                text=" "*26
                text += data[0][j][0:4]+"-"+data[0][j][4:6]+"-"+data[0][j][6:8]+" "*91
                text += data[1][j]+" "*98
                text += data[2][j]+"%"
                label=QLabel()
                label.setMinimumSize(1000, 30)
                label.setMaximumSize(1000, 30)
                label.setText(text)
                self.inner.layout().addWidget(label)
        except:
            pass

    def downloadcsv(self):
        try:
            self.down = DownThread(self.date_f, self.date_t)
            self.downloading()
            self.down.start()
            self.down.complete_alert.connect(self.downsuccess)
            self.down.stop()
            
        except:
            QMessageBox.warning(self, 'Download Failed', 'Set period first to Download in .csv file')
        
    def downloading(self):
        self.button_csv.setEnabled(False)
        self.button_csv.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.button_csv.setText("Downloading ...")
        
    def downsuccess(self):
        self.button_csv.setEnabled(True)
        self.button_csv.setText("Download as .csv")
        self.button_csv.setStyleSheet("background-color: rgb(255, 153, 69);")
        QMessageBox.information(self, 'Download Success', 'Your .csv file has been successfully downloaded!')
        
    def tolog(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        
if __name__=='__main__':
    GPIO_init()
    getidpw()
    
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
