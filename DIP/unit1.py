from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import cv2
import numpy as np
import os


def clear(self):
    self.img = np.ndarray(())
    self.imgOrg = np.ndarray(())
    self.imgShow = np.ndarray(())
    self.w = 0
    self.h = 0
    self.c = 1
    self.ui.textBrowser.setText('')
    self.ui.textBrowser_3.setText('')
    self.ui.textBrowser_4.setText('')
    self.ui.label_10.setPixmap(QtGui.QPixmap(""))

def select_button_clicked(self):
    fileName, tmp = QFileDialog.getOpenFileName(self, '打开图像', 'Image', '*.png *.jpg *.bmp *.jpeg')
    print(fileName)
    if fileName is '':
        return
    root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
    pwd = os.getcwd()  # 返回当前工作目录
    if root_dir:
        os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
    self.img = cv2.imread(file_name, -1)
    os.chdir(pwd)
    if self.img.size <= 1:
        return
    self.fname = file_name.split('.')[0]
    self.imgOrg = self.img.copy()
    if len(self.img.shape) == 3:
        self.c = self.img.shape[2]
        if self.img.shape[2] == 4:
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGRA2BGR)
    print(self.img.shape)
    refreshShow(self)

def reset(self):
    if self.img.size>1:
        self.img = self.imgOrg
        refreshShow(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()

def refreshShow(self):
    # else:
    #     self.h, self.w = self.img.shape
    self.imgShow = self.img
    self.h = self.imgShow.shape[0]
    self.w = self.imgShow.shape[1]
    # c=self.c
    self.ui.textBrowser.setText('%s×%s×%s' % (self.w, self.h, self.c))
    # M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, 1)
    M=np.float32([[1, 0, 0], [0, 1, 0]])
    # print(M)
    if self.h/self.w==3/4:
        data = self.imgShow.tobytes()
        if self.c == 3:
            image = QtGui.QImage(data, self.w, self.h, self.w * self.c, QtGui.QImage.Format_BGR888)
        else:
            image = QtGui.QImage(data, self.w, self.h, self.w * self.c, QtGui.QImage.Format_Grayscale8)

        w_label = self.ui.label_10.width()
        h_label = self.ui.label_10.height()
        pix = QtGui.QPixmap.fromImage(image)
        scale_pix = pix.scaled(w_label, h_label)
        self.ui.label_10.setPixmap(scale_pix)
        return
    elif self.h/self.w>3/4:
        h_=self.h
        w_=int(self.h*4/3+0.5)
        M[0, 2] += (w_ - self.w) / 2
        M[1, 2] += (h_ - self.h) / 2
    else:
        h_ = int(self.w * 3 / 4+0.5)
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

    w_label = self.ui.label_10.width()
    h_label = self.ui.label_10.height()
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(w_label, h_label)
    self.ui.label_10.setPixmap(scale_pix)

def mouseReleaseEvent(self, e):
    if self.imgShow.size>1:
        h = self.imgShow.shape[0]
        w = self.imgShow.shape[1]
        c=self.c
        globalpos=e.globalPos()
        pos=self.ui.label_10.mapFromGlobal(globalpos)
        # print(pos)
        if pos.y()<540 and pos.y()>0 and pos.x()>0 and pos.x()<720:
            x=int(pos.x()/720*w)
            y = int(pos.y() / 540 * h)
            # print(x,y)
            # print(self.imgShow[y,x])
            self.ui.textBrowser_4.setText(' (%s, %s)'% (x,y))
            if c==3:
                rgb=self.imgShow[y,x]
                self.ui.textBrowser_3.setText(' R%s G%s B%s'%(rgb[2],rgb[1],rgb[0]))
            else:
                gray=self.imgShow[y,x]
                self.ui.textBrowser_3.setText(' G %s' % gray)

def scale_by_pixel(self):
    if self.img.size>1:
        x=self.ui.lineEdit_7.text()
        y=self.ui.lineEdit_8.text()
        if x and y:
            try:
                x=int(x)
                y=int(y)
                self.img = cv2.resize(self.img, (x, y))
                refreshShow(self)
            except:
                msg_box = QMessageBox(QMessageBox.Warning, '警告', '输入错误  ')
                msg_box.exec_()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入  ')
            msg_box.exec_()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()

def scale_by_rate(self):
    if self.img.size>1:
        r = self.ui.lineEdit_6.text()
        if r:
            r=float(r)/100
            self.img = cv2.resize(self.img, (0, 0), fx=r, fy=r,
                                   interpolation=cv2.INTER_NEAREST)
            refreshShow(self)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入  ')
            msg_box.exec_()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()


def rotate(self):
    if self.img.size>1:
        a = self.ui.lineEdit_5.text()
        if a:
            a=float(a)
            M = cv2.getRotationMatrix2D((self.w / 2, self.h / 2), a, 1)
            angle = a * np.pi / 180
            w = int(self.w * abs(np.cos(angle)) + self.h * abs(np.sin(angle)) + 0.5)
            h = int(self.w * abs(np.sin(angle)) + self.h * abs(np.cos(angle)) + 0.5)
            M[0, 2] += (w - self.w) / 2
            M[1, 2] += (h - self.h) / 2
            self.img = cv2.warpAffine(self.img, M, (w, h))
            refreshShow(self)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入  ')
            msg_box.exec_()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()

def trans_by_pixel(self):
    if self.img.size>1:
        x=self.ui.lineEdit_3.text()
        y=self.ui.lineEdit_4.text()
        if x and y:
            x=int(x)
            y=int(y)
            M = np.float32([[1, 0, x], [0, 1, y]])
            self.img = cv2.warpAffine(self.img, M, (self.w, self.h))
            refreshShow(self)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入  ')
            msg_box.exec_()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()

def trans_by_rate(self):
    if self.img.size>1:
        x=self.ui.lineEdit.text()
        y=self.ui.lineEdit_2.text()
        if x and y:
            x=float(x)/100
            y=float(y)/100
            M = np.float32([[1, 0, x * self.w], [0, 1, y * self.h]])
            self.img = cv2.warpAffine(self.img, M, (self.w, self.h))
            refreshShow(self)
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入  ')
            msg_box.exec_()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()

def saveimg(self):
    if self.img.size>1:
        fileName, tmp = QFileDialog.getSaveFileName(self, '保存图像', str(self.fname)+'_fin', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        print(fileName)
        root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
        pwd = os.getcwd()  # 返回当前工作目录
        if root_dir:
            os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
        cv2.imwrite(file_name, self.img)
        os.chdir(pwd)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像为空，无法保存  ')
        msg_box.exec_()


def showlarge(self):
    if self.img.size>1:
        cv2.imshow('Original pic',self.img)
        cv2.setMouseCallback("Original pic", self.get_rgb)
        cv2.waitKey(0)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
        msg_box.exec_()

def get_rgb(self, event, x, y, a, b):
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(self.img[y, x])
        self.ui.textBrowser_4.setText(' (%s, %s)' % (x, y))
        if self.c == 3:
            rgb = self.img[y, x]
            self.ui.textBrowser_3.setText(' R%s G%s B%s' % (rgb[2], rgb[1], rgb[0]))
        else:
            gray = self.img[y, x]
            self.ui.textBrowser_3.setText(' G %s ' % gray)