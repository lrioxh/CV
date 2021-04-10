import cv2
import matplotlib.pyplot as plt
import numpy as np
import copy
from math import sqrt,pow
import os
import math
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)

class ImageProcess():
    def __init__(self,fileName,type='gray'):
        root_dir, file_name = os.path.split(fileName)  # 按照路径将文件名和路径分割开
        pwd = os.getcwd()  # 返回当前工作目录
        if root_dir:
            os.chdir(root_dir)  # 改变当前工作目录到指定的路径。
        self.img = cv2.imread(file_name)
        os.chdir(pwd)
        if type == 'gray':
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
            self.img_height, self.img_width = self.img.shape
            self.bytesPerLine = self.img_width
        elif type == 'rgb':
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.img_height, self.img_width, self.img_channel = self.img.shape
            self.bytesPerLine = self.img_channel * self.img_width

    def show(self):
        cv2.imshow('img',self.img)
        cv2.waitKey()

    def img_power_transform(self,c,gamma):
        new_img = self.img.copy()
        new_img = c*np.power(new_img,gamma)
        new_img = (new_img-np.min(new_img)*np.ones(new_img.shape))/(np.max(new_img)-np.min(new_img))
        new_img = 255*new_img
        new_img = np.where(new_img>255,255,new_img)
        new_img = new_img.astype(np.uint8)
        return new_img

    def cal_mean(self,hist):
        m = 0
        for i in range(len(hist)):
            m += i*hist[i]
        return m

    def cal_var(self,hist):
        v = 0
        m = self.cal_mean(hist)
        for i in range(len(hist)):
            v += ((i-m)**2)*hist[i]
        return v

    # 全局直方图
    def global_hist(self,img=None):
        if type(img)==type(None):
            hist = cv2.calcHist([self.img], [0], None, [256], [0, 256])
            hist = hist / (self.img_height * self.img_width)
            self.global_hist_mean = self.cal_mean(hist)
            self.global_hist_var = self.cal_var(hist)
            return hist
        else:
            hist = cv2.calcHist([img], [0], None, [256], [0, 256])
            hist = hist / (img.shape[0]*img.shape[1])
            return hist

    # 画图
    def plot_hist(self,hist,name):
        self.F = MyFigure(width=5,height=2,dpi=100)
        r = [i for i in range(len(hist))]
        self.F.fig.suptitle(name)
        self.F.axes.plot(r,hist)

    def local_enhancement(self,E,k0,k1,k2,scale=(3,3)):
        new_img = copy.deepcopy(self.img)
        g_hist = self.global_hist()
        g_mean = self.cal_mean(g_hist)
        g_var = self.cal_var(g_hist)
        g_std = math.sqrt(g_var)
        for i in range(self.img_height):
            # 判定是否为边界
            height_start = i-int((scale[0]-1)/2)
            height_end = i+int((scale[0]-1)/2)
            if height_start < 0:
                height_start = 0
            if height_end > self.img_height-int((scale[0]-1)/2):
                height_end = self.img_height-int((scale[0]-1)/2)
            for j in range(self.img_width):
                width_start = j-int((scale[1]-1)/2)
                width_end = j+int((scale[1]-1)/2)
                if width_start < 0:
                    width_start = 0
                if width_end > self.img_width-int((scale[1]-1)/2):
                    width_end = self.img_width-int((scale[1]-1)/2)
                local_img = self.img[height_start:height_end+1,width_start:width_end+1]
                mean = np.mean(local_img)
                # var = np
                # local_hist = self.local_hist(local_img)
                # mean = self.cal_mean(local_hist)
                # var = self.cal_var(local_hist)
                # std = math.sqrt(var)
                std = np.std(local_img)
                if mean <= k0*g_mean and std>= k1*g_std and std <= k2*g_std:
                    new_img[i,j] = E*self.img[i,j]
        return new_img


    def fft(self):
        img_fft = cv2.dft(np.float32(self.img),flags=cv2.DFT_COMPLEX_OUTPUT)

        # 中心化
        central = np.fft.fftshift(img_fft)
        magnitude_spectrum = 20*np.log(cv2.magnitude(central[:, :, 0], central[:, :, 1]))
        magnitude_spectrum = np.array(magnitude_spectrum)

        self.magnitude_spectrum = magnitude_spectrum
        self.dshift = central
        return magnitude_spectrum


    def onmouse(self,event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print(x, y)

    def bandstop(self,D0,n,pair_list= [(44,56), (85,55), (166,57), (203,58)]):
        self.fft()
        new_dshift = self.dshift
        mid_row = self.img_height/2
        mid_col = self.img_width/2
        for i in range(self.img_height):
            for j in range(self.img_width):
                h = 1
                for location in pair_list:
                    # 距离
                    Dk = sqrt(pow(i-location[0],2)+pow(j-location[1],2))
                    sym_i = -(i - mid_row)+mid_row
                    sym_j = -(j-mid_col)+mid_col
                    Dminusk = sqrt(pow(sym_i-location[0],2)+pow(sym_j-location[1],2))
                    if Dk ==0:
                        a1 = 0.0000001
                    else:
                        a1 = 1/(1+pow(D0/Dk,2*n))
                    if Dminusk ==0:
                        a2 = 0.0000001
                    else:
                        a2 = 1 / (1 + pow(D0 / Dminusk, 2 * n))
                    h = h*a1*a2
                new_dshift[i,j,0] = new_dshift[i,j,0]*h
                new_dshift[i,j,1] = new_dshift[i,j,1]*h
        magnitude_spectrum = 20 * np.log(cv2.magnitude(new_dshift[:, :, 0], new_dshift[:, :, 1]))
        magnitude_spectrum = np.array(magnitude_spectrum)
        # cv2.imshow('img',magnitude_spectrum/255)
        # cv2.waitKey()
        ishift = np.fft.ifftshift(new_dshift)
        image_filtering = cv2.idft(ishift)
        image_filtering = cv2.magnitude(image_filtering[:, :, 0], image_filtering[:, :, 1])
        # 对逆变换结果进行归一化（一般对图像处理的最后一步都要进行归一化，特殊情况除外）
        cv2.normalize(image_filtering, image_filtering, 0, 1, cv2.NORM_MINMAX)
        # cv2.imshow('img',image_filtering)
        # cv2.waitKey()
        return magnitude_spectrum,image_filtering

    def narrow_stop(self,width=2):
        self.fft()
        print(self.dshift.shape)
        H = np.ones(self.dshift.shape)
        if width%2 != 0:
            print("error!")
            return None
        width_start = int(self.img_width/2 - width/2 - 1)
        width_end = int(self.img_width/2 + width/2)
        H[:,width_start:width_end,:] = 0.0000001
        H[328:345, width_start:width_end, :] = 1
        new_dshift = self.dshift*H

        magnitude_spectrum = 20 * np.log(cv2.magnitude(new_dshift[:, :, 0], new_dshift[:, :, 1]))
        magnitude_spectrum = np.array(magnitude_spectrum)

        ishift = np.fft.ifftshift(new_dshift)
        image_filtering = cv2.idft(ishift)
        image_filtering = cv2.magnitude(image_filtering[:, :, 0], image_filtering[:, :, 1])
        # 对逆变换结果进行归一化（一般对图像处理的最后一步都要进行归一化，特殊情况除外）
        cv2.normalize(image_filtering, image_filtering, 0, 1, cv2.NORM_MINMAX)
        # cv2.imshow('img', image_filtering)
        # cv2.waitKey()
        return magnitude_spectrum,image_filtering

class RegionGrowing(ImageProcess):
    def setSeed(self,seed):
        if type(seed) != int:
            return TypeError("Seed必须是整数值！")
        if 0>seed or seed>255:
            return ValueError("Seed必须在0~255之间！")
        Q = np.where(self.img>=seed,1,0)
        Q = Q.astype(np.uint8)
        # 种子图片
        cv2.imshow("img",255*Q)
        cv2.waitKey()
        return Q
        # cv2.imwrite("seed.png",255*Q)

    def grow(self,Q,maxInter=64):
        # 确定边缘以及颜色最小值&最大值
        max_gray = np.max(self.img * Q)
        min_gray = 255
        Q_edges = []
        for i in range(1, Q.shape[0] - 1):
            for j in range(1, Q.shape[1] - 1):
                if Q[i, j] == 0:
                    continue
                if np.sum(Q[i - 1:i + 2, j - 1:j + 2]) != 9:
                    Q_edges.append((i, j))
                if self.img[i, j] < min_gray:
                    min_gray = self.img[i, j]

        # 生长

        end_flag = 0
        while (end_flag == 0):
            # 在边缘找符合条件的点生长
            end_flag = 1
            new_Q_edges = copy.deepcopy(Q_edges)
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
                    if abs(min_gray - int(self.img[location[0], location[1]])) <= maxInter or abs(
                            int(self.img[location[0], location[1]]) - max_gray) <= maxInter:
                        Q[location[0], location[1]] = 1
                        new_Q_edges.append(location)
                        # 更新最小最大灰度值
                        # if self.img[location[0],location[1]] < min_gray:
                        #     min_gray = self.img[location[0],location[1]]
                        # if self.img[location[0],location[1]] > max_gray:
                        #     max_gray = self.img[location[0],location[1]]
                        end_flag = 0
                if np.sum(Q[i - 1:i + 2, j - 1:j + 2]) == 9:
                    new_Q_edges.remove((i, j))

            Q_edges = new_Q_edges
            if end_flag == 1:
                cv2.imshow("img", 255 * Q)
                cv2.waitKey()
                # cv2.imwrite("region_grow_q.png",255*Q)
            # if np.sum(Q) == 0:
            #     end_flag = 1

        new_img = copy.deepcopy(self.img)
        for i, j in Q_edges:
            new_img[i, j] = 0
        cv2.imshow("img", new_img)
        cv2.waitKey()

    def threshold_two(self,t1,t2,v1,v2,v3):
        inverse_img = 255 * np.ones(self.img.shape).astype(np.uint8) - self.img
        for i in range(inverse_img.shape[0]):
            for j in range(inverse_img.shape[1]):
                if inverse_img[i,j]<t1:
                    inverse_img[i,j] = v1
                elif self.img[i,j]>t2:
                    inverse_img[i,j] = v3
                else:
                    inverse_img[i,j] = v2
        return inverse_img

class Gradient(ImageProcess):
    def Sobel(self):
        ret = cv2.copyMakeBorder(self.img,1,1,1,1,cv2.BORDER_REFLECT) #padding
        ret = ret/255
        gradient = np.zeros((self.img_height,self.img_width,2))
        gx_filter = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
        gy_filter = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        for i in range(1,self.img_height+1):
            for j in range(1,self.img_width+1):
                gradient[i-1,j-1,0] = np.sum(gx_filter*ret[i-1:i+2,j-1:j+2])
                gradient[i-1,j-1,1] = np.sum(gy_filter*ret[i-1:i+2,j-1:j+2])
        gradient_angle = np.arctan(gradient[:,:,1]/(gradient[:,:,0]+0.000001*np.ones((self.img_height,self.img_width)))) #计算梯度角度
        gradient_magnitude = np.sqrt(np.power(gradient[:,:,0],2)+np.power(gradient[:,:,1],2))
        gradient_magnitude = (gradient_magnitude-np.min(gradient_magnitude)*gradient_magnitude)/(np.max(gradient_magnitude)-np.min(gradient_magnitude))
        self.gradient_magnitude = gradient_magnitude
        self.gradient_angle = gradient_angle
        return gradient_magnitude,gradient_angle

    @staticmethod
    def edgeConnect(gradient_magnitude,gradient_angle,method,A = np.pi / 2,Ta = np.pi / 4,k=25):
        Tm = 0.3*np.max(gradient_magnitude)
        g = np.zeros(gradient_magnitude.shape)
        for i in range(gradient_magnitude.shape[0]):
            for j in range(gradient_magnitude.shape[1]):
                angle = gradient_angle[i,j]
                if angle <0:
                    angle = angle + np.pi
                if method == "horizontal":
                    if gradient_magnitude[i,j] >Tm and (angle>A+Ta or angle< A-Ta):
                        g[i,j] = 1
                elif method == "vertical":
                    if gradient_magnitude[i,j] >Tm and angle<=A+Ta and angle>= A-Ta:
                        g[i,j] = 1
                else:
                    print("abaaba")
                    return ValueError("method不存在！")

        # 连接
        if method == "horizontal":
            for i in range(g.shape[0]):
                start_index = None
                start_flag = False
                switch_flag = True
                for j in range(g.shape[1]):
                    if start_flag == False:
                        if g[i,j] == 1:
                            start_flag = True
                    else:
                        if g[i,j] == 1:
                            flag = True
                        else:
                            flag = False
                        if switch_flag != flag:
                            if switch_flag == True:
                                start_index = j-1
                                switch_flag = False
                            else:
                                end_index = j
                                if end_index - start_index-1 <= k:
                                    g[i,start_index:end_index] = 1
                                switch_flag = True
        elif method == "vertical":
            for i in range(g.shape[1]):
                start_index = None
                start_flag = False
                switch_flag = True
                for j in range(g.shape[0]):
                    if start_flag == False:
                        if g[j,i] == 1:
                            start_flag = True
                    else:
                        if g[j,i] == 1:
                            flag = True
                        else:
                            flag = False
                        if switch_flag != flag:
                            if switch_flag == True:
                                start_index = j-1
                                switch_flag = False
                            else:
                                end_index = j
                                if end_index - start_index-1 <= k:
                                    g[start_index:end_index,i] = 1
                                switch_flag = True
        return g

    @staticmethod
    def refining(f):
        rows, cols = f.shape
        # 细化模板
        B1 = np.array([-1, -1, -1, 0, 1, 0, 1, 1, 1]).reshape(3, 3)
        B2 = np.array([0, -1, -1, 1, 1, -1, 1, 1, 0]).reshape(3, 3)
        B3 = np.array([1, 0, -1, 1, 1, -1, 1, 0, -1]).reshape(3, 3)
        B4 = np.array([1, 1, 0, 1, 1, -1, 0, -1, -1]).reshape(3, 3)
        B5 = np.array([1, 1, 1, 0, 1, 0, -1, -1, -1]).reshape(3, 3)
        B6 = np.array([0, 1, 1, -1, 1, 1, -1, -1, 0]).reshape(3, 3)
        B7 = np.array([-1, 0, 1, -1, 1, 1, -1, 0, 1]).reshape(3, 3)
        B8 = np.array([-1, -1, 0, -1, 1, 1, 0, 1, 1]).reshape(3, 3)
        maskList = [B1, B2, B3, B4, B5, B6, B7, B8]
        count = 0
        while True:
            temp = f.copy
            for m in maskList:
                mas = []
                for i in range(1, rows - 1):
                    for j in range(1, cols - 1):
                        if f[i, j] == 0:
                            continue
                        elif np.sum(m * f[i - 1:i + 2, j - 1:j + 2]) == 4:
                            # 击中时标记删除点
                            mas.append((i, j))
                for it in mas:
                    x, y = it
                    f[x, y] = 0
            if (temp == f).all:
                count += 1
            else:
                count = 0
            if count == 8:
                break
        return f

    def gradient_filter(self,rate):
        id = int(self.img.size*rate)
        th = np.sort(self.gradient_magnitude.reshape(1, -1))[0, id]
        gradient_magnitude = np.where(self.gradient_magnitude > th, self.img, 0)
        gradient_magnitude = gradient_magnitude.astype(np.uint8)
        return gradient_magnitude

    def Laplacian(self):
        gradient = cv2.Laplacian(self.img, cv2.CV_64F, ksize=3)
        gradient_magnitude = np.abs(gradient)
        self.gradient_magnitude = gradient_magnitude
        return gradient_magnitude

    def Otsu(self,img):
        if np.sum(img[img < 255]) == 0:# 先去除所有灰度值为0的点
            g = img.ravel()
        else:
            g = img[img > 0]
        max_sigma = 0
        threshold = 0
        g_group = []
        for i in range(0, 255):
            g1 = g[g <= i]
            g2 = g[g > i]
            if len(g1) > 0 and len(g2) > 0:
                mean1 = np.mean(g1)
                mean2 = np.mean(g2)
                p1 = len(g1) / len(g)
                sigma = p1 * (1 - p1) * (mean1 - mean2) ** 2
                g_group.append(sigma)
                if max_sigma < sigma:
                    max_sigma = sigma
                    threshold = i
            else:
                g_group.append(0)

        threshold = int(threshold + g_group.count(max_sigma) * 0.5)
        return threshold




def refining(f):
    rows, cols = f.shape
    # 细化模板
    B1 = np.array([-1, -1, -1, 0, 1, 0, 1, 1, 1]).reshape(3, 3)
    B2 = np.array([0, -1, -1, 1, 1, -1, 1, 1, 0]).reshape(3, 3)
    B3 = np.array([1, 0, -1, 1, 1, -1, 1, 0, -1]).reshape(3, 3)
    B4 = np.array([1, 1, 0, 1, 1, -1, 0, -1, -1]).reshape(3, 3)
    B5 = np.array([1, 1, 1, 0, 1, 0, -1, -1, -1]).reshape(3, 3)
    B6 = np.array([0, 1, 1, -1, 1, 1, -1, -1, 0]).reshape(3, 3)
    B7 = np.array([-1, 0, 1, -1, 1, 1, -1, 0, 1]).reshape(3, 3)
    B8 = np.array([-1, -1, 0, -1, 1, 1, 0, 1, 1]).reshape(3, 3)
    maskList = [B1, B2, B3, B4, B5, B6, B7, B8]
    count = 0
    while True:
        temp = f.copy
        for m in maskList:
            mas = []
            for i in range(1, rows - 1):
                for j in range(1, cols - 1):
                    if f[i, j] == 0:
                        continue
                    elif np.sum(m * f[i - 1:i + 2, j - 1:j + 2]) == 4:
                        # 击中时标记删除点
                        mas.append((i, j))
            for it in mas:
                x, y = it
                f[x, y] = 0
        if (temp == f).all:
            count += 1
        else:
            count = 0
        if count == 8:
            break
    return f

def H52(img):
    if np.sum(img[img < 255])==0:
        g = img.ravel()
    else:
        g = img[img > 0]
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
    return threshold

# if __name__ == '__main__':
#     project = Gradient('experiment5(2).tif')
#     project.show()
#     hist = project.global_hist()
#     plt.figure()
#     plt.plot(hist)
#     plt.show()
#     th = H52(project.img)
#     new_img = np.where(project.img>th,255,0)
#     new_img = new_img.astype(np.uint8)
#     cv2.imshow('img',new_img)
#     cv2.waitKey()
#     gradient = cv2.Laplacian(project.img, cv2.CV_64F, ksize=3)
#     gradient_magnitude = np.abs(gradient)
#     gradient_magnitude = np.where(gradient_magnitude>0.3*np.max(gradient_magnitude),project.img,0)
#     gradient_magnitude = gradient_magnitude.astype(np.uint8)
#     cv2.imshow('img',gradient_magnitude)
#     cv2.waitKey()
#     th2 = H52(gradient_magnitude)
#     new_img2 = np.where(project.img>th2,255,0)
#     new_img2 = new_img2.astype(np.uint8)
#     cv2.imshow('img',new_img2)
#     cv2.waitKey()

    # gradient_magnitude, gradient_angle = project.Sobel()
    # cv2.imshow('img',gradient_magnitude)
    # cv2.waitKey()
    # gradient_magnitude = np.where(gradient_magnitude>= 0.5*np.max(gradient_magnitude),1,0)
    # gradient_magnitude = gradient_magnitude.astype(np.uint8)
    # # cv2.imshow('img',255*gradient_magnitude)
    # # cv2.waitKey()
    # new_img = gradient_magnitude*project.img
    # new_img = new_img.astype(np.uint8)
    # cv2.imshow('img',new_img)
    # cv2.waitKey()
    #
    # th2 = H52(new_img)
    # new_img = np.where(project.img>th2,255,0)
    # new_img = new_img.astype(np.uint8)
    # cv2.imshow('img',new_img)
    # cv2.waitKey()