import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import cv2
import numpy as np
from fucRGB import *
from fucBin import *
from fucGray import *


def init(self):
    self.imgCache = np.ndarray(())
    # self.imgRGB = np.ndarray(())
    self.imgLast = np.ndarray(())
    # self.imgShow = np.ndarray(())
    # self.imgGray= np.ndarray(())
    # self.imgBin= np.ndarray(())
    self.imgOgl=np.ndarray(())
    # self.type = 0
    # self.h = 0
    # self.c = 1
    self.Ogl=0


def Binwhich(self,btn):
    if self.imgCache.size == 1:
        return
    pic =self.ui.spinBox.value()
    if not pic:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入分块(默认1即不分块)  ')
        msg_box.exec_()
        return
    # self.imgBin = self.img.copy()
    self.imgLast=self.imgCache.copy()
    if len(self.imgCache.shape)==3:
        self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGR2GRAY)
    pic=int(pic)
    h, w = self.imgCache.shape[:2]
    hh = int(h / pic)
    hw = int(w / pic)
    # res = np.zeros(self.img.shape,np.uint8)
    for i in range(pic):
        for j in range(pic):
            cache = self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw)]
            if btn==14:
                cache = img_power_transform(cache,1, 1.9)
                cache = seperate_otsu(cache,block=(1,1))
            elif btn==16:
                cache = img_power_transform(cache,1, 1.9)
                cache = movingThreshold(cache,n=20,b=0.5)
            elif btn==25:
                cache = binopen(cache,ks=3)
            self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw)] = cache
    # self.img=gauss_division(self.img)
    # self.type=2
    refreshShow(self, self.imgCache)

def Graywhich(self,btn):
    if self.imgCache.size == 1:
        return
    pic =self.ui.spinBox.value()
    # print(pic)
    if not pic:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入分块(默认1即不分块)  ')
        msg_box.exec_()
        return
    if len(self.imgCache[self.imgCache==255])+len(self.imgCache[self.imgCache==0])==self.imgCache.size:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '当前图像可能为二值图像  ')
        msg_box.exec_()

    self.imgLast=self.imgCache.copy()
    if len(self.imgCache.shape)==3:
        self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGR2GRAY)
    pic=int(pic)
    h, w = self.imgCache.shape[:2]
    hh = int(h / pic)
    hw = int(w / pic)
    # res = np.zeros(self.img.shape,np.uint8)
    for i in range(pic):
        for j in range(pic):
            cache = self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw)]
            if btn==17:
                cache = hat_demo(cache,ks=5)
            elif btn==18:
                cache = unevenLightCompensate(cache, blockSize=16)
            elif btn == 19:
                cache = gauss_division(cache)
            elif btn == 20:
                # k = self.ui.spinBox_2.value()
                cache = USM(cache,0.3)
            elif btn == 21:
                cache = sharpening(cache)
            elif btn == 22:
                cache = streching(cache)
            elif btn == 23:
                cache = singalCLAHE(cache)
            elif btn == 24:
                cache = grayopen(cache,ks=3)
            self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw)] = cache
    # self.img=gauss_division(self.img)
    refreshShow(self, self.imgCache)

def RGBwhich(self,btn):
    if self.imgCache.size == 1:
        return
    pic =self.ui.spinBox.value()
    # print(pic)
    if not pic:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入分块(默认1即不分块)  ')
        msg_box.exec_()
        return
    if len(self.imgCache.shape)!=3:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '当前图像非RGB图像  ')
        msg_box.exec_()
        return
    self.imgLast=self.imgCache.copy()
    pic=int(pic)
    h, w = self.imgCache.shape[:2]
    hh = int(h / pic)
    hw = int(w / pic)
    # res = np.zeros(self.img.shape,np.uint8)
    for i in range(pic):
        for j in range(pic):
            cache = self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw), :]
            if btn==6:
                cache = gauss_division(cache)
            elif btn==7:
                cache = MSRCR(cache)
            elif btn == 8:
                cache = Saturation(cache,k=1.8)
            elif btn == 9:
                # k = self.ui.spinBox_2.value()
                cache = sharpening(cache)
            elif btn == 10:
                cache = streching(cache)
            elif btn == 12:
                cache = hisEqulColor2(cache)
            elif btn == 13:
                cache = erode(cache)
                cache = dilate(cache)
            elif btn == 15:
                cache = USM(cache,0.3)
            self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw), :] = cache
    # self.img=gauss_division(self.img)
    refreshShow(self, self.imgCache)


