import cv2
import numpy as np
import os
import copy
def file_name(file_dir):
  for root, dirs, files in os.walk(file_dir):
    print(root) #当前目录路径
    print(dirs) #当前路径下所有子目录
    print(files) #当前路径下所有非目录子文件

file_name('imgs')

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
    return top_dst,black_dst

for file in os.listdir('imgs'):
    img=cv2.imread(os.path.join('imgs',file),0)
    top_dst,black_dst=hat_demo(img)
    name=os.path.splitext(file)[0]
    cv2.imwrite('tophat/2'+name+'.jpg', top_dst)
    cv2.imwrite('bothat/2'+name+'.jpg', black_dst)

def fanbianhuan(img):
    rows=img.shape[0]
    cols=img.shape[1]
    cover=copy.deepcopy(img)
    for i in range(rows):
        for j in range(cols):
            cover[i][j]=255-cover[i][j]
    return cover

for file in os.listdir('bothat'):
    img=cv2.imread(os.path.join('bothat',file),0)
    cover=fanbianhuan(img)
    name=os.path.splitext(file)[0]
    cv2.imwrite('botfan/'+name+'.jpg', cover)