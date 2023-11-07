import pyqtgraph as pg
import numpy as np
import time, random


class SigPlot(pg.PlotWidget):
    def __init__(self, fs=500, channels=8, ts=5, vs=40) -> None:
        super().__init__()
        self.fs = fs
        self.fps = int(self.fs / 55) # ?

        self.channels = channels
        self.time_scale = ts
        self.vert_scale = vs
        self.__init_canvas()

    def __generate_cool_colors(self):
        r = random.randint(0, 128)  # 蓝色分量
        g = random.randint(128, 255)  # 绿色分量
        b = random.randint(128, 255)  # 紫色分量
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def update_data(self, plotdata):
        self.Data_y[: self.channels, self.curr_position] = plotdata[: self.channels]
        self.curr_position += 1
        # whether to update plot base on fps config
        if self.curr_position % self.fps == 0:
            self.__update_plot()
        # redraw canvas and reset pointer if reached right limit
        if self.curr_position == self.display_length:
            self.__update_plot()
            self.last_position = 0
            self.curr_position = 0

    def __update_plot(self):
        if self.last_position == self.curr_position:
            return
        for i in range(self.channels):
            self.curve[i].setData(y=self.Data_y[i] + self.vert_scale * (2 * i + 1))
        self.vLine.setPos(self.curr_position)

    def __init_canvas(self):
        # Remove all items from the PlotItem’s ViewBox.
        self.plotItem.clear()
        self.display_length = int(self.fs * self.time_scale)
        self.Data_y = np.zeros((self.channels, self.display_length))
        self.last_position = 0
        self.curr_position = 0
        self.__set_x_ticks()
        self.__set_y_ticks()
        # 显示网格线
        self.plotItem.showGrid(x=True)
        self.curve = []  # type: list[pg.PlotDataItem]
        for i in range(self.channels):
            # 设置线条的颜色
            pen = pg.mkPen(self.__generate_cool_colors(), width=0.7)
            # 实例化单个绘图曲线
            curve = pg.PlotCurveItem(
                self.Data_y[i] + (i * 2 + 1) * self.vert_scale,
                pen=pen,
                antialias=True,
            )
            # 添加线条
            self.addItem(curve)
            self.curve.append(curve)
        # 设置指示线
        self.vLine = pg.InfiniteLine(angle=90, movable=True)
        # 添加指示线
        self.addItem(self.vLine, ignoreBounds=True)
        # 设置鼠标失能
        self.enableMouse(False)

    def __set_x_ticks(self):
        # 设置X轴宽度
        self.setXRange(0, self.display_length, padding=0)
        ax = self.plotItem.getAxis("bottom")
        ax.setTicks(
            [
                [
                    (i, str(self.time_scale * i / self.display_length))
                    for i in range(
                        0, self.display_length + 1, int(self.display_length / 10)
                    )
                ]
            ]
        )

    def __set_y_ticks(self):
        # 设置Y轴高度
        self.setYRange(0, self.channels * 2 * self.vert_scale, padding=0)
        ax = self.plotItem.getAxis("left")
        ax.setTicks(
            [
                [
                    ((i * 2 + 1) * self.vert_scale, "C" + str(i))
                    for i in range(0, self.channels)
                ]
            ]
        )

    def wheelEvent(self, ev):
        pass

    def mousePressEvent(self, ev):
        pass

    def mouseReleaseEvent(self, ev):
        pass

    def mouseMoveEvent(self, ev):
        pass
