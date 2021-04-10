import cv2
import numpy as np


def unevenLightCompensate(gray, blockSize=16):
    '''
    平滑光照不均的函数
    :param img:
    :param blockSize:
    :return:
    '''
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    average = np.mean(gray)

    rows_new = int(np.ceil(gray.shape[0] / blockSize))
    cols_new = int(np.ceil(gray.shape[1] / blockSize))

    blockImage = np.zeros((rows_new, cols_new), dtype=np.float32)
    for r in range(rows_new):
        for c in range(cols_new):
            rowmin = r * blockSize
            rowmax = (r + 1) * blockSize
            if (rowmax > gray.shape[0]):
                rowmax = gray.shape[0]
            colmin = c * blockSize
            colmax = (c + 1) * blockSize
            if (colmax > gray.shape[1]):
                colmax = gray.shape[1]

            imageROI = gray[rowmin:rowmax, colmin:colmax]
            temaver = np.mean(imageROI)
            blockImage[r, c] = temaver

    blockImage = blockImage - average
    blockImage2 = cv2.resize(blockImage, (gray.shape[1], gray.shape[0]), interpolation=cv2.INTER_CUBIC)
    gray2 = gray.astype(np.float32)
    dst = gray2 - blockImage2
    dst = dst.astype(np.uint8)
    # dst = cv2.GaussianBlur(dst, (3, 3), 0)
    # dst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    return dst

def hat_demo(image,ks=5):
    # gray=image
    """底冒变换"""
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ks, ks))
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (ks, ks))
    # top_dst = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    black_dst = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
    """给dst图像添加100亮度"""
    # cimage = np.array(gray.shape,np.uint8)
    # cimage = 100
    # top_dst = cv2.add(top_dst, cimage)
    # black_dst = cv2.add(black_dst, cimage)
    black_dst=255-black_dst
    return black_dst

def singalCLAHE(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    return clahe.apply(img)

def grayopen(img,ks=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (ks, ks))
    res = cv2.erode(img, kernel,iterations=1)
    res = cv2.dilate(res, kernel,iterations=1)
    return res