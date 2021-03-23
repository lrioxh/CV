import cv2
import numpy as np
from skimage import morphology

path = "../images/4Fig1027(a)(van_original).tif"
img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = img / 255.0 #像素值0-1之间
# cv2.imshow("g", gray)
# cv2.waitKey(0)
#sobel算子分别求出gx，gy
gx = np.abs(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3))
# print(gx)
gy = np.abs(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3))
mag, ang = cv2.cartToPolar(gx, gy, angleInDegrees=1) #得到梯度幅度和梯度角度阵列
# ang=np.arctan2(gy,gx)*180/3.1415926535
# print(mag,ang)
# cv2.imshow("g", gx )
# cv2.waitKey(0)

#行扫描，间隔k时，进行填充，填充值为1
def edge_connection(img, size, k):
    for i in range(size):
        Yi = np.where(img[i, :] > 0)
        if len(Yi[0]) >= 10: #可调整
            for j in range(0, len(Yi[0])-1):
                if Yi[0][j+1] - Yi[0][j] <= k:
                    img[i, Yi[0][j]:Yi[0][j+1]] = 1
    return img

#选取边缘，提取边缘坐标，将g中相应坐标像素值设为1
# X, Y = np.where((mag > np.max(mag) * 0.3)&((ang >= 45)&(ang <=135)))
# g[X, Y] = 1
# X, Y = np.where((gx > np.max(gx) * 0.3)&((ang >= -45)&(ang <=45)))
# g[X, Y] = 1
# cv2.imshow("g", g)
# cv2.waitKey(0)
X, Y = np.where((mag > np.max(mag) * 0.3)&((ang >= 45)&(ang <=135)))
g1 = np.zeros(gray.shape)
g1[X, Y] = 1
cv2.imshow("g", g1)
cv2.waitKey(0)
#边缘连接，此过程只涉及水平，垂直边缘连接，不同角度边缘只需旋转相应角度即可
g1 = edge_connection(g1, gray.shape[0], k=25)
cv2.imshow("g", g1)
cv2.waitKey(0)
# g = cv2.rotate(g, 0)
X, Y = np.where((mag > np.max(mag) * 0.3)&((ang >= -45)&(ang <=45)))
g2 = np.zeros(gray.shape)
g2[X, Y] = 1
g2 = cv2.rotate(g2, 0)
g2 = edge_connection(g2, gray.shape[1], k=25)
g2 = cv2.rotate(g2, 2)
#
# # cv2.imshow("img", img)
cv2.imshow("g", g2)
cv2.waitKey(0)

g=g1+g2
cv2.imshow("g", g)
cv2.waitKey(0)



def Three_element_add(array):
    array0 = array[:]
    array1 = np.append(array[1:],np.array([0]))
    array2 = np.append(array[2:],np.array([0, 0]))
    arr_sum = array0 + array1 + array2
    return arr_sum[:-2]


def VThin(image, array):
    NEXT = 1
    height, width = image.shape[:2]
    for i in range(1,height):
        M_all = Three_element_add(image[i])
        for j in range(1,width):
            if NEXT == 0:
                NEXT = 1
            else:
                M = M_all[j-1] if j<width-1 else 1
                if image[i, j] == 0 and M != 0:
                    a = np.zeros(9)
                    if height-1 > i and width-1 > j:
                        kernel = image[i - 1:i + 2, j - 1:j + 2]
                        a = np.where(kernel == 255, 1, 0)
                        a = a.reshape(1, -1)[0]
                    NUM = np.array([1,2,4,8,0,16,32,64,128])
                    sumArr = np.int(np.sum(a*NUM))
                    image[i, j] = \
                        array[sumArr] * 255
                    if array[sumArr] == 1:
                        NEXT = 0
    return image


