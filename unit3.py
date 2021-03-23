from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import cv2
import numpy as np

def mmin(x,y):
    if x>y:return y
    else:return x
def mmax(x,y):
    if x<y:return y
    else:return x

def mousePressEvent(self, e):
    globalpos = e.globalPos()
    pos = self.ui.label_36.mapFromGlobal(globalpos)
    pos2 = self.ui.label_31.mapFromGlobal(globalpos)
    if pos.y() < 246 and pos.y() > 0 and pos.x() > 0 and pos.x() < 168:
        self.m_drag = True
        self.m_DragPosition = pos
        e.accept()
    elif pos2.y() < 337 and pos2.y() > 0 and pos2.x() > 0 and pos2.x() < 337:
        self.m_drag = True
        self.m_DragPosition = pos2
        e.accept()

def mouseReleaseEvent(self, e):
    globalpos = e.globalPos()
    pos = self.ui.label_36.mapFromGlobal(globalpos)
    pos2 = self.ui.label_31.mapFromGlobal(globalpos)
    if pos.y() < 246 and pos.y() > 0 and pos.x() > 0 and pos.x() < 168:
        self.m_drag = False
    elif pos2.y() < 337 and pos2.y() > 0 and pos2.x() > 0 and pos2.x() < 337:
        self.m_drag = False

def mouseMoveEvent(self, e):
    globalpos = e.globalPos()
    pos = self.ui.label_36.mapFromGlobal(globalpos)
    pos2 = self.ui.label_31.mapFromGlobal(globalpos)
    if pos.y() < 246 and pos.y() > 0 and pos.x() > 0 and pos.x() < 168:
        # h = self.img2Show.shape[0]
        # w = self.img2Show.shape[1]
        h = 246
        w = 168
        Ox=self.m_DragPosition.x() *2
        Oy=self.m_DragPosition.y() *2
        D = round(2*pow((pos.x() - self.m_DragPosition.x()) ** 2 + (pos.y() - self.m_DragPosition.y()) ** 2, 0.5))
        if self.ui.radioButton.isChecked():
            self.ui.lineEdit_18.setText('%s, %s' % (Ox,Oy))
            self.ui.lineEdit_19.setText('%s' % D)
        if self.ui.radioButton_2.isChecked():
            self.ui.lineEdit_21.setText('%s, %s' % (Ox,Oy))
            self.ui.lineEdit_20.setText('%s' % D)
        if self.ui.radioButton_3.isChecked():
            self.ui.lineEdit_23.setText('%s, %s' % (Ox,Oy))
            self.ui.lineEdit_22.setText('%s' % D)
        if self.ui.radioButton_4.isChecked():
            self.ui.lineEdit_25.setText('%s, %s' % (Ox,Oy))
            self.ui.lineEdit_24.setText('%s' % D)
        e.accept()
    elif pos2.y() < 337 and pos2.y() > 0 and pos2.x() > 0 and pos2.x() < 337:
        # h = self.img2Show.shape[0]
        # w = self.img2Show.shape[1]
        h = 337
        w = 337
        self.ui.lineEdit_27.setText(
            '%s, %s' % (self.m_DragPosition.x() *4, self.m_DragPosition.y() *4))
        self.ui.lineEdit_28.setText('%s' % ((pos2.x() - self.m_DragPosition.x())*4))
        self.ui.lineEdit_29.setText('%s' % ((pos2.y() - self.m_DragPosition.y())*4))
        e.accept()

