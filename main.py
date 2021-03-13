import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
import cv_ui
import unit1
import unit2


# def create_uuid(): #生成唯一的图片的名称字符串
#     nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # 当前时间
#     randomNum = random.randint(0, 100)
#     if randomNum <= 10:
#         randomNum = str(0) + str(randomNum)
#     uniqueNum = str(nowTime) + str(randomNum)
#     return uniqueNum


class MainDialog(QMainWindow):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.ui = cv_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('CV lrioxh')

        self.img = np.ndarray(())
        self.imgOrg=np.ndarray(())
        self.imgShow = np.ndarray(())
        self.w=0
        self.h=0
        self.c=1

        self.m_drag=False
        self.img2 = cv2.imread('images/Fig0327(a)(tungsten_original).tif',cv2.IMREAD_GRAYSCALE)
        self.img2Org = np.ndarray(())
        self.img2Show = np.ndarray(())
        self.img2Right=np.ndarray(())
        self.w2 = 0
        self.h2 = 0
        self.c2 = 1
        self.gMean=0
        self.gStd=0
        unit2.init(self)

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


        self.ui.pushButton_11.clicked.connect(self.choosePic2)
        self.ui.pushButton_12.clicked.connect(self.globalH)
        self.ui.pushButton_13.clicked.connect(self.localH)
        self.ui.pushButton_14.clicked.connect(self.showOrg)
        self.ui.pushButton_15.clicked.connect(self.gEqH)
        self.ui.pushButton_16.clicked.connect(self.CLAHE)
        self.ui.pushButton_17.clicked.connect(self.local_enhance)
        self.ui.pushButton_18.clicked.connect(self.reset2)

    def reset2(self):
        return unit2.reset2(self)

    def showOrg(self):
        return unit2.showOrg(self)

    def gEqH(self):
        return unit2.gEqH(self)

    def CLAHE(self):
        return unit2.CLAHE(self)

    def local_enhance(self):
        return unit2.local_enhance(self)

    def choosePic2(self):
        return unit2.choosePic2(self)

    def globalH(self):
        return unit2.globalH(self)

    def localH(self):
        return unit2.localH(self)


    ### U2/U1
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
    ###
    def mouseReleaseEvent(self, e):
        if Qt.LeftButton:
            if self.ui.tabWidget.currentIndex() == 0:
                return unit1.mouseReleaseEvent(self,e)
            if self.ui.tabWidget.currentIndex() == 1:
                return unit2.mouseReleaseEvent(self,e)
            else:
                return 0

    def mousePressEvent(self, e):
        if Qt.LeftButton:
            if self.ui.tabWidget.currentIndex() == 1:
                return unit2.mousePressEvent(self,e)

    def mouseMoveEvent(self, e):
        if self.ui.tabWidget.currentIndex() == 1:
            if Qt.LeftButton and self.m_drag:
                return unit2.mouseMoveEvent(self,e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    Dlg = MainDialog()
    Dlg.show()
    sys.exit(app.exec_())

    # pyuic5 -o cv_ui.py untitled.ui