def HThin(image, array):
    height, width = image.shape[:2]
    NEXT = 1
    for j in range(1,width):
        M_all = Three_element_add(image[:,j])
        for i in range(1,height):
            if NEXT == 0:
                NEXT = 1
            else:
                M = M_all[i-1] if i < height - 1 else 1
                if image[i, j] == 0 and M != 0:
                    a = np.zeros(9)
                    if height - 1 > i and width - 1 > j:
                        kernel = image[i - 1:i + 2, j - 1:j + 2]
                        a = np.where(kernel == 255, 1, 0)
                        a = a.reshape(1, -1)[0]
                    NUM = np.array([1, 2, 4, 8, 0, 16, 32, 64, 128])
                    sumArr = np.int(np.sum(a * NUM))
                    image[i, j] = array[sumArr] * 255
                    if array[sumArr] == 1:
                        NEXT = 0
    return image


def Xihua(binary, array, num=10):
    binary_image = binary.copy()
    image = cv2.copyMakeBorder(binary_image, 1, 0, 1, 0, cv2.BORDER_CONSTANT, value=0)
    for i in range(num):
        VThin(image, array)
        HThin(image, array)
    return image


array = [0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1,\
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1,\
         0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,\
         1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0,\
         1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0]

def thin(img):
    """
    细化函数，根据算法，运算出中心点的对应值
    :param img: 需要细化的图片（经过二值化处理的图片）
    :return:
    """
    h, w = img.shape
    i_thin = img.copy()
    for i in range(h):
        for j in range(w):
            if img[i, j] == 0:
                a = [1] * 9
                for k in range(3):
                    for l in range(3):
                        if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and i_thin[i - 1 + k, j - 1 + l] == 0:
                            a[k * 3 + l] = 0
                i_sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                i_thin[i, j] = array[i_sum] * 255

    return i_thin

def v_thin(img):
    """
    细化函数，根据算法，运算出中心点的对应值
    :param img: 需要细化的图片（经过二值化处理的图片）
    :param array: 映射矩阵array
    :return:
    """
    h, w = img.shape
    i_next = 1
    for i in range(h):
        for j in range(w):
            if i_next == 0:
                i_next = 1
            else:
                i_m = int(img[i, j - 1]) + int(img[i, j]) + int(img[i, j + 1]) if 0 < j < w - 1 else 1
                if img[i, j] == 0 and i_m != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and img[i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    i_sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    img[i, j] = array[i_sum] * 255
                    if array[i_sum] == 1:
                        i_next = 0


def h_thin(img):
    """
    细化函数，根据算法，运算出中心点的对应值
    :param img: 需要细化的图片（经过二值化处理的图片）
    :param array: 映射矩阵array
    :return:
    """
    h, w = img.shape
    i_next = 1
    for j in range(w):
        for i in range(h):
            if i_next == 0:
                i_next = 1
            else:
                i_m = int(img[i -1, j]) + int(img[i, j]) + int(img[i + 1, j]) if 0 < i < h - 1 else 1
                if img[i, j] == 0 and i_m != 0:
                    a = [0] * 9
                    for k in range(3):
                        for l in range(3):
                            if -1 < (i - 1 + k) < h and -1 < (j - 1 + l) < w and img[i - 1 + k, j - 1 + l] == 255:
                                a[k * 3 + l] = 1
                    i_sum = a[0] * 1 + a[1] * 2 + a[2] * 4 + a[3] * 8 + a[5] * 16 + a[6] * 32 + a[7] * 64 + a[8] * 128
                    img[i, j] = array[i_sum] * 255
                    if array[i_sum] == 1:
                        i_next = 0


def xi_hua(img, num=10):
    for i in range(num):
        v_thin(img)
        h_thin(img)

    return img

# print(1-g)
# g=np.uint(g)
g[g>1]=1
# print(np.max(g))
# skeleton =morphology.skeletonize(g)
iThin = thin(1-g)
print(np.max(1-iThin))
cv2.imshow('iThin', 1-iThin)
cv2.waitKey(0)
cv2.destroyAllWindows()
# skeleton=np.int(skeleton)
# skeleton[skeleton==True]=1
# skeleton[skeleton==False]=0
# print(skeleton.shape)
# cv2.imshow('iThin', skeleton.astype(np.float32))
# cv2.waitKey(0)
# cv2.destroyAllWindows()



