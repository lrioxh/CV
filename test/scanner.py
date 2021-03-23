
from scipy.ndimage import gaussian_filter
import cv2
import numpy as np
from PIL import Image, ImageEnhance

# def gaussian_filter(image, sigma=101):
#     h,w=image.shape[:2]
#     padding = cv2.copyMakeBorder(image, 0, h, 0, w, cv2.BORDER_CONSTANT, value=0)
#     # dft = cv2.dft(np.float32(padding), flags=cv2.DFT_COMPLEX_OUTPUT)
#     dft = np.fft.fft2(padding)
#     dft = np.fft.fftshift(dft)
#     # magnitude_spectrum = np.log(np.abs(dft) + 1)
#     # normalize = (magnitude_spectrum - 2) / (np.max(magnitude_spectrum - 2))
#     # magnitude_spectrum_uint8 = np.uint8(255 * (np.power(normalize, 2)))
#     # cv2.imshow(" ", magnitude_spectrum_uint8)
#     # cv2.waitKey()
#     # cv2.destroyAllWindows()
#     for i in range(h*2):
#         for j in range(w*2):
#             dft[i, j,:] *= np.exp(-((i - h) ** 2 + (j - w) ** 2) / 2 / sigma ** 2)
#
#     dft = np.fft.ifftshift(dft)
#     idft = np.fft.ifft2(dft)
#
#     idft = np.abs(idft)
#     max = np.max(idft)
#     min = np.min(idft)
#
#     res = np.zeros((h, w, 3), dtype="uint8")
#
#     for i in range(h):
#         for j in range(w):
#             res[i,j,:] = 255 * (idft[i,j,:] - min) / (max - min)
#     return res[:h,:w]


def gauss_division(image):
    '''高斯滤波，图像除法
    image cv2'''
    src1 = image.astype(np.float32)
    gauss = cv2.GaussianBlur(image, ksize=(101,101),sigmaX=0)
    print(gauss.shape)
    cv2.imshow(" ", gauss)
    cv2.waitKey()
    cv2.destroyAllWindows()
    gauss1 = gauss.astype(np.float32)
    src1=(src1 / gauss1) * 255
    src1[src1 > 255] = 255
    dst1 = np.uint8(src1)
    return dst1

def image_enhancement(image):
    '''图像增强，增强对比度和亮度
    image PIL'''
    # 对比度增强
    enh_con = ImageEnhance.Contrast(image)
    # contrast = 5
    image_contrasted = enh_con.enhance(10)
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(image_contrasted)
    image_contrasted1 = cv2.cvtColor(np.asarray(image_contrasted), cv2.COLOR_RGB2BGR)  # PIL转cv2
    clear = image_contrasted1.mean()
    # print(clear)
    brightness = max(round(clear / 2000, 1), 1)
    # print(brightness)
    image_brightened = enh_bri.enhance(brightness)
    return image_brightened

img=cv2.imread('../images/HM$(}RMJND)]%JS~PYV7%]P.jpg')
cv2.imshow(" ", img)
cv2.waitKey()
cv2.destroyAllWindows()
step1=gauss_division(img)
cv2.imshow(" ", step1)
cv2.waitKey()
cv2.destroyAllWindows()
image = Image.fromarray(cv2.cvtColor(step1,cv2.COLOR_BGR2RGB))
step2=image_enhancement(image)
step2 = cv2.cvtColor(np.asarray(step2), cv2.COLOR_RGB2BGR)
cv2.imshow(" ", step2)
cv2.waitKey()
cv2.destroyAllWindows()
# conp = np.hstack((step1,step2))
# cv2.imshow("comparison", conp)
# cv2.waitKey()
# cv2.destroyAllWindows()