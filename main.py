import sys
from PyQt5.QtWidgets import *
import cv_ui
import unit1
import numpy as np

# def create_uuid(): #生成唯一的图片的名称字符串
#     nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 当前时间
#     randomNum = random.randint(0, 100)
#     if randomNum <= 10:
#         randomNum = str(0) + str(randomNum)
#     uniqueNum = str(nowTime) + str(randomNum)
#     return uniqueNum


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        self.img = np.ndarray(())
        self.imgOrg=np.ndarray(())
        self.imgShow = np.ndarray(())
        self.w=0
        self.h=0
        self.c=1
        super(MainDialog, self).__init__(parent)
        self.ui = cv_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('CV lrioxh')

        self.ui.pushButton.clicked.connect(self.select_button_clicked)
        self.ui.pushButton_2.clicked.connect(self.showlarge)
        self.ui.pushButton_3.clicked.connect(self.saveimg)
        self.ui.pushButton_4.clicked.connect(self.trans_by_rate)
        self.ui.pushButton_5.clicked.connect(self.trans_by_pixel)
        self.ui.pushButton_6.clicked.connect(self.rotate)
        self.ui.pushButton_7.clicked.connect(self.scale_by_rate)
        self.ui.pushButton_8.clicked.connect(self.scale_by_pixel)
        self.ui.pushButton_9.clicked.connect(self.reset)
        self.ui.pushButton_10.clicked.connect(self.clear)

    def clear(self):
        return unit1.clear(self)

    def scale_by_pixel(self):
        return unit1.scale_by_pixel(self)

    def scale_by_rate(self):
        return unit1.scale_by_rate(self)

    def reset(self):
        return unit1.reset(self)

    def rotate(self):
        return unit1.rotate(self)

    def trans_by_pixel(self):
        return unit1.trans_by_pixel(self)

    def trans_by_rate(self):
        return unit1.trans_by_rate(self)

    def saveimg(self):
        return unit1.saveimg(self)

    def showlarge(self):
        return unit1.showlarge(self)

    def get_rgb(self, event, x, y, a, b):
        return unit1.get_rgb(self, event, x, y, a, b)

    def select_button_clicked(self):
        return unit1.select_button_clicked(self)

    def mouseReleaseEvent(self, e):
        return unit1.mouseReleaseEvent(self,e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    Dlg = MainDialog()
    Dlg.show()
    sys.exit(app.exec_())

    # pyuic5 -o cv_ui.py untitled.ui