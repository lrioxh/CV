import numpy as np

m=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
m=np.array(m).reshape(4,5)
print(m)

def zigzag(m):
    r=m.shape[0]
    c=m.shape[1]
    i,j = 0,0
    line = []#经历过的数字
    up = True#方向向上
    for t in range(r*c):
        line.append(m[j,i])
        #碰壁后就转向
        if up:#右上
            if i==c-1:    # 碰到了右边界
                j += 1        # 向下走一格
                up=False      # 转向
            elif j==0:    # 碰到了上边界
                i += 1        # 向右走一格
                up=False      # 转向
            else:         # 没碰到边界
                i += 1        # 向右上斜着走一格
                j -= 1
        else:#左下
            if j==r-1:    # 碰到了下边界
                i += 1        # 向右走一格
                up=True       # 转向
            elif i==0:    # 碰到了左边界
                j += 1        # 向下走一格
                up=True       # 转向
            else:         # 没碰到边界
                i -= 1        # 向左下斜着走一格
                j += 1
    return np.array(line)

def zigzagscan(img,n=20,b=0.5):
    line=zigzag(img.astype(np.float32))
    r = img.shape[0]
    c = img.shape[1]
    i, j= 0, 0
    res = np.zeros(img.shape, np.uint8)
    k = int(n / 2)
    up = True  # 方向向上
    for t in range(r * c):
        print(t)
        if k <= n:
            mean = np.mean(line[:k])
        elif k > n:
            mean = np.mean(line[k - int(n / 2):])
        else:
            mean=np.mean(line[k -n:k])
            # mean = mean_ + (line[k - 1] - line[k - 1 - n]) / n
        mean_ = mean
        tr = mean * b
        # print(img[j,i],line[k-1])
        res[j, i] = 1 if img[j,i] > tr else 0
        # 碰壁后就转向
        k += 1
        if up:  # 右上
            if i == c - 1:  # 碰到了右边界
                j += 1  # 向下走一格
                up = False  # 转向
            elif j == 0:  # 碰到了上边界
                i += 1  # 向右走一格
                up = False  # 转向
            else:  # 没碰到边界
                i += 1  # 向右上斜着走一格
                j -= 1
        else:  # 左下
            if j == r - 1:  # 碰到了下边界
                i += 1  # 向右走一格
                up = True  # 转向
            elif i == 0:  # 碰到了左边界
                j += 1  # 向下走一格
                up = True  # 转向
            else:  # 没碰到边界
                i -= 1  # 向左下斜着走一格
                j += 1
    return res*255

print(zigzagscan(m))