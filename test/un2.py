import cv2
import numpy as np
from matplotlib import pyplot as plt
# 读图片
img = cv2.imread('images/Fig0327(a)(tungsten_original).tif',cv2.IMREAD_GRAYSCALE)
# hist,bins = np.histogram(img.flatten(),256,[0,256])
# cdf = hist.cumsum()
# cdf_normalized = cdf * hist.max() / cdf.max()
# plt.plot(cdf_normalized, color = 'b')
# plt.hist(img.flatten(),256,[0,256], color = 'r')
# plt.xlim([0,256])
# plt.legend(('cdf','histogram'), loc = 'upper left')
# plt.show()
# print(img[2,3])
# equ = cv2.equalizeHist(img)
# res = np.hstack((img,equ))
# #stacking images side-by-side
# cv2.imwrite('globalH.jpg',res)
# cv2.imshow('img',res)
# cv2.waitKey()
# cv2.destroyAllWindows()

# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16,16))
# cl1 = clahe.apply(img)
# res = np.hstack((img,cl1))
# cv2.imwrite('localH.jpg',res)
# cv2.imshow('img',res)
# cv2.waitKey()
# cv2.destroyAllWindows()

# img=img[1:100,1:100]
gMean,gStd=cv2.meanStdDev(img)
# print(gMean[0][0],gStd[0][0])
# hist = cv2.calcHist([img], [0], None, [256], [0, 256])
hist = np.bincount(img.ravel(), minlength=256)
# print(hist)
E=4
k0=0.4
k1=0.02
k2=0.4
l=3
w=img.shape[1]
h=img.shape[0]
def local_enhance(img,E,k0,k1,k2,l=3):
    border=int((l-1)/2)
    padding=cv2.copyMakeBorder(img, border,border,border,border, cv2.BORDER_CONSTANT, value=0)
    # img=padding
    for i in range(border,border+h):
        for j in range(border,border+w):
            if j==border:
                M,S=cv2.meanStdDev(padding[i-border:i+border+1,j-border:j+border+1])
                M=M[0][0];S=S[0][0]
            else:
                Mf=M;Sf=S
                # print(j)
                # print(padding[i - border:i + border+1, j - border:j + border+1])
                # M2, S22 = cv2.meanStdDev(padding[i - border:i + border+1, j - border:j + border+1])
                a=padding[i-border:i+border+1,j+border].astype("int32")
                # print(sum(a**2))
                b=padding[i-border:i+border+1,j-border-1].astype("int32")
                # M=Mf+(np.sum(padding[i-border:i+border+1,j+border])-np.sum(padding[i-border:i+border+1,j-border-1]))/9
                M=round(Mf+float(sum(a)-sum(b))/l**2,7)
                # a=np.sum((padding[i-border:i+border+1,j+border])**2).astype("int32")
                # b=np.sum((padding[i-border:i+border+1,j-border-1])**2).astype("int32")
                S2=Sf**2+Mf**2-M**2+float(sum(a**2)-sum(b**2))/l**2
                if S2>0:
                    S=round(pow(S2,0.5),5)
                else:
                    S=0

            if M<=k0*gMean and k1*gStd<=S and S<=k2*gStd:
                img[i-border,j-border]=E*padding[i,j]
                # img[i, j] = E * padding[i, j]
    return img

img=local_enhance(img,E,k0,k1,k2,l)
cv2.imshow('img',img)
cv2.waitKey()
cv2.destroyAllWindows()
# print(padding)
    # return 0

# plt.figure(
#     # dpi=5,
#     # figsize=(45,22)
# )
# plt.title("Grayscale Histogram")
# plt.xlabel("Bins")
# plt.ylabel("# of Pixels")
# plt.plot(hist)
# plt.xlim([0, 256])
# plt.show()