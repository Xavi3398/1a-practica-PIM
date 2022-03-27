from utils import *
from ITab import *
import cv2
from matplotlib import pyplot as plt


class Windowing(ITab):

    def __init__(self, model, view):
        super().__init__(model, view)

    def plot(self):

        if self.m.img_result is not None:

            # Histogram
            hist = cv2.calcHist([(self.m.img_result * 100).astype('uint16')], [0], None, [101], (0, 101)).flatten()
            fig = plt.figure(figsize=(5, 4))
            ax = fig.add_subplot(111)
            ax.fill_between(range(101), hist, color='blue')
            plt.xticks(range(0, 110, 10), ["{:.1f}".format(el) for el in np.arange(0, 1.1, .1)])

            # Deleted areas
            ax.fill_between([0, int(self.v.values["Slider_min"] * 100)], [int(max(hist))] * 2, alpha=.3, color="red")
            ax.fill_between([int(self.v.values["Slider_max"] * 100), 100], [int(max(hist))] * 2, alpha=.3, color="red")

            # Plot figure
            self.m.windowing_hist_plot = draw_figure(self.v.window["Histogram"].TKCanvas, fig,
                                                     self.m.windowing_hist_plot)

    def windowing_slider_event(self, slider):
        if int(self.v.values["Slider_max"]) < int(self.v.values["Slider_min"]):
            if slider == "Slider_min":
                self.v.window["Slider_min"].Update(value=int(self.v.values["Slider_max"]))
            else:
                self.v.window["Slider_max"].Update(value=int(self.v.values["Slider_min"]))

        self.plot()

    def see_changes(self):

        # Update histogram
        self.plot()

        # New minimum amb maximum values
        min_s = self.v.values["Slider_min"]
        max_s = self.v.values["Slider_max"]

        # Iterate over pixels of image
        self.m.img_result_copy = self.m.img_result.copy()
        for y in range(self.m.img_result.shape[0]):
            for x in range(self.m.img_result.shape[1]):
                # self.m.img_result_copy[y, x] = (self.m.img_result[y, x] - min_s) * (1 - 0) / (max_s - min_s) + 0
                self.m.img_result_copy[y, x] = (self.m.img_result[y, x] - min_s) / (max_s - min_s)

        # Set values out of bounds
        self.m.img_result_copy[self.m.img_result_copy < 0] = 0
        self.m.img_result_copy[self.m.img_result_copy > 1] = 1

        # Plot
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.axis(False)
        plt.title('RESULTING IMAGE')
        ax.imshow(self.m.img_result_copy, cmap="gray", aspect=self.m.get_aspect())
        self.m.out_img_plot = draw_figure(self.v.window["IMAGE-OUT"].TKCanvas, fig, self.m.out_img_plot)
