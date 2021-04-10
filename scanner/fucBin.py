import cv2
import numpy as np
from scipy.signal import lfilter

def img_power_transform(img, c, gamma):
    new_img = img.copy()
    new_img = c * np.power(new_img, gamma)
    new_img = (new_img - np.min(new_img) * np.ones(new_img.shape)) / (np.max(new_img) - np.min(new_img))
    new_img = 255 * new_img
    new_img = np.where(new_img > 255, 255, new_img)
    new_img = new_img.astype(np.uint8)
    return new_img

def seperate_otsu(img,block=(1,1)):
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
    # print(temp.shape)
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

def movingthreshold(f, n=20, k=0.5):
    shape = f.shape
    assert n >= 1
    assert 0 < k < 1
    f[1:-1:2, :] = np.fliplr(f[1:-1:2, :])
    f = f.flatten()
    maf = np.ones(n) / n
    res_filter = lfilter(maf, 1, f)
    g = np.array(f > k * res_filter).astype(int)
    g = g.reshape(shape)
    g[1:-1:2, :] = np.fliplr(g[1:-1:2, :])
    g = g * 255

    return g

def binopen(img,ks=3):
    ret, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (ks, ks))
    ret = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    return ret
