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


class RegionGrowing():
    def __init__(self,img):
        self.img=img

    # def setSeed(self,seed):
    #     if type(seed) != int:
    #         return TypeError("Seed必须是整数值！")
    #     if 0>seed or seed>255:
    #         return ValueError("Seed必须在0~255之间！")
    #     Q = np.where(self.img>=seed,1,0)
    #     Q = Q.astype(np.uint8)
    #     # 种子图片
    #     # cv2.imshow("intseed",255*Q)
    #     # cv2.waitKey()
    #     return Q

    # def grow(self,Q,maxInter=64):
        # 确定边缘以及颜色最小值&最大值


    def threshold_two(self,t1,t2,v1,v2,v3):# 0 255 128
        inverse_img = 255 - self.img
        dst=np.zeros(inverse_img.shape,np.uint8)
        dst=v3+dst
        dst[inverse_img>t2]=v2
        dst[inverse_img<t1]=v1
        # for i in range(inverse_img.shape[0]):
        #     for j in range(inverse_img.shape[1]):
        #         if inverse_img[i,j]<t1:
        #             inverse_img[i,j] = v1
        #         elif self.img[i,j]>t2:
        #             inverse_img[i,j] = v3
        #         else:
        #             inverse_img[i,j] = v2
        return dst

def init(self):
    self.img6 = np.uint8(cv2.imread('images/u6.tif', cv2.IMREAD_GRAYSCALE))
    self.img6Show = self.img6.copy()
    self.c6 = 1
    self.h6, self.w6 = self.img6.shape
    self.iSEED=np.ndarray(())
    self.fSEED = np.ndarray(())

    self.fig6 = pltFigure6(width=8, height=6, dpi=80)
    self.fig_ntb6 = NavigationToolbar(self.fig6, self)
    self.gridlayout6 = QGridLayout(self.ui.label_59)
    self.gridlayout6.addWidget(self.fig6)
    self.gridlayout6.addWidget(self.fig_ntb6)

    # self.project6 = RegionGrowing(self.img6)

    refrashShow(self)

