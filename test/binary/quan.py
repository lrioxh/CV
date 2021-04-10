import cv2
import numpy as np
from MyImage import Gradient

def seperate_otsu(img,block=(2,2)):
    unit_height = int(img.shape[0]/block[0])
    unit_width = int(img.shape[1]/block[1])
    new_img = None
    new_img_flag = 0
    for i in range(block[0]):
        if i != block[0] - 1:
            img_block_origin = img[i * unit_height:(i + 1) * unit_height, :]
        else:
            img_block_origin = img[i * unit_height:, :]
        img_block_rows = None
        rows_flag = 0
        for j in range(block[1]):
            img_block = img_block_origin.copy()
            if j != block[1]-1:
                img_block = img_block[:,j*unit_width:(j+1)*unit_width]
            else:
                img_block = img_block[:,j*unit_width:]
            # print(img_block.shape)
            _,new_img_block = cv2.threshold(img_block,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            if rows_flag == 0:
                img_block_rows = new_img_block
                rows_flag = 1
            else:
                # print(img_block_rows.shape)
                # print(new_img_block)
                # print(new_img_block.shape)
                img_block_rows = np.concatenate((img_block_rows,new_img_block), axis=1)
        if new_img_flag == 0:
            new_img = img_block_rows
            new_img_flag = 1
        else:
            new_img = np.concatenate((new_img,img_block_rows),axis=0)
    return new_img

def movingThreshold(img,n=20,b=0.5):
    new_img = img.copy()
    temp = np.zeros(img.shape[0]*img.shape[1])
    print(temp.shape)
    for y in range(0,img.shape[0]):
        for x in range(0,img.shape[1]):
            if y%2 == 0:
                temp[y*img.shape[1]+x] = img[y,x]
            else:
                # print(y*img.shape[0]+x)
                temp[y*img.shape[1]+x] = img[y,img.shape[1]-1-x]
    m_pre = 0
    for y in range(0,img.shape[0]):
        for x in range(0,img.shape[1]):
            index = y*img.shape[1]+x
            if index<n:
                dif = temp[index]
            else:
                dif = temp[index] - temp[index-n]
            dif *=1/n
            m_now = m_pre + dif
            m_pre = m_now
            if img[y,x] >b*m_now:
                new_img[y,x] = 255
            else:
                new_img[y,x] = 0
    new_img = np.uint8(new_img)
    return new_img





my_img = Gradient('./扫描全能王/wenzi2.jpg')
power_img = my_img.img_power_transform(1,1.9) # 做幂次变换，增强对比度

ret,new_img = cv2.threshold(my_img.img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
ret2,new_img2 = cv2.threshold(power_img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
new_img3 = seperate_otsu(power_img) # 这个是最好的（把图像分层）
new_img4 = movingThreshold(my_img.img,n=10,b=0.5)


cv2.imshow('img',my_img.img)
cv2.imshow('img2',power_img)
cv2.waitKey()
cv2.imshow('img',new_img)
cv2.imshow('img2',new_img2)
cv2.imshow('img3',new_img3)
cv2.imshow('img4',new_img4)
cv2.waitKey()


