from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

class pltFigure(FigureCanvas):
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


def init(self):
    self.img2 = cv2.imread('../images/Fig0327(a)(tungsten_original).tif', cv2.IMREAD_GRAYSCALE)
    self.img2Org = np.ndarray(())
    self.img2Show = np.ndarray(())
    self.img2Right = np.ndarray(())
    self.c2 = 1
    # self.gMean, self.gStd = cv2.meanStdDev(self.img2)
    # self.gMean = round(self.gMean[0][0], 3)
    # self.gStd = round(self.gStd[0][0], 3)
    self.h2, self.w2 = self.img2.shape
    self.img2Org=self.img2.copy()

    self.fig1 = pltFigure(width=5, height=3, dpi=80)
    self.fig_ntb1 = NavigationToolbar(self.fig1, self)
    self.gridlayout1 = QGridLayout(self.ui.label_18)
    self.gridlayout1.addWidget(self.fig1)
    self.gridlayout1.addWidget(self.fig_ntb1)

    refreshShow(self)

def mouseReleaseEvent(self, e):
    globalpos = e.globalPos()
    pos = self.ui.label_16.mapFromGlobal(globalpos)
    if pos.y() < 298 and pos.y() > 0 and pos.x() > 0 and pos.x() < 252:
        self.m_drag = False

def mousePressEvent(self, e):
    globalpos = e.globalPos()
    pos = self.ui.label_16.mapFromGlobal(globalpos)
    if pos.y() < 298 and pos.y() > 0 and pos.x() > 0 and pos.x() < 252:
        self.m_drag = True
        self.m_DragPosition = pos
        e.accept()

def mouseMoveEvent(self, e):
    globalpos = e.globalPos()
    pos = self.ui.label_16.mapFromGlobal(globalpos)
    if pos.y() < 298 and pos.y() > 0 and pos.x() > 0 and pos.x() < 252:
        h = self.img2Show.shape[0]
        w = self.img2Show.shape[1]
        self.ui.lineEdit_9.setText('%s' % round(self.m_DragPosition.x()/252*w))
        self.ui.lineEdit_10.setText('%s' % round(pos.x()/252*w))
        self.ui.lineEdit_15.setText('%s' % round(self.m_DragPosition.y()/ 298 * h))
        self.ui.lineEdit_16.setText('%s' % round(pos.y()/ 298 * h))
        e.accept()

def choosePic2(self):
    fileName, tmp = QFileDialog.getOpenFileName(self, '打开图像', 'Image', '*.png *.jpg *.bmp *.tif')
    print(fileName)
    if fileName is '':
        return
    self.img2 = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    self.img2Org = self.img2.copy()
    # cv2.imshow('pic', self.img)
    if self.img2.size == 1:
        return
    self.gMean, self.gStd = cv2.meanStdDev(self.img2)
    self.gMean=round(self.gMean[0][0],3)
    self.gStd=round(self.gStd[0][0],3)
    self.h2, self.w2 = self.img2.shape
    refreshShow(self)

