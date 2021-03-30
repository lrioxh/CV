import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('../images/u51.tif',cv2.IMREAD_GRAYSCALE)
cv2.imshow("img", img)
cv2.waitKey(0)

# gray = img / 255.0
sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
mag=np.abs(sobelx)+np.abs(sobelx)
# mag, ang = cv2.cartToPolar(sobelx, sobely, angleInDegrees=1)
index=int(img.size*0.9997)
threshold =np.sort(mag.reshape(1,-1))[0,index]
# print(sort_mag)
X, Y = np.where((mag > threshold))
g = np.zeros(img.shape)
g[X, Y] = 1
# cv2.imshow("g", g)
# cv2.waitKey(0)
g=g*img
print(np.max(g))
cv2.imshow("g", g)
cv2.waitKey(0)
g=g[g>0]
h = np.bincount(np.uint8(g), minlength=256)
# print(np.uint(g))
# h,x = np.histogram(np.uint(g),256,[0,256])
# print(h)
# plt.plot(h)
# plt.show()


# 整体均值
# meanall = np.sum(np.dot(h, np.array([n for n in range(256)])))
# meanall = meanall / np.sum(np.array([n for n in range(256)]))
# print(meanall)
meanall=np.mean(g)
# print(meanall)
maxscore = 0
gi = []
# threshold_=0
for i in range(1, 255):
    g1=g[g<i]
    g2=g[g >= i]
    if len(g1)>0 and len(g2)>0:
        mean1=np.mean(g1)
        mean2 = np.mean(g2)
        score = sum(h[:i]) * ((meanall - mean1) ** 2) + sum(h[i:]) * ((meanall - mean2) ** 2)

        gi.append(score)
        if maxscore < score:
            maxscore = score
            threshold = i
    else:
        gi.append(0)
# print("max value = %d, th = %d" % (np.max(gi), threshold))

# 用于绘图
# print(gi)
plot1 = plt.figure()
# 绘制直方图
plt.bar(np.array([n for n in range(256)]), h)
# 绘制分割点
threshold=int(threshold+gi.count(maxscore)*0.5)
plt.axvline(threshold, color='r')
# 绘制类间方差遍历过程示意图
# plt.scatter([n for n in range(256)], (gi - min(gi)) / (max(gi) - min(gi)) * max(h))
plt.scatter([n+1 for n in range(254)],np.array(gi)*0.5*np.max(h)/np.max(gi))
plt.show()

img[img>threshold]=255
img[img<=threshold]=0
cv2.imshow("img", img)
cv2.waitKey(0)

