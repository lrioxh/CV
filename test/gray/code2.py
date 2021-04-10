import cv2
import numpy as np

def bottomhat(img):
    """用的椭圆kernel"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)
    #给处理后的图像增加100亮度
    cimage = np.array(img.shape,np.uint8)
    cimage = 100
    blackhat = cv2.add(blackhat, cimage)

    cv2.imwrite('bothat/1e65.jpg',blackhat)
    return blackhat

def tophat(img):
    """用的椭圆kernel"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)

    cimage = np.array(img.shape,np.uint8)
    cimage = 100
    tophat = cv2.add(tophat, cimage)

    cv2.imwrite('tophat/1e65.jpg',tophat)
    return tophat

src = cv2.imread("imgs/e65.jpg",0)  #读取灰度图
cv2.imshow("input image",src)

bothat=bottomhat(src)
# cv2.imshow('bot',bothat)

tophat1=tophat(src)
# cv2.imshow('top',tophat1)
cv2.waitKey(0)




def hat_demo(image):
    gray=image
    """用矩形kernel"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    top_dst = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    black_dst = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    """给dst图像添加100亮度"""
    cimage = np.array(gray.shape,np.uint8)
    cimage = 100
    top_dst = cv2.add(top_dst, cimage)
    black_dst = cv2.add(black_dst, cimage)
    cv2.imwrite('tophat/2e65.jpg',top_dst)
    cv2.imwrite('bothat/2e65.jpg',black_dst)
    # cv2.imshow("top_hat", top_dst)
    # cv2.imshow("black_hat", black_dst)
    # cv2.waitKey(0)


def hat_gray_demo(image):  #把原图变成二值图像再进行顶帽和底帽变换
    gray = image
    """用矩形kernel"""
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    top_dst = cv2.morphologyEx(binary, cv2.MORPH_TOPHAT, kernel)
    black_dst = cv2.morphologyEx(binary, cv2.MORPH_BLACKHAT, kernel)
    cv2.imwrite('tophat/bine65.jpg',top_dst)
    cv2.imwrite('bothat/bine65.jpg',black_dst)
    # cv2.imshow("binary_top_hat", top_dst)
    # cv2.imshow("binary_black_hat", black_dst)


def gradient_demo(image):
    gray = image
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    basic_dst = cv2.morphologyEx(binary, cv2.MORPH_GRADIENT, kernel)
    cv2.imshow("gradient", basic_dst)

    dm = cv2.dilate(image, kernel)
    em = cv2.erode(image, kernel)

    internal_dst = cv2.subtract(image, em)  # internal gradient
    external_dst = cv2.subtract(dm, image)  # external gradient
#给图像加100亮度
    cimage = np.array(gray.shape,np.uint8)
    cimage = 100
    internal_dst = cv2.add(internal_dst, cimage)
    external_dst = cv2.add(external_dst, cimage)

    cv2.imwrite('int_grae65.jpg',internal_dst)
    cv2.imwrite('ext_grae65.jpg',external_dst)
    # cv2.imshow("internal_gradient", internal_dst)
    # cv2.imshow("external_gradient", external_dst)

hat_demo(src)
hat_gray_demo(src)
gradient_demo(src)
