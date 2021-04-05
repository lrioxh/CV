
from scipy.ndimage import gaussian_filter
import cv2
import numpy as np
from PIL import Image, ImageEnhance

# 移动平均
# 暗底帽Bottom-hat
# 直方图均衡
def get_rgb(event, x, y,a,b):
    if event==cv2.EVENT_LBUTTONDOWN:
        print(img[y, x])

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
    gauss = cv2.GaussianBlur(image, ksize=(201,201),sigmaX=32)
    # print(gauss.shape)
    # cv2.imshow(" ", gauss)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    gauss1 = gauss.astype(np.float32)
    src1=(src1 / gauss1)*250
    # src1=src1* 255/np.max(src1)
    src1[src1 > 255] = 255
    dst1 = np.uint8(src1)
    return dst1

# def image_enhancement(image):
#     '''图像增强，增强对比度和亮度
#     image PIL'''
#     # 对比度增强
#     enh_con = ImageEnhance.Contrast(image)
#     # contrast = 5
#     image_contrasted = enh_con.enhance(10)
#     # 亮度增强
#     enh_bri = ImageEnhance.Brightness(image_contrasted)
#     image_contrasted1 = cv2.cvtColor(np.asarray(image_contrasted), cv2.COLOR_RGB2BGR)  # PIL转cv2
#     clear = image_contrasted1.mean()
#     # print(clear)
#     brightness = max(round(clear / 2000, 1), 1)
#     # print(brightness)
#     image_brightened = enh_bri.enhance(brightness)
#     return image_brightened

kernal3=[
    [0,   -0, -1,   -0,   0],
    [-0,-1,   -1, -1 , -0],
    [-1,  -1,  13,  -1,  -1],
    [-0,-1,   -1, -1,  -0],
    [0,   -0, -1,   -0,   0]
]
kernal1=[[-0.1, -1, -0.1], [-1, 5.4, -1], [-0.1, -1, -0.1]]
kernal2=[[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
kernal0=[[0, -1, 0], [-1, 5, -1], [0, -1, 0]]
def sharpening(img):

    kernel = np.array(kernal1, np.float32)  # 锐化
    dst = cv2.filter2D(img, -1, kernel=kernel)
    return dst

def hisEqulColor2(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe.apply(channels[0], channels[0])

    ycrcb = cv2.merge(channels)
    img = cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR)
    return img

def hisEqulColor1(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])   # 对第1个通道即亮度通道进行全局直方图均衡化并保存
    ycrcb = cv2.merge(channels)
    img = cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR)
    return img
def rgbmediumfilter(img,k=5):
    ret=np.zeros(img.shape,np.uint8)
    ret[:,:,0] = cv2.medianBlur(img[:,:,0],k)
    ret[:,:,1] = cv2.medianBlur(img[:,:,1],k)
    ret[:,:,2] = cv2.medianBlur(img[:,:,2],k)
    return ret


def singleScaleRetinex(img, sigma):
    retinex = np.log10(img) - np.log10(cv2.GaussianBlur(img, (201, 201), sigma))

    # src1 = img.astype(np.float32)
    # gauss = cv2.GaussianBlur(img, ksize=(201, 201), sigmaX=sigma)
    # gauss1 = gauss.astype(np.float32)
    # src1 = (src1 / gauss1) * 255
    # src1[src1 > 255] = 255
    # retinex = np.uint8(src1)

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


def automatedMSRCR(img, sigma_list):
    img = np.float64(img) + 1.0

    img_retinex = multiScaleRetinex(img, sigma_list)

    for i in range(img_retinex.shape[2]):
        unique, count = np.unique(np.int32(img_retinex[:, :, i] * 100), return_counts=True)
        for u, c in zip(unique, count):
            if u == 0:
                zero_count = c
                break

        low_val = unique[0] / 100.0
        high_val = unique[-1] / 100.0
        for u, c in zip(unique, count):
            if u < 0 and c < zero_count * 0.1:
                low_val = u / 100.0
            if u > 0 and c < zero_count * 0.1:
                high_val = u / 100.0
                break

        img_retinex[:, :, i] = np.maximum(np.minimum(img_retinex[:, :, i], high_val), low_val)

        img_retinex[:, :, i] = (img_retinex[:, :, i] - np.min(img_retinex[:, :, i])) / \
                               (np.max(img_retinex[:, :, i]) - np.min(img_retinex[:, :, i])) \
                               * 255

    img_retinex = np.uint8(img_retinex)

    return img_retinex


