import cv2
import numpy as np
import copy
import os
#平滑光照不均的函数
def unevenLightCompensate(img, blockSize):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
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

def fanbianhuan(img):
    rows=img.shape[0]
    cols=img.shape[1]
    cover=copy.deepcopy(img)
    for i in range(rows):
        for j in range(cols):
            cover[i][j]=255-cover[i][j]
    return cover

def hat_demo(image):
    gray=image
    """用矩形kernel"""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    top_dst = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
    black_dst = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    """给dst图像添加100亮度"""
    # cimage = np.array(gray.shape,np.uint8)
    # cimage = 100
    # top_dst = cv2.add(top_dst, cimage)
    # black_dst = cv2.add(black_dst, cimage)
    return top_dst,black_dst

# if __name__ == '__main__':
#     file = 'imgs/e69.jpg'
#     blockSize = 16
#     img = cv2.imread(file)
#     dst = unevenLightCompensate(img, blockSize)
#     fan=fanbianhuan(dst)
#     cv2.imwrite('qgze69.jpg',dst)
#     cv2.imwrite('fanqgze69.jpg',fan)
#     img1 = cv2.imread('qgze69.jpg',0)
#     top_dst,black_dst=hat_demo(img1)
#     cv2.imwrite('tophat/qgz' + 'e69' + '.jpg', top_dst)
#     cv2.imwrite('bothat/qgz' + 'e69' + '.jpg', black_dst)
#     fan1=fanbianhuan(black_dst)
#     fan2=fanbianhuan(top_dst)
#     cv2.imwrite('botfan/qgz'+'e69'+'.jpg',fan1)
#     cv2.imwrite('topfan/qgz'+'e69'+'.jpg',fan2)
#     # result = np.concatenate([img, dst], axis=1)
#     # cv2.imwrite('quguangzhaoe65.jpg',result)
#     # cv2.imshow('result', result)
#     # cv2.waitKey(0)
#
for file in os.listdir('imgs'):
    blockSize = 16
    img=cv2.imread(os.path.join('imgs',file))
    dst = unevenLightCompensate(img, blockSize)
    name = os.path.splitext(file)[0]
    cv2.imwrite('qgz/'+name+'.jpg',dst)

# for file in os.listdir('qgz'):
#     img1 = cv2.imread(os.path.join('qgz',file), 0)
#     top_dst, black_dst = hat_demo(img1)
#     name = os.path.splitext(file)[0]
#     cv2.imwrite('tophat/qgz'+name+'.jpg', top_dst)
#     cv2.imwrite('bothat/qgz'+name+'.jpg', black_dst)
#     fan1 = fanbianhuan(black_dst)
#     # fan2 = fanbianhuan(top_dst)
#     cv2.imwrite('botfan/qgz' + name + '.jpg', fan1)
    # cv2.imwrite('topfan/qgz' + name + '.jpg', fan2)