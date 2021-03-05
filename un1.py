import cv2 as cv
import numpy as np
# 读图片
img = cv.imread('D:/file/class/cv/code/photo/202131000.png')

# print(img.shape)
rows,cols, channels = img.shape
# 平移矩阵M：[[1,0,x],[0,1,y]]
M = np.float32([[1,0,20.2],[0,1,100.5]])
translate = cv.warpAffine(img,M,(cols,rows))

a=120
M = cv.getRotationMatrix2D((cols/2,rows/2),a,1)
angle=a*np.pi/180
w=round(cols*abs(np.cos(angle))+rows*abs(np.sin(angle))+0.5)
h=round(cols*abs(np.sin(angle))+rows*abs(np.cos(angle))+0.5)
M[0,2]+=(w - cols) / 2
M[1,2]+= (h - rows) / 2
rotate = cv.warpAffine(img,M,(w,h))

img_scale = cv.resize(img, (500, 500))

# def scale_rate(img,r):
img_scale_rate = cv.resize(img, (0, 0), fx=1.5, fy=1.5,
                              interpolation=cv.INTER_NEAREST)


# cv.imwrite('photo/202131000_scale.png', img_scale)
# cv.imwrite('photo/202131000_rate.png', img_scale_rate)
# cv.imwrite('photo/202131000_.png', rotate)


def get_rgb(event, x, y,a,b):
    if event==cv.EVENT_LBUTTONDOWN:
        print(img[y, x])


cv.imshow('pic', img_scale)
cv.setMouseCallback("pic", get_rgb)
cv.waitKey(0)