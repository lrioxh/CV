import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageEnhance
#这个函数用来对扫描后生成的扫描图进行对比度增强
def image_enhancement(image):
    '''图像增强，增强对比度和亮度'''
    enh_con = ImageEnhance.Contrast(image)
    # contrast = 5 参数5-10都可以
    image_contrasted = enh_con.enhance(10)
    # 亮度增强
    enh_bri = ImageEnhance.Brightness(image_contrasted)
    image_contrasted1 = cv2.cvtColor(np.asarray(image_contrasted), cv2.COLOR_RGB2BGR)  # PIL转cv2
    # clear = getImageVar(image_contrasted1)
    # # print(clear)
    # brightness = max(round(clear / 2000, 1), 1)
    # # print(brightness)
    # image_brightened = enh_bri.enhance(brightness)
    # return image_brightened
    return image_contrasted1


image = Image.open("smh.jpg")
image.show()

final_img=image_enhancement(image)
cv2.imshow('PIL enhance',final_img)
cv2.waitKey(0)