def MSRCP(img, sigma_list=[64], low_clip=0.01, high_clip=0.99):
    img = np.float64(img) + 1.0

    intensity = np.sum(img, axis=2) / img.shape[2]

    retinex = multiScaleRetinex(intensity, sigma_list)

    intensity = np.expand_dims(intensity, 2)
    retinex = np.expand_dims(retinex, 2)

    intensity1 = simplestColorBalance(retinex, low_clip, high_clip)

    intensity1 = (intensity1 - np.min(intensity1)) / \
                 (np.max(intensity1) - np.min(intensity1)) * \
                 255.0 + 1.0

    img_msrcp = np.zeros_like(img)

    for y in range(img_msrcp.shape[0]):
        for x in range(img_msrcp.shape[1]):
            B = np.max(img[y, x])
            A = np.minimum(256.0 / B, intensity1[y, x, 0] / intensity[y, x, 0])
            img_msrcp[y, x, 0] = A * img[y, x, 0]
            img_msrcp[y, x, 1] = A * img[y, x, 1]
            img_msrcp[y, x, 2] = A * img[y, x, 2]

    img_msrcp = np.uint8(img_msrcp - 1.0)

    return img_msrcp


def streching(img):
    # print(img.mean())
    # m=int(img.mean()/50+128)
    # a=int(img.mean()/50+80)
    # b=int(img.mean()/50+200)
    xp = [0, 64, 128, 200, 255]
    fp = [0, 16, 128, 240, 255]
    x = np.arange(256)
    table = np.interp(x, xp, fp).astype('uint8')
    return cv2.LUT(img, table)

def Saturation(img):
    fImg = np.float32(img / 255.0)
    hlsImg = cv2.cvtColor(fImg, cv2.COLOR_BGR2HLS)
    # lsImg = np.zeros(img.shape, np.float32)
    hlsCopy = np.copy(hlsImg)
    hlsCopy[:, :, 2] = (1.8) * hlsCopy[:, :, 2]
    hlsCopy[:, :, 2][hlsCopy[:, :, 2] > 1] = 1
    # HLS2BGR
    lsImg = np.uint8(cv2.cvtColor(hlsCopy, cv2.COLOR_HLS2BGR)*255)
    return lsImg


# images/CV@P4XEUFJYC{D~1)R0D[RP.png images/HM$(}RMJND)]%JS~PYV7%]P.jpg


img=cv2.imread('../images/e66.jpg')
# cv2.imshow("img", img)
# cv2.waitKey()
pic=1
h,w=img.shape[:2]
hh=int(h/pic)
hw=int(w/pic)
res=img.copy()
for i in range(pic):  # [1]480*360==15*11---height
    for j in range(pic):  # [2]column-----------width
        cache = img[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw),:]

        # step1=MSRCR(cache,sigma_list=[64])
        # step1 = MSRCP(cache,sigma_list=[15,80,200])
        # step1 = automatedMSRCR(cache,sigma_list=[15,80,200])
        # img=sharpening(img)
        step1=gauss_division(cache)
        # cv2.imshow("img", step1)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16,16))
        # cl1 = clahe.apply(step1)
        # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.imshow("img", step1)
        # cv2.setMouseCallback("img", get_rgb)
        # cv2.waitKey()

        # step1=MSRCR(step1)
        # cv2.imshow("step1", step1)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # image = Image.fromarray(cv2.cvtColor(step1,cv2.COLOR_BGR2RGB))
        # step1=sharpening(step1)
        # step1=sharpening(step1)
        # step1=sharpening(step1)
        # # step2 = cv2.cvtColor(np.asarray(step2), cv2.COLOR_RGB2BGR)
        # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.imshow("img", step2)
        # cv2.waitKey()
        # step1=streching(step1)
        step1=Saturation(step1)
        # step1=streching(step1)
        # step1= hisEqulColor2(step1)
        # step1=sharpening(step1)
        # cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        # cv2.imshow("img", step3)
        # cv2.waitKey()
        # cv2.destroyAllWindows()
        # conp = np.hstack((step1,step2))
        # cv2.imshow("comparison", conp)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        res[(i * hh):((i + 1) * hh), (j * hw):((j + 1) * hw),:]=step1

# res= gauss_division(img)
# res=sharpening(res)
# res = MSRCR(img,sigma_list=[15,80,200])
cv2.namedWindow('img', cv2.WINDOW_KEEPRATIO)
cv2.imshow("img", res)
cv2.waitKey()
cv2.destroyAllWindows()