def refreshShow(self,img):
    # self.imgShow = img
    if img.size == 1:
        return
    self.Ogl = 0
    self.ui.label_2.setPixmap(QtGui.QPixmap(""))
    # self.imgGray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
    # self.imgBin = self.imgGray.copy()
    w_label = self.ui.label.width()
    h_label = self.ui.label.height()
    h = img.shape[0]
    w = img.shape[1]
    M=np.float32([[1, 0, 0], [0, 1, 0]])
    if h/w==h_label/w_label:
        data = img.tobytes()
        if len(self.imgCache.shape) == 3:
            image = QtGui.QImage(data, w, h, w * 3, QtGui.QImage.Format_BGR888)
        else:
            image = QtGui.QImage(data, w, h, w, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(w_label, h_label)
        self.ui.label.setPixmap(scale_pix)
        return
    elif h/w>h_label/w_label:
        h_=h
        w_=round(h*w_label/h_label)
        M[0, 2] += (w_ - w) / 2
        M[1, 2] += (h_ - h) / 2
    else:
        h_ = round(w * h_label / w_label)
        w_ = w
        M[0, 2] += (w_ - w) / 2
        M[1, 2] += (h_ - h) / 2

    # print(1)
    img = cv2.warpAffine(img, M, (w_, h_))
    # cv2.imshow('pic', self.imgShow)
    data = img.tobytes()
    if len(self.imgCache.shape) == 3:
        image = QtGui.QImage(data, w_, h_, w_ * 3, QtGui.QImage.Format_BGR888)
    else:
        image = QtGui.QImage(data, w_, h_, w_, QtGui.QImage.Format_Grayscale8)

    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(w_label, h_label)
    self.ui.label.setPixmap(scale_pix)


def choosepic(self):
    fileName, tmp = QFileDialog.getOpenFileName(self, '打开图像', 'Image', '*.png *.jpg *.bmp')
    print(fileName)
    if fileName is '':
        return
    root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
    pwd = os.getcwd()  # 返回当前工作目录
    if root_dir:
        os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
    # self.img = cv2.imread(file_name)
    self.imgCache = cv2.imread(fileName, -1)
    # self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGR2RGB)
    os.chdir(pwd)
    # cv2.imshow('pic', self.img)
    if self.imgCache.size == 1:
        return
    self.imgOgl = self.imgCache.copy()
    # self.h, self.w = self.img.shape[:2]
    if self.imgCache.shape[2] == 4:
        self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGRA2BGR)
    print(self.imgCache.shape)
    refreshShow(self,self.imgCache)

def compare(self):
    if self.Ogl==0:
        self.Ogl=1
        refreshShow2(self)
    else:
        self.Ogl=0
        self.ui.label_2.setPixmap(QtGui.QPixmap(""))

def refreshShow2(self):
    if self.imgOgl.size == 1:
        return
    w_label = self.ui.label_2.width()
    h_label = self.ui.label_2.height()
    h = self.imgOgl.shape[0]
    w = self.imgOgl.shape[1]
    M = np.float32([[1, 0, 0], [0, 1, 0]])
    if h / w == h_label / w_label:
        data = self.imgOgl.tobytes()
        if len(self.imgOgl.shape) == 3:
            image = QtGui.QImage(data, w, h, w * 3, QtGui.QImage.Format_BGR888)
        else:
            image = QtGui.QImage(data, w, h, w, QtGui.QImage.Format_Grayscale8)
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(w_label, h_label)
        self.ui.label_2.setPixmap(scale_pix)
        return
    elif h / w > h_label / w_label:
        h_ = h
        w_ = round(h * w_label / h_label)
        M[0, 2] += (w_ - w) / 2
        M[1, 2] += (h_ - h) / 2
    else:
        h_ = round(w * h_label / w_label)
        w_ = w
        M[0, 2] += (w_ - w) / 2
        M[1, 2] += (h_ - h) / 2

    # print(1)
    data = cv2.warpAffine(self.imgOgl, M, (w_, h_))
    # cv2.imshow('pic', self.imgShow)
    data = data.tobytes()
    if len(self.imgOgl.shape) == 3:
        image = QtGui.QImage(data, w_, h_, w_ * 3, QtGui.QImage.Format_BGR888)
    else:
        image = QtGui.QImage(data, w_, h_, w_, QtGui.QImage.Format_Grayscale8)

    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(w_label, h_label)
    self.ui.label_2.setPixmap(scale_pix)

def showlarge(self):
    if self.imgCache.size>1:
        cv2.namedWindow('large pic', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('large pic',self.imgCache)
        # cv2.setMouseCallback("large pic", self.get_rgb)
        cv2.waitKey()
    # else:
    #     msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像为空  ')
    #     msg_box.exec_()


def back(self):
    if self.imgLast.size == 1:
        return
    self.imgCache=self.imgLast.copy()
    refreshShow(self, self.imgCache)

def saveimg(self):
    if self.imgCache.size>1:
        fileName, tmp = QFileDialog.getSaveFileName(self, '保存图像', 'Image', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        print(fileName)
        root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
        pwd = os.getcwd()  # 返回当前工作目录
        if root_dir:
            os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
        # self.img = cv2.imread(file_name)
        # self.img = cv2.imread(fileName, -1)
        cv2.imwrite(fileName, self.imgCache)
        os.chdir(pwd)
    # else:
    #     msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像为空，无法保存  ')
    #     msg_box.exec_()

def reset(self):
    self.ui.spinBox.setValue(1)
    # self.ui.spinBox_2.setValue(1)
    # self.ui.spinBox_3.setValue(2)
    # self.ui.spinBox_4.setValue(2)
    if self.imgOgl.size>1:
        self.imgCache = self.imgOgl.copy()
        refreshShow(self, self.imgCache)
    # else:
    #     msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
    #     msg_box.exec_()


