import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from scanner.fucRGB import *
from scanner.fucBin import *
from scanner.fucGray import *
# from scanner.drawPlt import Point_Move

def init(self):
    self.imgCache = np.ndarray(())
    self.imgLast = np.ndarray(())
    self.imgOgl=np.ndarray(())
    self.imgTrans=np.ndarray(())
    self.imgShow=np.ndarray(())
    self.imgMulti=[]
    self.points=np.zeros((4,2),np.float32)
    self.fname=''
    self.Ogl=0

def mouseReleaseEvent(self, e):
    if self.imgShow.size>1:
        h = self.imgShow.shape[0]
        w = self.imgShow.shape[1]
        globalpos=e.globalPos()
        pos=self.ui.label.mapFromGlobal(globalpos)
        # print(pos)
        if pos.y()<730 and pos.y()>0 and pos.x()>0 and pos.x()<900:
            x= pos.x()/900*w
            y = pos.y() / 730 * h
            if self.ui.lineEdit.text()=='':
                self.ui.lineEdit.setText(' %d,%d'% (x,y))
                self.points[0,:]=(x,y)
            elif self.ui.lineEdit_3.text()=='':
                self.ui.lineEdit_3.setText(' %d,%d'% (x,y))
                self.points[1,:]=(x,y)
            elif self.ui.lineEdit_2.text()=='':
                self.ui.lineEdit_2.setText(' %d,%d'% (x,y))
                self.points[2,:]=(x,y)
            else:
                self.ui.lineEdit_4.setText(' %d,%d'% (x,y))
                self.points[3,:]=(x,y)

def rotate(self):
    if self.imgCache.size == 1:
        return
    self.imgLast=self.imgCache.copy()
    h, w = self.imgCache.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), -90, 1)
    angle =  -np.pi / 2
    w_ = int(w * abs(np.cos(angle)) + h * abs(np.sin(angle)) + 0.5)
    h_ = int(w * abs(np.sin(angle)) + h * abs(np.cos(angle)) + 0.5)
    M[0, 2] += (w_ - w) / 2
    M[1, 2] += (h_ - h) / 2
    self.imgCache = cv2.warpAffine(self.imgCache, M, (w_, h_))
    self.imgTrans = self.imgCache.copy()
    refreshShow(self, self.imgCache)

def trans(self):
    if self.imgCache.size == 1:
        return
    self.imgLast=self.imgCache.copy()
    if np.sum(self.points[3,:])>0:
        self.imgCache = four_point_transform(self.imgShow, self.points)
        self.imgTrans = self.imgCache.copy()
        refreshShow(self, self.imgCache)
        # clear(self)
    else:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '单击四点标定方形区域  ')
        msg_box.exec_()

def clear(self):
    self.points=np.zeros((4,2),np.float32)
    self.ui.lineEdit.setText('')
    self.ui.lineEdit_2.setText('')
    self.ui.lineEdit_3.setText('')
    self.ui.lineEdit_4.setText('')

def detect(self):
    if self.imgCache.size == 1:
        return
    self.imgLast=self.imgCache.copy()
    try:
        self.imgCache=transform(self.imgCache)
        self.imgTrans = self.imgCache.copy()
        refreshShow(self, self.imgCache)
    except:
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '提取边界出错  ')
        msg_box.exec_()


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
                cache = movethreshold(cache,n=5,b=0.88)
            elif btn==25:
                cache = binopen(cache,ks=3)
            elif btn==27:
                cache = binclose(cache,ks=3)
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
                cache = hat_demo(cache,ks=50)
            elif btn==18:
                cache = unevenLightCompensate(cache, blockSize=16)
            elif btn == 19:
                cache = gauss_division(cache)
            elif btn == 20:
                # k = self.ui.spinBox_2.value()
                cache = USM(cache,0.4)
            elif btn == 21:
                cache = sharpening(cache)
            elif btn == 22:
                cache = streching(cache)
            elif btn == 23:
                cache = singalCLAHE(cache)
            elif btn == 24:
                cache = grayopen(cache,ks=3)
            elif btn == 28:
                cache = grayclose(cache,ks=3)
            elif btn == 30:
                cache = cv2.medianBlur(cache,3)
            elif btn == 33:
                cache = streching2(cache)
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
                cache = USM(cache,0.4)
            elif btn == 29:
                cache = dilate(cache)
                cache = erode(cache)
            elif btn == 31:
                cache = cv2.medianBlur(cache, 3)
            elif btn == 32:
                cache = streching2(cache)
            self.imgCache[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw), :] = cache
    # self.img=gauss_division(self.img)
    refreshShow(self, self.imgCache)


