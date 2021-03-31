import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import numpy as np
import cv_ui
import unit1,unit2,unit3,unit4,unit5,unit6


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
        self.m_drag = False
        self.img = np.ndarray(())
        self.imgOrg=np.ndarray(())
        self.imgShow = np.ndarray(())
        self.w=0
        self.h=0
        self.c=1
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

        unit2.init(self)
        self.ui.pushButton_11.clicked.connect(self.choosePic2)
        self.ui.pushButton_12.clicked.connect(self.globalH)
        self.ui.pushButton_13.clicked.connect(self.localH)
        self.ui.pushButton_14.clicked.connect(self.showOrg)
        self.ui.pushButton_15.clicked.connect(self.gEqH)
        self.ui.pushButton_16.clicked.connect(self.CLAHE)
        self.ui.pushButton_17.clicked.connect(self.local_enhance)
        self.ui.pushButton_18.clicked.connect(self.reset2)

        unit3.init(self)
        self.ui.pushButton_20.clicked.connect(self.DFT31)
        self.ui.pushButton_22.clicked.connect(self.DFT32)
        self.ui.pushButton_19.clicked.connect(self.TRAP31)
        self.ui.pushButton_21.clicked.connect(self.iDFT31)
        self.ui.pushButton_23.clicked.connect(self.TRAP32)
        self.ui.pushButton_24.clicked.connect(self.iDFT32)

        unit4.init(self)
        self.ui.pushButton_25.clicked.connect(self.showOrg4)
        self.ui.pushButton_26.clicked.connect(self.connect1)
        self.ui.pushButton_27.clicked.connect(self.connect2)
        self.ui.pushButton_28.clicked.connect(self.conbine)
        self.ui.pushButton_29.clicked.connect(self.refinement)
        self.ui.pushButton_30.clicked.connect(self.clear4)

        unit5.init(self)
        self.ui.pushButton_31.clicked.connect(self.original51)
        self.ui.pushButton_32.clicked.connect(self.gradient51)
        self.ui.pushButton_33.clicked.connect(self.H51)
        self.ui.pushButton_35.clicked.connect(self.segmentation)
        self.ui.pushButton_39.clicked.connect(self.original52)
        self.ui.pushButton_36.clicked.connect(self.gradient52)
        self.ui.pushButton_40.clicked.connect(self.H52)
        self.ui.pushButton_37.clicked.connect(self.segmentation52)

        unit6.init(self)

    def original52(self):
        return unit5.original52(self)

    def segmentation52(self):
        return unit5.segmentation52(self)

    def H52(self):
        return unit5.H52(self)

    def gradient52(self):
        return unit5.gradient52(self)

    def original51(self):
        return unit5.original51(self)

    def segmentation(self):
        return unit5.segmentation(self)

    def H51(self):
        return unit5.H51(self)

    def gradient51(self):
        return unit5.gradient51(self)

    ### U5/U4
    def clear4(self):
        return unit4.clear4(self)

    def showOrg4(self):
        return unit4.refrashShow(self, self.img4)

    def refinement(self):
        return unit4.refinement(self)

    def conbine(self):
        return unit4.conbine(self)

    def connect2(self):
        return unit4.connect2(self)

    def connect1(self):
        return unit4.connect1(self)

    ### U4/U3
    def iDFT32(self):
        return unit3.iDFT32(self)

    def TRAP32(self):
        return unit3.TRAP32(self)

    def iDFT31(self):
        return unit3.iDFT31(self)

    def TRAP31(self):
        return unit3.TRAP31(self)

    def DFT32(self):
        return unit3.DFT32(self)

    def DFT31(self):
        return unit3.DFT31(self)

    ### U3/U2
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
            if self.ui.tabWidget.currentIndex() == 2:
                return unit3.mouseReleaseEvent(self,e)

    def mousePressEvent(self, e):
        if Qt.LeftButton:
            if self.ui.tabWidget.currentIndex() == 1:
                return unit2.mousePressEvent(self,e)
            if self.ui.tabWidget.currentIndex() == 2:
                return unit3.mousePressEvent(self,e)

    def mouseMoveEvent(self, e):
        if Qt.LeftButton and self.m_drag:
            if self.ui.tabWidget.currentIndex() == 1:
                return unit2.mouseMoveEvent(self,e)
            if self.ui.tabWidget.currentIndex() == 2:
                return unit3.mouseMoveEvent(self,e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    Dlg = MainDialog()
    Dlg.show()
    sys.exit(app.exec_())

    # pyuic5 -o cv_ui.py untitled.ui