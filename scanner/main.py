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