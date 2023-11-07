import pyqtgraph as pg
import numpy as np
import time, random


class EmgPlot(pg.PlotWidget):
    def __init__(self, fs=500, channels=8, imu_channels=6, fpi=9, ts=5, vs=40) -> None:
        super().__init__()
        self.fs = fs
        self.fps = int(self.fs / 55) # 1/fps
        self.imu_channels = imu_channels

        self.channels = channels + self.imu_channels

        self.time_scale = ts
        self.voltage_scale = vs
        self.fps_stamp = time.perf_counter()
        self.__init_canvas()

    def __generate_cool_colors(self):
        r = random.randint(0, 128)  # 蓝色分量
        g = random.randint(128, 255)  # 绿色分量
        b = random.randint(128, 255)  # 紫色分量
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def update_data(self, plotdata):
        # self.Data_y = np.insert(self.Data_y[:self.channels,1:], self.display_length-1, values=plotdata*0.02235174, axis=1)
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

    def reset_channels(self, channels):
        self.channels = channels
        self.__init_canvas()

    def __update_plot(self):
        if self.last_position == self.curr_position:
            return
        dstart = time.perf_counter()
        for i in range(self.channels):
            self.curve[i].setData(y=self.Data_y[i] + self.voltage_scale * (2 * i + 1))
        self.vLine.setPos(self.curr_position)
        # print("Draw efficiency(FPS):", 1 / (time.perf_counter() - dstart))
        # print("FPS:", 1 / (time.perf_counter() - self.fps_stamp))
        # self.fps_stamp = time.perf_counter()

    def __init_canvas(self):
        self.plotItem.clear()
        # self.setBackground('#f0f0f0')
        self.display_length = int(self.fs * self.time_scale)
        self.trigger_plot = []
        self.Data_y = np.zeros((self.channels, self.display_length))
        self.last_position = 0
        self.curr_position = 0
        self.__set_x_ticks()
        self.__set_y_ticks()
        self.plotItem.showGrid(x=True)
        self.curve = []  # type: list[pg.PlotDataItem]
        for i in range(self.channels):
            pen = pg.mkPen(self.__generate_cool_colors(), width=0.7)
            curve = pg.PlotCurveItem(
                self.Data_y[i] + (i * 2 + 1) * self.voltage_scale,
                pen=pen,
                antialias=True,
            )
            # curve.setSegmentedLineMode('on')
            self.addItem(curve)
            self.curve.append(curve)
            # self.plotItem.plot(self.Data_y[i] + (i * 2 + 1) * self.voltage_scale, pen=pen)
        self.vLine = pg.InfiniteLine(angle=90, movable=True)
        self.addItem(self.vLine, ignoreBounds=True)
        self.enableMouse(False)

    def __set_x_ticks(self):
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
        self.setYRange(0, self.channels * 2 * self.voltage_scale, padding=0)
        ax = self.plotItem.getAxis("left")
        ax.setTicks(
            [
                [
                    ((i * 2 + 1) * self.voltage_scale, "C" + str(i))
                    if i < 8
                    else ((i * 2 + 1) * self.voltage_scale, "IMU")
                    for i in range(0, self.channels + 1)
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