def refrashShow(self):
    data = self.img6Show.tobytes()
    image = QtGui.QImage(data, self.w6, self.h6, self.w6 * self.c6, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(566, 482)
    self.ui.label_58.setPixmap(scale_pix)

def doubleTH(self):
    t1 = self.ui.lineEdit_39.text()
    t2 = self.ui.lineEdit_40.text()
    if t1 and t2:
        t1=int(t1)
        t2=int(t2)
        inverse_img = 255 - self.img6
        self.img6Show = np.zeros(inverse_img.shape, np.uint8)
        self.img6Show = 128 + self.img6Show
        self.img6Show[inverse_img > t2] = 255
        self.img6Show[inverse_img < t1] = 0
        # self.img6Show = self.project6.threshold_two(t1, t2, 0, 255, 128)
        refrashShow(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先输入  ')
        msg_box.exec_()

def min2TH(self):
    t1 = self.ui.lineEdit_39.text()
    if t1:
        t1=int(t1)
        inverse_img = 255 - self.img6
        self.img6Show = np.zeros((self.h6,self.w6), np.uint8)
        self.img6Show[inverse_img > t1] = 255
        refrashShow(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先输入  ')
        msg_box.exec_()

def initSeed(self):
    t = self.ui.lineEdit_41.text()
    if t:
        t=int(t)
        if type(t) != int:
            return TypeError("Seed必须是整数值！")
        if 0>t or t>255:
            return ValueError("Seed必须在0~255之间！")
        self.iSEED = np.where(self.img6>=t,1,0).astype(np.uint8)
        # Q = Q.astype(np.uint8)

        # self.iSEED = self.project6.setSeed(int(t))
        self.img6Show = self.iSEED*255
        refrashShow(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先输入  ')
        msg_box.exec_()

def finSeed(self):
    if self.iSEED.size==1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先生成初始种子  ')
        msg_box.exec_()
        return
    thresh_B = np.zeros((self.h6,self.w6), np.uint8)  # thresh_B大小与A相同，像素值为0
    thresh_A_copy = self.iSEED.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))  # 3×3结构元

    count = []  # 为了记录连通分量中的像素个数
    liantong_dict = {}

    # 循环，直到thresh_A_copy中的像素值全部为0
    while thresh_A_copy.any():

        Xa_copy, Ya_copy = np.where(thresh_A_copy > 0)  # thresh_A_copy中值为255的像素的坐标
        thresh_B[Xa_copy[0]][Ya_copy[0]] = 1  # 选取第一个点，并将thresh_B中对应像素值改为255

        # 连通分量算法，先对thresh_B进行膨胀，再和thresh_A执行and操作（取交集）
        for i in range(200):
            dilation_B = cv2.dilate(thresh_B, kernel, iterations=1)
            thresh_B = cv2.bitwise_and(self.iSEED, dilation_B)

        # 取thresh_B值为255的像素坐标，并将thresh_A_copy中对应坐标像素值变为0
        Xb, Yb = np.where(thresh_B > 0)
        thresh_A_copy[Xb, Yb] = 0

        # 显示连通分量及其包含像素数量
        count.append(len(Xb))
        if len(count) == 0:
            print("无连通分量")
        if len(count) == 1:
            print("第1个连通分量为{0},坐标为{1}".format(count[0], (Xa_copy[0], Ya_copy[0])))
            liantong_dict[str(len(count))] = (Xa_copy[0], Ya_copy[0])
        if len(count) >= 2:
            print("第{0}个连通分量为{1},坐标为{2}".format(len(count), count[-1] - count[-2], (Xa_copy[0], Ya_copy[0])))
            liantong_dict[str(len(count))] = (Xa_copy[0], Ya_copy[0])

    self.fSEED = np.zeros((self.h6,self.w6),np.uint8)
    for i in range(len(count)):
        m, n = liantong_dict[str(i + 1)]
        self.fSEED[m, n] = 1

    self.img6Show = self.fSEED * 255
    refrashShow(self)

def grow6(self):
    if self.fSEED.size==1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '种子为空  ')
        msg_box.exec_()
        return
    elif self.ui.lineEdit_42.text():
        maxInter=int(self.ui.lineEdit_42.text())
        Q=self.fSEED
        max_gray = int(np.max(self.img6 * Q))
        min_gray = 255
        Q_edges = []
        for i in range(1, Q.shape[0] - 1):
            for j in range(1, Q.shape[1] - 1):
                if Q[i, j] == 0:
                    continue
                if np.sum(Q[i - 1:i + 2, j - 1:j + 2]) != 9:
                    Q_edges.append((i, j))
                if self.img6[i, j] < min_gray:
                    min_gray = self.img6[i, j]

        end_flag = 0
        while (end_flag == 0):
            # 在边缘找符合条件的点生长
            end_flag = 1
            new_Q_edges = Q_edges.copy()
            for i, j in Q_edges:
                around_list = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                               (i, j - 1), (i, j + 1),
                               (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]
                for location in around_list:
                    try:
                        if Q[location[0], location[1]] == 1:  # 已经加入Q中的点不用再判断
                            continue
                    except:
                        continue
                    if location in Q_edges:
                        continue
                    if abs(min_gray - int(self.img6[location[0], location[1]])) <= maxInter \
                            or abs(int(self.img6[location[0], location[1]]) - max_gray) <= maxInter \
                            :
                        Q[location[0], location[1]] = 1
                        new_Q_edges.append(location)
                        end_flag = 0
                if np.sum(Q[i - 1:i + 2, j - 1:j + 2]) == 9:
                    new_Q_edges.remove((i, j))

            Q_edges = new_Q_edges
            if end_flag == 1:
                # return Q
                self.img6Show=Q*255
                refrashShow(self)

        # self.img6Show=self.project6.grow(self.fSEED,
        #                                  maxInter=int(self.ui.lineEdit_42.text()))*255
        # refrashShow(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先输入  ')
        msg_box.exec_()

def original6(self):
    self.img6Show = self.img6
    refrashShow(self)

def inverse6(self):
    self.img6Show=255-self.img6Show
    refrashShow(self)

def H6(self):
    h = np.bincount(np.uint8(self.img6Show.ravel()), minlength=256)
    self.fig6.axes.cla()
    self.fig6.axes.bar(np.array([n for n in range(256)]), h)
    self.fig6.draw()