def refreshShow(self):
    self.img2Show = self.img2

    M=np.float32([[1, 0, 0], [0, 1, 0]])
    # print(M)
    if self.h2/self.w2==298/252:
        data = self.img2Show.tobytes()
        image = QtGui.QImage(data, self.w2, self.h2, self.w2 * self.c2, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(252, 298)
        self.ui.label_16.setPixmap(scale_pix)
        return
    elif self.h2/self.w2>298/252:
        h_=self.h2
        w_=round(self.h2*252/298+0.5)
        M[0, 2] += (w_ - self.w2) / 2
        M[1, 2] += (h_ - self.h2) / 2
    else:
        h_ = round(self.w2 * 298 / 252+0.5)
        w_ = self.w2
        M[0, 2] += (w_ - self.w2) / 2
        M[1, 2] += (h_ - self.h2) / 2

    # print(1)
    self.img2Show = cv2.warpAffine(self.img2Show, M, (w_, h_))
    # cv2.imshow('pic', self.imgShow)
    data = self.img2Show.tobytes()
    image = QtGui.QImage(data, w_, h_, w_ * self.c2, QtGui.QImage.Format_Grayscale8)

    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(252, 298)
    self.ui.label_16.setPixmap(scale_pix)

def globalH(self):
    hist = np.bincount(self.img2.ravel(), minlength=256)
    self.fig1.axes.cla()
    self.fig1.axes.plot(hist)
    self.fig1.draw()

    Mean, Std = cv2.meanStdDev(self.img2)
    Mean = round(Mean[0][0], 3)
    Std = round(Std[0][0], 3)
    self.ui.textBrowser_2.setText('%s' % Mean)
    self.ui.textBrowser_5.setText('%s' % Std)

def localH(self):
    x1 = self.ui.lineEdit_9.text()
    x2 = self.ui.lineEdit_10.text()
    y1 = self.ui.lineEdit_15.text()
    y2 = self.ui.lineEdit_16.text()
    if x1 and y1 and x2 and y2:
        x1 = int(x1); x2 = int(x2)
        y1 = int(y1); y2 = int(y2)
        if x1>x2:
            m=x1;x1=x2;x2=m
        if y1>y2:
            m = y1;y1 = y2;y2 = m
        img = self.img2Show[y1:y2,x1:x2]
        Mean,Std=cv2.meanStdDev(img)
        Mean = round(Mean[0][0], 3)
        Std = round(Std[0][0], 3)
        self.ui.textBrowser_2.setText('%s' % Mean)
        self.ui.textBrowser_5.setText('%s' % Std)

        hist = np.bincount(img.ravel(), minlength=256)
        self.fig1.axes.cla()
        self.fig1.axes.plot(hist)
        self.fig1.draw()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入或选择区域  ')
        msg_box.exec_()

def local_enhance(self):
    E = float(self.ui.lineEdit_11.text())
    k0 = float(self.ui.lineEdit_12.text())
    k1 = float(self.ui.lineEdit_13.text())
    k2 = float(self.ui.lineEdit_14.text())
    l = float(self.ui.lineEdit_17.text())
    self.img2Right = self.img2Org.copy()
    border=int((l-1)/2)
    padding=cv2.copyMakeBorder(self.img2Org, border,border,border,border, cv2.BORDER_CONSTANT, value=0)
    gMean, gStd = cv2.meanStdDev(padding)
    gMean = round(gMean[0][0], 3)
    gStd = round(gStd[0][0], 3)
    # img=padding
    for i in range(border,border+self.h2):
        for j in range(border,border+self.w2):
            # print(j)
            if j==border:
                M,S=cv2.meanStdDev(padding[i-border:i+border+1,j-border:j+border+1])
                M=M[0][0];S=S[0][0]
            else:
                Mf=M;Sf=S
                # M2, S22 = cv2.meanStdDev(padding[i - border:i + border+1, j - border:j + border+1])
                a=padding[i-border:i+border+1,j+border].astype("int32")
                b=padding[i-border:i+border+1,j-border-1].astype("int32")
                M=round(Mf+float(sum(a)-sum(b))/l**2,7)
                S2=Sf**2+Mf**2-M**2+float(sum(a**2)-sum(b**2))/l**2
                if S2>0:
                    S=round(pow(S2,0.5),5)
                else:
                    S=0

            if M<=k0*gMean and k1*gStd<=S and S<=k2*gStd:
                self.img2Right[i-border,j-border]=E*padding[i,j]
                # img[i, j] = E * padding[i, j]
    # return img
    M = np.float32([[1, 0, 0], [0, 1, 0]])
    # print(M)
    if self.h2 / self.w2 == 298 / 252:
        data = self.img2Right.tobytes()
        image = QtGui.QImage(data, self.w2, self.h2, self.w2 * self.c2, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(252, 298)
        self.ui.label_17.setPixmap(scale_pix)
        return
    elif self.h2 / self.w2 > 298 / 252:
        h_ = self.h2
        w_ = round(self.h2 * 252 / 298 + 0.5)
        M[0, 2] += (w_ - self.w2) / 2
        M[1, 2] += (h_ - self.h2) / 2
    else:
        h_ = round(self.w2 * 298 / 252 + 0.5)
        w_ = self.w2
        M[0, 2] += (w_ - self.w2) / 2
        M[1, 2] += (h_ - self.h2) / 2

    # print(1)
    self.img2Right = cv2.warpAffine(self.img2Right, M, (w_, h_))
    # cv2.imshow('pic', self.imgShow)
    data = self.img2Right.tobytes()
    image = QtGui.QImage(data, w_, h_, w_ * self.c2, QtGui.QImage.Format_Grayscale8)

    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(252, 298)
    self.ui.label_17.setPixmap(scale_pix)

def gEqH(self):
    self.img2 = cv2.equalizeHist(self.img2Org)
    refreshShow(self)
def CLAHE(self):
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
    self.img2=clahe.apply(self.img2Org)
    refreshShow(self)
def showOrg(self):
    self.img2=self.img2Org.copy()
    refreshShow(self)

def reset2(self):
    self.img2 = cv2.imread('images/Fig0327(a)(tungsten_original).tif',cv2.IMREAD_GRAYSCALE)
    self.img2Show = np.ndarray(())
    self.img2Right=np.ndarray(())
    self.w2 = 0
    self.h2 = 0
    self.c2 = 1
    self.ui.lineEdit_11.setText('4')
    self.ui.lineEdit_12.setText('0.4')
    self.ui.lineEdit_13.setText('0.02')
    self.ui.lineEdit_14.setText('0.4')
    self.ui.lineEdit_17.setText('3')
    self.ui.label_17.setPixmap(QtGui.QPixmap(""))

    self.gMean, self.gStd = cv2.meanStdDev(self.img2)
    self.gMean = round(self.gMean[0][0], 3)
    self.gStd = round(self.gStd[0][0], 3)
    self.h2, self.w2 = self.img2.shape
    self.img2Org = self.img2.copy()

    refreshShow(self)