def refreshShow(self,img):
    self.imgShow = img
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
    img = cv2.warpAffine(img, M, (w_, h_))
    self.imgShow = img
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
    fileName, tmp = QFileDialog.getOpenFileName(self, '打开图像', 'Image', '*.png *.jpg *.bmp *.jpeg')
    print(fileName)
    if fileName is '':
        return
    root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
    pwd = os.getcwd()  # 返回当前工作目录
    if root_dir:
        os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
    # self.img = cv2.imread(file_name)
    self.imgCache = cv2.imread(file_name, -1)
    os.chdir(pwd)
    # cv2.imshow('pic', self.img)
    if self.imgCache.size <= 1:
        return
    self.fname=file_name.split('.')[0]
    # self.h, self.w = self.img.shape[:2]
    if len(self.imgCache.shape) == 3:
        if self.imgCache.shape[2] == 4:
            self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGRA2BGR)
    self.imgOgl = self.imgCache.copy()
    self.imgLast = self.imgCache.copy()
    self.imgTrans=np.ndarray(())
    clear(self)
    print(self.imgCache.shape)
    refreshShow(self,self.imgCache)

def choosemulti(self):
    fileName, tmp = QFileDialog.getOpenFileNames(self, '打开图像', '', '*.png *.jpg *.bmp')
    # print(fileName, tmp)
    if len(fileName) ==0:
        return
    self.nfiles=len(fileName)
    # print(tmp)
    for i in range(self.nfiles):
        root_dir, file_name = os.path.split(fileName[i])  # 按照路径将文件名和路径分割开
        # print(tmp[i])
        pwd = os.getcwd()  # 返回当前工作目录
        if root_dir:
            os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
        # self.img = cv2.imread(file_name)
        self.imgMulti.append(cv2.imread(file_name, -1))
        # self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGR2RGB)
        os.chdir(pwd)
        if self.imgMulti[i].size == 1:
            return
        cv2.imshow('pics', self.imgMulti[i])
        cv2.waitKey()
        # self.fname=file_name.split('.')[0]
        # self.imgOgl = self.imgCache.copy()
        # self.h, self.w = self.img.shape[:2]
        # if self.imgCache.shape[2] == 4:
        #     self.imgCache = cv2.cvtColor(self.imgCache, cv2.COLOR_BGRA2BGR)
        # print(self.imgCache.shape)
    # refreshShow(self,self.imgCache)
    cv2.destroyAllWindows()
    msg_box = QMessageBox(QMessageBox.Warning, '提示', '暂不支持批处理！  ')
    msg_box.exec_()

def compare(self):
    if self.Ogl==0:
        self.Ogl=1
        if self.imgTrans.size > 1:
            refreshShow2(self, self.imgTrans)
        else:
            refreshShow2(self, self.imgOgl)
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
        if len(img.shape) == 3:
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
    data = cv2.warpAffine(img, M, (w_, h_))
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
        cv2.destroyAllWindows()
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
        fileName, tmp = QFileDialog.getSaveFileName(self, '保存图像', str(self.fname)+'_fin', '*.png *.jpg *.bmp')
        if fileName is '':
            return
        print(fileName)
        root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
        pwd = os.getcwd()  # 返回当前工作目录
        if root_dir:
            os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
        cv2.imwrite(file_name, self.imgCache)
        os.chdir(pwd)
    # else:
    #     msg_box = QMessageBox(QMessageBox.Warning, '提示', '图像为空，无法保存  ')
    #     msg_box.exec_()

def reset(self):
    self.ui.spinBox.setValue(1)
    if self.imgOgl.size>1:
        self.imgCache = self.imgOgl.copy()
        self.imgTrans=np.ndarray(())
        refreshShow(self, self.imgCache)
        # self.points=np.zeros((4,2),np.float32)
    # else:
    #     msg_box = QMessageBox(QMessageBox.Warning, '提示', '请选择图像  ')
    #     msg_box.exec_()

