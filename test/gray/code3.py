import cv2
import numpy as np
import copy
#对底帽变换产生的图像进行图像增强

img=cv2.imread('bothat/2e65.jpg',0)

#直接对原图取255-r反变换
def fanbianhuan(img):
    rows=img.shape[0]
    cols=img.shape[1]
    cover=copy.deepcopy(img)
    for i in range(rows):
        for j in range(cols):
            cover[i][j]=255-cover[i][j]
    return cover

cover=fanbianhuan(img)
cv2.imwrite('fane65.jpg',cover)

#对原图进行Otsu二值化
def Otsu(img):
    maxval = 255
    otsuThe = 0
    otsuThe, dst_Otsu = cv2.threshold(img, otsuThe, maxval, cv2.THRESH_OTSU)
    cv2.imwrite('DirectOtsu.jpg',dst_Otsu)
    fan1=fanbianhuan(dst_Otsu)
    cv2.imwrite('OtsuFan.jpg',fan1)
    # cv2.imshow('Otsu', dst_Otsu)
    # return dst_Otsu

Otsu(img)


def adaptiveThresh(img, winSize=(5,5), ratio=0.15):
    # 第一步:对图像矩阵进行均值平滑
    I_mean = cv2.boxFilter(img, cv2.CV_32FC1, winSize)

    # 第二步:原图像矩阵与平滑结果做差
    out = img - (1.0 - ratio) * I_mean

    # 第三步:当差值大于或等于0时，输出值为255；反之，输出值为0
    out[out >= 0] = 255
    out[out < 0] = 0
    out = out.astype(np.uint8)
    cv2.imwrite('adapThre.jpg',out)
    fan2=fanbianhuan(out)
    cv2.imwrite('adaThreFan.jpg',fan2)
    # return out

adaptiveThresh(img)