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


class pltFigure6(FigureCanvas):
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
    self.img6 = cv2.imread('images/u6.tif', cv2.IMREAD_GRAYSCALE)
    self.img6Show = self.img6.copy()
    self.c6 = 1
    self.h6, self.w6 = self.img6.shape

    self.fig6 = pltFigure6(width=8, height=6, dpi=80)
    self.fig_ntb6 = NavigationToolbar(self.fig6, self)
    self.gridlayout6 = QGridLayout(self.ui.label_59)
    self.gridlayout6.addWidget(self.fig6)
    self.gridlayout6.addWidget(self.fig_ntb6)

    refrashShow(self)

def refrashShow(self):
    data = self.img6Show.tobytes()
    image = QtGui.QImage(data, self.w6, self.h6, self.w6 * self.c6, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(566, 482)
    self.ui.label_58.setPixmap(scale_pix)

