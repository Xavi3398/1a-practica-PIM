from utils import *
from ITab import *
import cv2
from matplotlib import pyplot as plt


class Segmentation(ITab):

    def __init__(self, model, view):
        super().__init__(model, view)
    
    def plot(self):
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        plt.title('SEGMENTATION')
        ax.imshow(self.m.img_result, cmap='gray', aspect=self.m.get_aspect())
        ax.axis(False)

        if self.m.point is not None:
            plt.plot(self.m.point[0], self.m.point[1], marker="o", markersize=5,
                     markeredgecolor=np.array(self.m.color).astype('float')/255,
                     markerfacecolor=np.array(self.m.color).astype('float')/255)

        fig.canvas.mpl_connect('button_press_event', self.segmentation_clicked_event)

        self.m.seg_plot = draw_figure(self.v.window["Segmentation_Canvas"].TKCanvas, fig, self.m.seg_plot)

    def see_changes(self):
        self.plot()

        if self.m.point is not None:
            thresh = self.v.values["Slider_segmentation"]
            x, y = self.m.point
            img = self.m.img_result.copy()
            value = img[y, x]

            # Apply Threshold
            img[img < value - thresh] = 0
            img[img > value + thresh] = 0
            img[img > 0] = 1

            # Region Growing
            mask = region_growing(img, (x, y))

            # Apply mask
            self.m.img_result_copy = self.m.img_result.copy()
            self.m.img_result_copy[mask == 0] = 0

            # Plot resulting image
            fig = plt.figure(figsize=(5, 4))
            ax = fig.add_subplot(111)
            ax.axis(False)
            plt.title('RESULTING IMAGE')

            # Plot depending on type of image
            if self.v.values["BW_Type"]:
                ax.imshow(mask, cmap="gray", aspect=self.m.get_aspect())
            elif self.v.values["Gray_Type"]:
                ax.imshow(self.m.img_result_copy, cmap="gray", aspect=self.m.get_aspect())
            elif self.v.values["Alpha_Type"]:
                mask_r = color_mask(mask, self.m.color)  # Red mask
                rgb = cv2.cvtColor((self.m.img_result * 255).astype("uint8"), cv2.COLOR_GRAY2RGB)  # Gray image to RGB
                ax.imshow(painter(rgb, mask_r, self.v.values["Slider_alpha"]),
                          aspect=self.m.get_aspect())  # Merge layers

            self.m.out_img_plot = draw_figure(self.v.window["IMAGE-OUT"].TKCanvas, fig, self.m.out_img_plot)

        else:
            fig = plt.figure(figsize=(5, 4))
            ax = fig.add_subplot(111)
            ax.axis(False)
            plt.title('RESULTING IMAGE')
            ax.imshow(self.m.img_result, cmap="gray", aspect=self.m.get_aspect())
            self.m.out_img_plot = draw_figure(self.v.window["IMAGE-OUT"].TKCanvas, fig, self.m.out_img_plot)

    def segmentation_clicked_event(self, ev):
        if ev is not None and ev.xdata is not None and ev.ydata is not None:
            self.m.point = [round(ev.xdata), round(ev.ydata)]
            self.plot()
