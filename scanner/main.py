###  pyuic5 -o ./scanner/ui.py ./scanner/scanner.ui
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
import ui, scan


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.ui = ui.Ui_scanner()
        self.ui.setupUi(self)
        self.setWindowTitle('scanner')
        scan.init(self)
        self.ui.pushButton.clicked.connect(self.choosepic)
        self.ui.pushButton_5.clicked.connect(self.compare)
        self.ui.pushButton_4.clicked.connect(self.large)
        self.ui.pushButton_11.clicked.connect(self.back)
        self.ui.pushButton_3.clicked.connect(self.save)
        self.ui.pushButton_2.clicked.connect(self.reset)
        self.ui.pushButton_6.clicked.connect(lambda:self.RGBwhich(6))
        self.ui.pushButton_7.clicked.connect(lambda:self.RGBwhich(7))
        self.ui.pushButton_8.clicked.connect(lambda:self.RGBwhich(8))
        self.ui.pushButton_9.clicked.connect(lambda:self.RGBwhich(9))
        self.ui.pushButton_10.clicked.connect(lambda:self.RGBwhich(10))
        self.ui.pushButton_12.clicked.connect(lambda:self.RGBwhich(12))
        self.ui.pushButton_13.clicked.connect(lambda:self.RGBwhich(13))
        self.ui.pushButton_14.clicked.connect(lambda:self.Binwhich(14))
        self.ui.pushButton_15.clicked.connect(lambda:self.RGBwhich(15))
        self.ui.pushButton_16.clicked.connect(lambda:self.Binwhich(16))
        self.ui.pushButton_17.clicked.connect(lambda:self.Graywhich(17))
        self.ui.pushButton_18.clicked.connect(lambda:self.Graywhich(18))
        self.ui.pushButton_19.clicked.connect(lambda:self.Graywhich(19))
        self.ui.pushButton_20.clicked.connect(lambda:self.Graywhich(20))
        self.ui.pushButton_21.clicked.connect(lambda:self.Graywhich(21))
        self.ui.pushButton_22.clicked.connect(lambda:self.Graywhich(22))
        self.ui.pushButton_23.clicked.connect(lambda:self.Graywhich(23))
        self.ui.pushButton_24.clicked.connect(lambda:self.Graywhich(24))
        self.ui.pushButton_25.clicked.connect(lambda:self.Binwhich(25))



    def reset(self):
        return scan.reset(self)
    def save(self):
        return scan.saveimg(self)
    def back(self):
        return scan.back(self)
    def RGBwhich(self,btn):
        return scan.RGBwhich(self,btn)
    def Binwhich(self,btn):
        return scan.Binwhich(self,btn)
    def Graywhich(self,btn):
        return scan.Graywhich(self,btn)
    def large(self):
        return scan.showlarge(self)
    def choosepic(self):
        return scan.choosepic(self)
    def compare(self):
        return scan.compare(self)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    Dlg = MainDialog()
    Dlg.show()
    sys.exit(app.exec_())