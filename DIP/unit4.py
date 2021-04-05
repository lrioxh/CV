import cv2
import numpy as np
# from skimage import morphology
from PyQt5 import QtGui
from PyQt5.QtWidgets import *

array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,\
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0,\
         1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]

def thin(img):
    h, w = img.shape
    i_thin = img.copy()
    for i in range(h):
        for j in range(w):
            if img[i, j] == 0:
                a = [1] * 9
                for k in range(3):
                    for l in range(3):
                        if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and i_thin[i - 1 + k, j - 1 + l] == 0:
                            a[k * 3 + l] = 0
                i_sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                i_thin[i, j] = array[i_sum]

    return i_thin

def thinCross(img):
    dst = img.copy()
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skeleton = np.zeros(dst.shape, np.float32)
    while (1):
        if np.sum(dst) <0.0001 :
            break
        dst = cv2.erode(dst, kernel)
        open_dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
        result = dst - open_dst
        skeleton = skeleton + result
    return skeleton

def thinRect(img):
    dst = img.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    skeleton = np.zeros(dst.shape, np.float32)
    while (1):
        if np.sum(dst) <0.0001:
            break
        dst = cv2.erode(dst, kernel)
        open_dst = cv2.morphologyEx(dst, cv2.MORPH_OPEN, kernel)
        result = dst - open_dst
        skeleton = skeleton + result
    return skeleton

def init(self):
    self.img4 = cv2.imread('../images/4Fig1027(a)(van_original).tif', cv2.IMREAD_GRAYSCALE)
    self.h4, self.w4 = self.img4.shape[:2]
    self.c4 = 1
    self.g=np.ndarray(())
    self.g1=np.ndarray(())
    self.g2=np.ndarray(())
    gray=self.img4/ 255.0
    gx = np.abs(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3))
    # print(gx)
    gy = np.abs(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3))
    self.mag, self.ang = cv2.cartToPolar(gx, gy, angleInDegrees=1)
    refrashShow(self, self.img4)

def refrashShow(self,img):
    data = img.tobytes()
    image = QtGui.QImage(data, self.w4, self.h4, self.w4 * self.c4, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    # print(self.w4,self.h4)
    scale_pix = pix.scaled(566, 534)
    self.ui.label_43.setPixmap(scale_pix)

def edge_connection(img, size, k):
    for i in range(size):
        Yi = np.where(img[i, :] > 0)
        if len(Yi[0]) >= 10: #可调整
            for j in range(0, len(Yi[0])-1):
                if Yi[0][j+1] - Yi[0][j] <= k:
                    img[i, Yi[0][j]:Yi[0][j+1]] = 1
    return img

def connect1(self):
    tm = float(self.ui.lineEdit_30.text())
    ta = float(self.ui.lineEdit_32.text())
    k = float(self.ui.lineEdit_36.text())
    X, Y = np.where((self.mag > np.max(self.mag) * tm) & ((self.ang >= 90-ta) & (self.ang <= 90+ta)))
    g = np.zeros((self.h4, self.w4))
    g[X, Y] = 1
    self.g1 = edge_connection(g, self.h4, k)
    g=255*self.g1.astype(np.uint8)
    refrashShow(self, g)

def connect2(self):
    tm = float(self.ui.lineEdit_35.text())
    ta = float(self.ui.lineEdit_33.text())
    k = float(self.ui.lineEdit_37.text())
    X, Y = np.where((self.mag > np.max(self.mag) * tm) & ((self.ang >= 0-ta) & (self.ang <= 0+ta)))
    g = np.zeros((self.h4, self.w4))
    g[X, Y] = 1
    g = cv2.rotate(g, 0)
    g = edge_connection(g, self.h4, k)
    self.g2 = cv2.rotate(g, 2)
    g=255*self.g2.astype(np.uint8)
    refrashShow(self, g)

def conbine(self):
    if self.g1.size==1 and self.g2.size==1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先进行边缘提取  ')
        msg_box.exec_()
        return
    g = self.g1 + self.g2
    g[g > 1] = 1
    self.g=g
    g = 255 * g.astype(np.uint8)
    refrashShow(self, g)

def refinement(self):
    if self.g.size==1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先进行合并  ')
        msg_box.exec_()
        return
    # skeleton =morphology.skeletonize(self.g)
    skeleton = np.zeros(self.g.shape, np.float32)
    if self.ui.radioButton_5.isChecked():
        skeleton = thinCross(self.g)
    if self.ui.radioButton_6.isChecked():
        skeleton = thinRect(self.g)
    if self.ui.radioButton_7.isChecked():
        skeleton = thin(1-self.g)
        skeleton = 1 - skeleton
    g = np.uint8(skeleton)
    g[g==1]=255
    refrashShow(self, g)

def clear4(self):
    self.g = np.ndarray(())
    self.g1 = np.ndarray(())
    self.g2 = np.ndarray(())
    self.ui.lineEdit_30.setText('%s' % 0.3)
    self.ui.lineEdit_32.setText('%s' % 45)
    self.ui.lineEdit_36.setText('%s' % 25)
    self.ui.lineEdit_35.setText('%s' % 0.3)
    self.ui.lineEdit_33.setText('%s' % 45)
    self.ui.lineEdit_37.setText('%s' % 25)
    refrashShow(self, self.img4)