def init(self):
    self.img31 = cv2.imread('images/unit3_1.tif', cv2.IMREAD_GRAYSCALE)
    self.img31Dft = np.ndarray(())
    self.img31Res = np.ndarray(())
    self.img31Fil = np.ndarray(())
    self.c31 = 1
    self.img32 = cv2.imread('images/unit3_2.tif', cv2.IMREAD_GRAYSCALE)
    self.img32Dft = np.ndarray(())
    self.img32Res = np.ndarray(())
    self.img32Fil = np.ndarray(())
    self.c32 = 1

    self.h31, self.w31 = self.img31.shape
    self.h32, self.w32 = self.img32.shape

    data = self.img31.tobytes()
    image = QtGui.QImage(data, self.w31, self.h31, self.w31 * self.c31, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(168, 246)
    self.ui.label_35.setPixmap(scale_pix)

    data = self.img32.tobytes()
    image = QtGui.QImage(data, self.w32, self.h32, self.w32 * self.c32, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(337, 337)
    self.ui.label_33.setPixmap(scale_pix)

def DFT31(self):
    if self.img31Dft.size==1:
        padding = cv2.copyMakeBorder(self.img31, 0, self.h31, 0, self.w31, cv2.BORDER_CONSTANT, value=0)
        # dft = cv2.dft(np.float32(padding), flags=cv2.DFT_COMPLEX_OUTPUT)
        dft = np.fft.fft2(padding)
        self.img31Dft = np.fft.fftshift(dft)
    # magnitude_spectrum = np.log(cv2.magnitude(self.img31Dft[:, :, 0], self.img31Dft[:, :, 1]))
    magnitude_spectrum=np.log(np.abs(self.img31Dft)+1)
    normalize=(magnitude_spectrum-2) / (np.max(magnitude_spectrum-2))
    magnitude_spectrum_uint8=np.uint8(255*(np.power(normalize,2)))

    data = magnitude_spectrum_uint8.tobytes()
    image = QtGui.QImage(data, self.w31*2, self.h31*2, self.w31*2 * self.c31, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(168, 246)
    self.ui.label_36.setPixmap(scale_pix)

def DFT32(self):
    if self.img32Dft.size==1:
        padding = cv2.copyMakeBorder(self.img32, 0, self.h32, 0, self.w32, cv2.BORDER_CONSTANT, value=0)
        dft = cv2.dft(np.float32(padding), flags=cv2.DFT_COMPLEX_OUTPUT)
        # dft = np.fft.fft2(padding)
        self.img32Dft = np.fft.fftshift(dft)

    magnitude_spectrum = np.log(cv2.magnitude(self.img32Dft[:, :, 0], self.img32Dft[:, :, 1])+1)
    # magnitude_spectrum = np.log(np.abs(self.img32Dft)+1)
    normalize = (magnitude_spectrum-1) / (np.max(magnitude_spectrum) -1)
    magnitude_spectrum_uint8 = np.uint8(255 * (np.power(normalize, 2)))

    data = magnitude_spectrum_uint8.tobytes()
    image = QtGui.QImage(data, self.w32*2, self.h32*2, self.w32*2 * self.c32, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(337, 337)
    self.ui.label_31.setPixmap(scale_pix)

def TRAP31(self):
    rank = int(self.ui.lineEdit_26.text())
    D=[]; r=[]
    D.append(self.ui.lineEdit_18.text())
    D.append(self.ui.lineEdit_21.text())
    D.append(self.ui.lineEdit_23.text())
    D.append(self.ui.lineEdit_25.text())
    r.append(self.ui.lineEdit_19.text())
    r.append(self.ui.lineEdit_20.text())
    r.append(self.ui.lineEdit_22.text())
    r.append(self.ui.lineEdit_24.text())
    radius=0
    if self.img31Dft.size==1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先进行DFT  ')
        msg_box.exec_()
        return
    w = self.w31 * 2
    h = self.h31 * 2
    self.img31Fil = self.img31Dft.copy()
    for p in range(4):
        if D[p] and r[p]:
            cx, cy = D[p].split(', ')
            cx = int(cx); cy = int(cy)
            radius = float(r[p])
            cx_ = w - cx
            cy_ = h - cy
            # 计算以中心为原点坐标分量
            u = np.array([[x - cx for x in range(w)] for i in range(h)], dtype=np.float32)
            v = np.array([[y - cy for y in range(h)] for i in range(w)], dtype=np.float32).T
            # 每个点到中心的距离
            dis = np.sqrt(u * u + v * v)
            filt = 1 / (1 + np.power(dis / radius, 2 * rank))

            u = np.array([[x - cx_ for x in range(w)] for i in range(h)], dtype=np.float32)
            v = np.array([[y - cy_ for y in range(h)] for i in range(w)], dtype=np.float32).T
            dis = np.sqrt(u * u + v * v)
            filt_ = 1 / (1 + np.power(dis / radius, 2 * rank))
            # self.img31Fil=np.zeros((self.h31*2, self.w31*2), np.float32)
            # self.img31Fil[:,:,0] = self.img31Dft[:,:,0] * filt
            # self.img31Fil[:, :, 1] = self.img31Dft[:, :, 1] * filt
            if self.ui.checkBox_2.isChecked():
                self.img31Fil = self.img31Fil * filt * filt_
            else:
                self.img31Fil = self.img31Fil * (1.0001-filt) * (1.0001-filt_)
    if radius==0:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请至少输入或选择一个陷波区域  ')
        msg_box.exec_()
        return

    magnitude_spectrum = np.log(np.abs(self.img31Fil)+1)
    normalize = (magnitude_spectrum -2) / (np.max(magnitude_spectrum) -2)
    # print(np.max(normalize), np.min(normalize))
    magnitude_spectrum_uint8 = np.uint8(255 * (np.power(normalize, 2)))

    data = magnitude_spectrum_uint8.tobytes()
    image = QtGui.QImage(data, w, h, w * self.c31, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(168, 246)
    self.ui.label_36.setPixmap(scale_pix)

def iDFT31(self):
    if self.img31Fil.size == 1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先进行陷波  ')
        msg_box.exec_()
        return
    f_ishift = np.fft.ifftshift(self.img31Fil)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    img_back_uint8 = np.uint8(255 * (img_back / np.max(img_back)))
    img_back_uint8=img_back_uint8[:self.h31,:self.w31]
    data = img_back_uint8.tobytes()
    image = QtGui.QImage(data, self.w31, self.h31, self.w31 * self.c31, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(168, 246)
    self.ui.label_29.setPixmap(scale_pix)

def TRAP32(self):
    O=self.ui.lineEdit_27.text()
    ww=self.ui.lineEdit_28.text()
    hh=self.ui.lineEdit_29.text()
    if self.img32Dft.size == 1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先进行DFT  ')
        msg_box.exec_()
        return
    w = self.w32 * 2
    h = self.h32 * 2
    self.img32Fil = self.img32Dft.copy()
    if O and ww and hh:
        cx, cy = O.split(', ')
        cx = int(cx)
        cy = int(cy)
        ww = int(ww)
        hh = int(hh)
        cx_ = w - cx
        cy_ = h - cy
        filt=np.ones((h,w,2),np.float32)
        filt[mmin(cy,cy+hh):mmax(cy,cy+hh),mmin(cx,cx+ww)-4:mmax(cx,cx+ww)-4,:]=0.0001
        filt[mmin(cy_-hh+1,cy_+1):mmax(cy_-hh+1,cy_+1),mmin(cx_-ww+1,cx_+1)+4:mmax(cx_-ww+1,cx_+1)+4,:]=0.0001
        if self.ui.checkBox.isChecked():
            self.img32Fil =(1.0001- filt)*self.img32Fil
        else:
            self.img32Fil =filt* self.img32Fil
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请输入或选择陷波区域  ')
        msg_box.exec_()
        return
    # magnitude_spectrum = np.log(np.abs(self.img32Fil)+1)
    magnitude_spectrum = np.log(cv2.magnitude(self.img32Fil[:, :, 0], self.img32Fil[:, :, 1]) + 1)
    normalize = (magnitude_spectrum -1) / (np.max(magnitude_spectrum)-1)
    magnitude_spectrum_uint8 = np.uint8(255 * (np.power(normalize, 2)))

    data = magnitude_spectrum_uint8.tobytes()
    image = QtGui.QImage(data, w, h, w * self.c32, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(337, 337)
    self.ui.label_31.setPixmap(scale_pix)

def iDFT32(self):
    if self.img32Fil.size == 1:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '请先进行陷波  ')
        msg_box.exec_()
        return
    f_ishift = np.fft.ifftshift(self.img32Fil)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
    img_back_uint8 = np.uint8(255 * (img_back / np.max(img_back)))
    img_back_uint8=img_back_uint8[:self.h32,:self.w32]
    data = img_back_uint8.tobytes()
    image = QtGui.QImage(data, self.w32, self.h32, self.w32 * self.c32, QtGui.QImage.Format_Grayscale8)
    pix = QtGui.QPixmap.fromImage(image)
    scale_pix = pix.scaled(337, 337)
    self.ui.label_34.setPixmap(scale_pix)