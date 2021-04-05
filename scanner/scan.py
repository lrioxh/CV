from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import cv2
import numpy as np


def init(self):
    self.img = np.ndarray(())
    self.imgShow = np.ndarray(())
    self.imgGray= np.ndarray(())
    self.imgOgl=np.ndarray(())
    self.w = 0
    self.h = 0
    self.c = 1
    self.Ogl=0


def refreshShow(self):
    self.imgShow = self.img
    w_label = self.ui.label.width()
    h_label = self.ui.label.height()
    self.h = self.imgShow.shape[0]
    self.w = self.imgShow.shape[1]
    M=np.float32([[1, 0, 0], [0, 1, 0]])
    if self.h/self.w==h_label/w_label:
        data = self.imgShow.tobytes()
        if self.c == 3:
            image = QtGui.QImage(data, self.w, self.h, self.w * self.c, QtGui.QImage.Format_BGR888)
        else:
            image = QtGui.QImage(data, self.w, self.h, self.w * self.c, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(w_label, h_label)
        self.ui.label.setPixmap(scale_pix)
        return
    elif self.h/self.w>h_label/w_label:
        h_=self.h
        w_=round(self.h*w_label/h_label+0.5)
        M[0, 2] += (w_ - self.w) / 2
        M[1, 2] += (h_ - self.h) / 2
    else:
        h_ = round(self.w * h_label / w_label+0.5)
        w_ = self.w
        M[0, 2] += (w_ - self.w) / 2
        M[1, 2] += (h_ - self.h) / 2

    # print(1)
    self.imgShow = cv2.warpAffine(self.imgShow, M, (w_, h_))
    # cv2.imshow('pic', self.imgShow)
    data = self.imgShow.tobytes()
    if self.c==3:
        image = QtGui.QImage(data, w_, h_, w_ * self.c, QtGui.QImage.Format_BGR888)
    else:
        image = QtGui.QImage(data, w_, h_, w_ * self.c, QtGui.QImage.Format_Grayscale8)

    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(w_label, h_label)
    self.ui.label.setPixmap(scale_pix)


def choosepic(self):
    fileName, tmp = QFileDialog.getOpenFileName(self, '打开图像', 'Image', '*.png *.jpg *.bmp')
    print(fileName)
    if fileName is '':
        return
    self.img = cv2.imread(fileName, -1)
    self.imgOgl = self.img.copy()
    self.imgGray=cv2.cvtColor(self.img,cv2.COLOR_RGB2GRAY)
    # cv2.imshow('pic', self.img)
    if self.img.size == 1:
        return
    if len(self.img.shape) > 1:
        self.c = self.img.shape[2]
    refreshShow(self)

def compare(self):
    if self.Ogl==0:
        self.Ogl=1
        refreshShow2(self,self.imgOgl)
    else:
        self.Ogl=0
        self.ui.label_2.setPixmap(QtGui.QPixmap(""))

def refreshShow2(self,img):
    if img.size == 1:
        return
    w_label = self.ui.label_2.width()
    h_label = self.ui.label_2.height()
    h = img.shape[0]
    w = img.shape[1]
    M = np.float32([[1, 0, 0], [0, 1, 0]])
    if h / w == h_label / w_label:
        data = img.tobytes()
        if self.c == 3:
            image = QtGui.QImage(data, w, h, w * self.c, QtGui.QImage.Format_BGR888)
        else:
            image = QtGui.QImage(data, w, h, w * self.c, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(w_label, h_label)
        self.ui.label_2.setPixmap(scale_pix)
        return
    elif h / w > h_label / w_label:
        h_ = h
        w_ = round(self.h * w_label / h_label + 0.5)
        M[0, 2] += (w_ - w) / 2
        M[1, 2] += (h_ - h) / 2
    else:
        h_ = round(w * h_label / w_label + 0.5)
        w_ = w
        M[0, 2] += (w_ - w) / 2
        M[1, 2] += (h_ - h) / 2

    # print(1)
    img = cv2.warpAffine(img, M, (w_, h_))
    # cv2.imshow('pic', self.imgShow)
    data = img.tobytes()
    if self.c == 3:
        image = QtGui.QImage(data, w_, h_, w_ * self.c, QtGui.QImage.Format_BGR888)
    else:
        image = QtGui.QImage(data, w_, h_, w_ * self.c, QtGui.QImage.Format_Grayscale8)

    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(w_label, h_label)
    self.ui.label_2.setPixmap(scale_pix)

def showlarge(self):
    if self.img.size>1:
        cv2.namedWindow('large pic', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('large pic',self.img)
        # cv2.setMouseCallback("large pic", self.get_rgb)
        cv2.waitKey()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像为空  ')
        msg_box.exec_()


