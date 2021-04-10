import cv2
import numpy as np


def gauss_division(image):
    src = image.astype(np.float32)
    gauss = cv2.GaussianBlur(image, ksize=(201,201),sigmaX=32)
    gauss = gauss.astype(np.float32)
    dst=(src / gauss)*250
    # src1=src1* 255/np.max(src1)
    dst[dst > 255] = 255
    dst = np.uint8(dst)
    return dst

def Saturation(img,k=1.8):
    '''
    饱和度，1.8为系数
    :param img:
    :return:
    '''
    fImg = np.float32(img / 255.0)
    hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
    # lsImg = np.zeros(img.shape, np.float32)
    hlsCopy = np.copy(hlsImg)
    hlsCopy[:, :, 2] = k * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1
    # HLS2BGR
    lsImg = np.uint8(cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)*255)
    return lsImg

def streching(img):
    '''
    像素值线性变换
    :param img:
    :return:
    '''
    # print(img.mean())
    # m=int(img.mean()/50+128)
    # a=int(img.mean()/50+80)
    # b=int(img.mean()/50+200)
    xp = [0, 64, 128, 196, 255]
    fp = [0, 16, 128, 240, 255]
    x = np.arange(256)
    table = np.interp(x, xp, fp).astype('uint8')
    # print(table)
    return cv2.LUT(img, table)

def hisEqulColor2(img):
    '''
    三通道自适应直方图，CLAHE
    :param img:
    :return:
    '''
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])

    ycrcb = cv2.merge(channels)
    img = cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR)
    return img

def sharpening(img):
    '''
    锐化，有4种核
    :param img:
    :return:
    '''
    # kernal3 = [
    #     [0, -0, -1, -0, 0],
    #     [-0, -1, -1, -1, -0],
    #     [-1, -1, 13, -1, -1],
    #     [-0, -1, -1, -1, -0],
    #     [0, -0, -1, -0, 0]
    # ]
    kernal1 = [[-0.1, -1, -0.1], [-1, 5.4, -1], [-0.1, -1, -0.1]]
    # kernal2 = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
    # kernal0 = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
    # if k==0:
    #     kernel = np.array(kernal0, np.float32)  # 锐化
    # elif k==1:
    kernel = np.array(kernal1, np.float32)
    # elif k==2:
    #     kernel = np.array(kernal2, np.float32)
    # elif k==3:
    #     kernel = np.array(kernal3, np.float32)
    dst = cv2.filter2D(img, -1, kernel=kernel)
    return dst

def USM(src,k):
    blur_img = cv2.GaussianBlur(src, (0, 0), 5)
    usm = cv2.addWeighted(src, 1.0+k, blur_img, -k, 0)
    return usm


#定义膨胀特征提取
def dilate(data):
    result = np.zeros(data.shape,np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    for i in range(data.shape[2]):
        dilate_data = cv2.dilate(data[:,:,i], kernel,iterations = 1)
        result[:,:,i] = dilate_data
    return result

#定义腐蚀特征提取
def erode(data):
    result = np.zeros(data.shape,np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    for i in range(data.shape[2]):
        erode_data = cv2.erode(data[:,:,i], kernel,iterations = 1)
        result[:,:,i] = erode_data
    return result


### 以下为Retinex算法
def singleScaleRetinex(img, sigma):
    retinex = np.log10(img) - np.log10(cv2.GaussianBlur(img, (201, 201), sigma))
    return retinex

def multiScaleRetinex(img, sigma_list):
    retinex = np.zeros_like(img)
    for sigma in sigma_list:
        retinex += singleScaleRetinex(img, sigma)
    retinex = retinex / len(sigma_list)
    return retinex

def colorRestoration(img, alpha, beta):
    img_sum = np.sum(img, axis=2, keepdims=True)
    color_restoration = beta * (np.log10(alpha * img) - np.log10(img_sum))
    return color_restoration

def simplestColorBalance(img, low_clip, high_clip):
    total = img.shape[0] * img.shape[1]
    for i in range(img.shape[2]):
        unique, counts = np.unique(img[:, :, i], return_counts=True)
        current = 0
        for u, c in zip(unique, counts):
            if float(current) / total < low_clip:
                low_val = u
            if float(current) / total < high_clip:
                high_val = u
            current += c
        img[:, :, i] = np.maximum(np.minimum(img[:, :, i], high_val), low_val)
    return img

def MSRCR(img, sigma_list=[64], G=5, b=25, alpha=125, beta=46, low_clip=0.01, high_clip=0.99):
    img = np.float64(img) + 1.0
    img_retinex = multiScaleRetinex(img, sigma_list)
    img_color = colorRestoration(img, alpha, beta)
    img_msrcr = G * (img_retinex * img_color + b)
    for i in range(img_msrcr.shape[2]):
        img_msrcr[:, :, i] = (img_msrcr[:, :, i] - np.min(img_msrcr[:, :, i])) / \
                             (np.max(img_msrcr[:, :, i]) - np.min(img_msrcr[:, :, i])) * \
                             255
    img_msrcr = np.uint8(np.minimum(np.maximum(img_msrcr, 0), 255))
    img_msrcr = simplestColorBalance(img_msrcr, low_clip, high_clip)
    return img_msrcr

