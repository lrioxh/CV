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


class pltFigure5(FigureCanvas):
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
    self.img51 = cv2.imread('images/u51.tif', cv2.IMREAD_GRAYSCALE)
    self.img51Show = self.img51.copy()
    self.c51 = 1
    self.h51, self.w51 = self.img51.shape

    self.img52 = cv2.imread('images/u52.tif', cv2.IMREAD_GRAYSCALE)
    self.img52Show = self.img52.copy()
    self.c52 = 1
    self.h52, self.w52 = self.img52.shape

    self.fig5 = pltFigure5(width=8, height=6, dpi=80)
    self.fig_ntb5 = NavigationToolbar(self.fig5, self)
    self.gridlayout5 = QGridLayout(self.ui.label_54)
    self.gridlayout5.addWidget(self.fig5)
    self.gridlayout5.addWidget(self.fig_ntb5)

    refrashShowRight(self)
    refrashShowLeft(self)

def refrashShowLeft(self):
    data = self.img52Show.tobytes()
    image = QtGui.QImage(data, self.w52, self.h52, self.w52 * self.c52, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(355, 409)
    self.ui.label_48.setPixmap(scale_pix)

def refrashShowRight(self):
    data = self.img51Show.tobytes()
    image = QtGui.QImage(data, self.w51, self.h51, self.w51 * self.c51, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(407, 326)
    self.ui.label_46.setPixmap(scale_pix)

def gradient51(self):
    rate = float(self.ui.lineEdit_31.text())/100.0
    sobelx = cv2.Sobel(self.img51, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(self.img51, cv2.CV_64F, 0, 1, ksize=3)
    mag = np.abs(sobelx) + np.abs(sobely)
    # mag, ang = cv2.cartToPolar(sobelx, sobely, angleInDegrees=1)
    index = int(self.img51.size * rate)
    threshold = np.sort(mag.reshape(1, -1))[0, index]
    X, Y = np.where((mag > threshold))
    g = np.zeros(self.img51.shape)
    g[X, Y] = 1
    self.img51Show = np.uint8(g * self.img51)
    # cv2.imshow("g", self.img51Show)
    # cv2.waitKey(0)

    refrashShowRight(self)


def H51(self):
    if np.sum(self.img51Show[self.img51Show < 255])==0:
        g = self.img51Show.ravel()
    else:
        g = self.img51Show[self.img51Show > 0]
    h = np.bincount(np.uint8(g), minlength=256)
    maxsigma = 0
    threshold = 0
    gi = []
    for i in range(0, 255):
        g1 = g[g <= i]
        g2 = g[g > i]
        if len(g1) > 0 and len(g2) > 0:
            mean1 = np.mean(g1)
            mean2 = np.mean(g2)
            p1 = len(g1) / len(g)
            sigma = p1 * (1 - p1) * (mean1 - mean2) ** 2
            gi.append(sigma)
            if maxsigma < sigma:
                maxsigma = sigma
                threshold = i
        else:
            gi.append(0)

    threshold = int(threshold + gi.count(maxsigma) * 0.5)
    self.ui.lineEdit_34.setText('%s' % threshold)
    self.fig5.axes.cla()
    self.fig5.axes.bar(np.array([n for n in range(256)]), h)
    self.fig5.axes.axvline(threshold, color='r')
    self.fig5.axes.scatter([n for n in range(255)], np.array(gi) * 0.5 * np.max(h) / np.max(gi), marker='.')
    self.fig5.draw()

def segmentation(self):
    threshold=self.ui.lineEdit_34.text()
    if threshold:
        threshold =int(threshold)
        self.img51Show[self.img51 > threshold] = 255
        self.img51Show[self.img51 <= threshold] = 0
        refrashShowRight(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先输入或生成分割阈值  ')
        msg_box.exec_()


def original51(self):
    self.img51Show=self.img51.copy()
    refrashShowRight(self)


def gradient52(self):
    rate = float(self.ui.lineEdit_38.text())/100.0
    gray_lap = cv2.Laplacian(self.img52, cv2.CV_64F, ksize=1)
    mag = np.abs(gray_lap)
    threshold=rate*np.max(mag)
    X, Y = np.where((mag > threshold))
    g = np.zeros(self.img52.shape)
    g[X, Y] = 1
    self.img52Show = np.uint8(g * self.img52)

    refrashShowLeft(self)


def H52(self):
    if np.sum(self.img52Show[self.img52Show < 255])==0:
        g = self.img52Show.ravel()
    else:
        g = self.img52Show[self.img52Show > 0]
    h = np.bincount(np.uint8(g), minlength=256)
    maxsigma = 0
    threshold=0
    gi = []
    for i in range(0, 255):
        g1 = g[g <= i]
        g2 = g[g > i]
        if len(g1) > 0 and len(g2) > 0:
            mean1 = np.mean(g1)
            mean2 = np.mean(g2)
            p1=len(g1)/len(g)
            sigma = p1 * (1-p1) * (mean1 - mean2) ** 2
            gi.append(sigma)
            if maxsigma < sigma:
                maxsigma = sigma
                threshold = i
        else:
            gi.append(0)

    threshold = int(threshold + gi.count(maxsigma) * 0.5)
    self.ui.lineEdit_34.setText('%s' % threshold)
    self.fig5.axes.cla()
    self.fig5.axes.bar(np.array([n for n in range(256)]), h)
    self.fig5.axes.axvline(threshold, color='r')
    self.fig5.axes.scatter([n for n in range(255)], np.array(gi) * 0.5 * np.max(h) / np.max(gi), marker='.')
    self.fig5.draw()

def segmentation52(self):
    threshold=self.ui.lineEdit_34.text()
    if threshold:
        threshold =int(threshold)
        self.img52Show[self.img52 > threshold] = 255
        self.img52Show[self.img52 <= threshold] = 0
        refrashShowLeft(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先输入或生成分割阈值  ')
        msg_box.exec_()


def original52(self):
    self.img52Show=self.img52.copy()
    refrashShowLeft(self)
