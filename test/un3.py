import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('images/unit3_1.tif', cv2.IMREAD_GRAYSCALE)
dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
# 平移还是要靠numpy
dft_shift = np.fft.fftshift(dft)
# # dft_shift = dft
# magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))
# # # float32
# # print(dft.dtype)
#
# rows, cols = img.shape
# crow, ccol = int(rows / 2), int(cols / 2)
#
# # 创建蒙板
# mask = np.zeros((rows, cols, 2), np.uint8)+0.2
# mask[crow - 30:crow + 30, ccol - 30:ccol + 30] = 1
#
# fftshift = dft_shift * mask
# f_ishift = np.fft.ifftshift(fftshift)
# magnitude_spectrum_filter = 20 * np.log(cv2.magnitude(fftshift[:, :, 0], fftshift[:, :, 1]))
# # 此时img_bak为复数
# img_back = cv2.idft(f_ishift)
# img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
#
# plt.subplot(221)
# plt.imshow(img, cmap='gray')
# plt.title('laugh.jpg')
# # 省略x,y坐标
# plt.xticks([]), plt.yticks([])
# plt.subplot(222), plt.imshow(magnitude_spectrum, cmap='gray')
# plt.title('magnitude_spectrum'), plt.xticks([]), plt.yticks([])
# plt.subplot(223), plt.imshow(magnitude_spectrum_filter, cmap='gray')
# # plt.subplot(223), plt.imshow(mask[:,:,0], cmap='gray')
# plt.title('High Pass Filter'), plt.xticks([]), plt.yticks([])
# plt.subplot(224), plt.imshow(img_back, cmap='gray')
# plt.title('High Pass Result'), plt.xticks([]), plt.yticks([])
# plt.show()
# dft=np.fft.fft2(img)
# dft_shift = np.fft.fftshift(dft)
print(dft_shift)
img32Fil = cv2.medianBlur(dft_shift, 3)