import numpy as np
import cv2
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt


def draw_min_rect_circle(image):  # conts = contours
    thresh = cv2.Canny(image, 128, 256)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res_param = []
    best_size = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w*h>best_size:
            best_size = w*h
            res_param = [x,y,w,h]
        # print(x,y,w,h)
    return res_param

class Point_Move():
    showverts = True
    def __init__(self):
        self.img = cv2.imread('app/data/4.jpg')
        self.img  = cv2.cvtColor(self.img , cv2.COLOR_BGR2RGB)
        # self.img = cv2.resize(self.img, (345, 460))
        self.width, self.height = self.img.shape[:2]
        self.size = self.width * self.height
        self.offset = np.sqrt(self.size/225)
        param = draw_min_rect_circle(self.img)
        x, y, w, h = param
        if 4 * w * h<self.size:
            x,y,w,h= 0+self.height*0.05, 0+self.width*0.05, self.height*0.9, self.width*0.9
        self.x = [x, x, x + w, x + w]
        self.y = [y, y + h, y + h, y]
        # 创建figure（绘制面板）、创建图表（axes）
        self.fig = plt.figure(dpi=150)
        self.ax = plt.subplot2grid((1, 1), (0, 0))
        # 设置标题
        self.ax.set_title('Click and drag a point to move it')
        # 设置坐标轴范围
        self.ax.imshow(self.img)

        self.line1 = Line2D(self.x, self.y,
                           ls="-",
                            # markersize = 10,
                           marker='o', markerfacecolor='g',
                           animated=True,
                           color='g')
        self.line2 = Line2D([self.x[3], self.x[0]],
                            [self.y[3], self.y[0]],
                           ls="-",
                            # markersize=10,
                           marker='o', markerfacecolor='g',
                           animated=True,
                           color='g')
        self.ax.add_line(self.line1)
        self.ax.add_line(self.line2)
        self._ind = None
        self.draw_callback_event = self.fig.canvas.mpl_connect('draw_event', self.draw_callback)
        self.button_press_callback_event=self.fig.canvas.mpl_connect('button_press_event', self.button_press_callback)
        self.button_release_callback_event=self.fig.canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.motion_notify_callback_event=self.fig.canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        plt.show()


    def draw_callback(self, event):
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.line1)
        self.ax.draw_artist(self.line2)
        self.fig.canvas.blit(self.ax.bbox)


    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'
        # 在公差允许的范围内，求出鼠标点下顶点坐标的数值
        xt,yt = np.array(self.x),np.array(self.y)
        d = np.sqrt((xt-event.xdata)**2 + (yt-event.ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        # 如果在公差范围内，则返回ind的值
        if d[ind] >=self.offset:
            ind = None
        return ind


    def change(self):
        print('change')
        pts_o = np.float32(np.array([self.x,self.y]).T)
        print(pts_o)
        new_height = max(pts_o[2][0]-pts_o[0][0],pts_o[3][0]-pts_o[1][0])
        new_width = max(pts_o[2][1]-pts_o[0][1],pts_o[1][1]-pts_o[3][1])
        pts_d = np.float32([[0, 0], [0, new_width], [new_height, new_width], [new_height, 0]])  # 这是变换之后的图上四个点的位置
        M = cv2.getPerspectiveTransform(pts_o, pts_d)
        dst = cv2.warpPerspective(self.img, M, (new_height, new_width))  # 最后一参数是输出dst的尺寸。可以和原来图片尺寸不一致。按需求来确定
        self.fig.canvas.mpl_disconnect(self.draw_callback_event)
        self.fig.canvas.mpl_disconnect(self.button_press_callback_event)
        self.fig.canvas.mpl_disconnect(self.button_release_callback_event)
        self.fig.canvas.mpl_disconnect(self.motion_notify_callback_event)
        self.ax.cla()
        self.ax = plt.subplot2grid((1, 1), (0, 0))
        self.ax.imshow(dst)
        plt.draw()


    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts:
            return
        if event.inaxes==None:
            return
        if event.button != 1:
            return
        self._ind = self.get_ind_under_point(event)
        # print(event.dblclick)
        if event.dblclick == True:
            self.change()


    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts: return
        if event.button != 1: return
        self._ind = None

    # 鼠标移动的事件
    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts:
            return
        if self._ind is None:
            return
        if event.inaxes is None:
            return
        if event.button != 1:
            return
        # 更新数据
        x,y = event.xdata, event.ydata
        self.x[self._ind] = x
        self.y[self._ind] = y
        self.line1 = Line2D(self.x, self.y,
                           ls="-",
                           marker='o', markerfacecolor='g',
                           animated=True,
                           color='g')
        self.line2 = Line2D([self.x[0], self.x[3]],
                            [self.y[0], self.y[3]],
                           ls="-",
                           marker='o', markerfacecolor='g',
                           animated=True,
                           color='g')
        self.ax.add_line(self.line1)
        self.ax.add_line(self.line2)
        self.fig.canvas.restore_region(self.background)
        self.ax.draw_artist(self.line1)
        self.ax.draw_artist(self.line2)
        self.fig.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    Point_Move()