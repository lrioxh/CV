import cv2
import numpy as np
import time
import matplotlib.pyplot as plt


img = cv2.imread('images/unit3_1.tif', cv2.IMREAD_GRAYSCALE)
# img = cv2.imread('images/unit3_2.tif', cv2.IMREAD_GRAYSCALE)
h,w=img.shape
# h2,w2=img2.shape
# print(h,w,h2,w2)
padding=cv2.copyMakeBorder(img, 0,h,0,w, cv2.BORDER_CONSTANT, value=0)
# cv2.imshow('',padding)

dft = cv2.dft(np.float32(padding), flags=cv2.DFT_COMPLEX_OUTPUT)
start1 = time.perf_counter()
dft_shift = np.fft.fftshift(dft)
# dft_shift= np.zeros((2*h,2*w, 2), np.float32)
# dft_shift[h:,w:,:]=dft[:h,:w,:]
# dft_shift[:h,:w,:]=dft[h:,w:,:]
# dft_shift[:h,w:,:]=dft[h:,:w,:]
# dft_shift[h:,:w,:]=dft[:h,w:,:]
end1 = time.perf_counter()

start2 = time.perf_counter()
for i in range(h):
    for j in range(w):
        if (i+j)%2==1:
            padding[i,j]= -padding[i,j]
end2 = time.perf_counter()
dft = cv2.dft(np.float32(padding), flags=cv2.DFT_COMPLEX_OUTPUT)

magnitude_spectrum =np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])+1)
dft_shift = np.fft.fftshift(dft)
magnitude_spectrum2 =np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])+1)

# mask = np.zeros((2*h,2*w, 2), np.uint8)+0.3
# mask[h - 30:h + 30, w - 30:w + 30] = 1
# fftshift = dft_shift * mask
#
# f_ishift = np.fft.ifftshift(fftshift)
#
# img_back = cv2.idft(f_ishift)
# img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
#
normalize = (magnitude_spectrum -2) / (np.max(magnitude_spectrum)-2)
magnitude_spectrum_uint8 = np.uint8(255 * (np.power(normalize, 2)))
normalize = (magnitude_spectrum2 -2) / (np.max(magnitude_spectrum2)-2)
magnitude_spectrum_uint8_2 = np.uint8(255 * (np.power(normalize, 2)))
# magnitude_spectrum_uint8 = np.uint8(255 * (magnitude_spectrum / np.max(magnitude_spectrum)))
# magnitude_spectrum_uint8_2 = np.uint8(255 * (magnitude_spectrum2 / np.max(magnitude_spectrum2)))

# img_back_uint8 = np.uint8(255 * (img_back / np.max(img_back)))
print(end1-start1,end2-start2)
conp = np.hstack((magnitude_spectrum_uint8,magnitude_spectrum_uint8_2))
cv2.imshow("comparison", conp)
cv2.waitKey()
cv2.destroyAllWindows()