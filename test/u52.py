import cv2
import numpy as np
import matplotlib.pyplot as plt
import pathlib
#解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

img = cv2.imread('../images/u52.tif', 0)

# 画全局直方图
def quanjuzft(img):
    imgravel=img.ravel()
    plt.hist(imgravel,256,[0,256])
    plt.title('原图全局直方图')
    plt.show()

quanjuzft(img)

#直接对原图进行Otsu阈值分割
def Otsu_origin(img):
    maxval = 255
    otsuThe1 = 0
    otsuThe1, dst_Otsu = cv2.threshold(img, otsuThe1, maxval, cv2.THRESH_OTSU)
    cv2.imshow('原图直接Otsu', dst_Otsu)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print('直接对原图进行Otsu阈值分割的阈值=',otsuThe1)
    return dst_Otsu,otsuThe1  #返回分割后的图像矩阵和阈值

dst_Otsu,otsuThe1=Otsu_origin(img)

# #sobel算子求梯度
# def sobel(img):
#     depth = cv2.CV_16S
#     # 求X方向梯度（创建grad_x, grad_y矩阵）
#     grad_x = cv2.Sobel(img, depth, 1, 0)
#     abs_grad_x = cv2.convertScaleAbs(grad_x)
#     # 求Y方向梯度
#     grad_y = cv2.Sobel(img, depth, 0, 1)
#     abs_grad_y = cv2.convertScaleAbs(grad_y)
#     # 合并梯度（近似）
#     edgeImg = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
#     cv2.imshow('sobel',edgeImg )
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     #画sobel算子梯度直方图
#     edgeImgravel=edgeImg.ravel()
#     plt.hist(edgeImgravel,256,[-50,206])
#     plt.title('sobel直方图')
#     plt.show()
#     return edgeImg

#拉普拉斯算子求梯度
def laplacian(img):
    #ksize是可变参数-算子一边的宽度 1表示拉普拉斯算子3*3，2表示算子5*5，3表示7*7
    gray_lap = cv2.Laplacian(img, cv2.CV_16S, ksize=3)
    print(len(gray_lap[gray_lap>0]))
    dst = np.abs(gray_lap)
    #显示拉普拉斯梯度图像
    cv2.imshow('laplacian', dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # 显示拉普拉斯梯度直方图
    imgravel2=dst.ravel()
    plt.hist(imgravel2, 256, [0, 256])
    plt.title('拉普拉斯直方图')
    plt.show()
    return dst,imgravel2 #返回梯度矩阵和矩阵拉平成一维的列表

dst,imgravel2=laplacian(img)

#对拉普拉斯梯度矩阵进行阈值处理得到0，1二值矩阵newGrad,再用二值矩阵和原图乘积得到新图片newimg
def yuzhi_laplacian(dst,imgravel2):
    global img
    maxT = max(imgravel2) #求梯度矩阵的最大值maxT
    print('maxT', maxT)
    thres = 0.4 * maxT   #这个0.4是可变阈值 这里取了最大值的40%
    # print('threshold', thres)
    newGrad = np.zeros(img.shape,dtype='uint8')
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if dst[i][j] > thres:
                newGrad[i][j] = 1
    newimg=newGrad*img
    plt.imshow(newimg,cmap='gray')
    plt.title('乘完之后图片newimg')
    plt.show()
    return newimg

newimg=yuzhi_laplacian(dst,imgravel2)

#画乘完之后的图片去掉0值像素点以外的直方图
def qu0zft(newimg):
    newimgDraw=newimg[newimg!=0]
    newimgDrawRavel=newimgDraw.ravel()
    # newimgravel=newimg.ravel()
    plt.hist(newimgDrawRavel,256,[0,256])
    plt.title('乘完之后直方图')
    plt.show()

qu0zft(newimg)

#Otsu求阈值的源码
def otsu(newimg, th=0):
    max_th = 0
    max_sigma = 0

    for _x in range(1, 255):

        # 公式元素准备
        v0 = newimg[np.where(newimg < _x)]
        v0 = v0[v0!=0]
        # print(v0.all())
        m0 = np.mean(v0) if len(v0) > 0 else 0.
        # w0 = len(v0)/(h * w)

        v1 = newimg[np.where(newimg > _x)]
        m1 = np.mean(v1) if len(v0) > 0 else 0.
        # w1 = len(v1)/(h * w)
        totalN=len(v0)+len(v1)
        p0=len(v0)/totalN
        p1=len(v1)/totalN
        # 计算类间方差
        # sigma = w0 * w1 * (m1 - m0)**2
        sigma = p0 * p1 * (m1 - m0) ** 2
        if sigma >= max_sigma:
            max_sigma = sigma
            max_th = _x

    newimgSigma = newimg[newimg != 0]
    sigma2Global=np.var(newimgSigma.ravel())
    print('原图总体方差',sigma2Global)
    print('阈值T= %d', max_th)
    print('类间方差= %d', max_sigma)
    print('可区分性度量eta=', max_sigma/sigma2Global)
        # 阈值分割
    th = max_th
    global img
    newimg[img < th] = 0
    newimg[img >= th] = 255

    return newimg

#
img1 = otsu(newimg)
cv2.imshow('otsu_method', img1);
cv2.waitKey(0)