from utils import *
from ITab import *
from matplotlib import pyplot as plt


class Crop(ITab):

    def __init__(self, model, view):
        super().__init__(model, view)

    def plot(self):

        # Plot image
        fig = plt.figure(figsize=(5, 4))
        plt.title('CROPPED IMAGE')
        ax = fig.add_subplot(111)
        ax.axis(False)
        ax.imshow(self.m.img_result, cmap="gray", aspect=self.m.get_aspect())
        self.m.crop_plot = draw_figure(self.v.window["IMAGE-CROPPED"].TKCanvas, fig, self.m.crop_plot)

        # Plot lines
        ax.plot([int(self.v.values['Slider_left']), int(self.v.values['Slider_left'])],
                [0, self.m.img_result.shape[0]], color='red')
        ax.plot([int(self.v.values['Slider_right']), int(self.v.values['Slider_right'])],
                [0, self.m.img_result.shape[0]], color='yellow')
        ax.plot([0, self.m.img_result.shape[1]],
                [int(self.v.values['Slider_up']), int(self.v.values['Slider_up'])], color='green')
        ax.plot([0, self.m.img_result.shape[1]],
                [int(self.v.values['Slider_down']), int(self.v.values['Slider_down'])], color='blue')

    def cropping_slider_event(self, slider=None):

        # Fix slider values
        if slider == "Slider_up":
            if int(self.v.values["Slider_up"]) > int(self.v.values["Slider_down"]):
                self.v.window["Slider_up"].Update(value=int(self.v.values["Slider_down"]))
        elif slider == "Slider_down":
            if int(self.v.values["Slider_up"]) > int(self.v.values["Slider_down"]):
                self.v.window["Slider_down"].Update(value=int(self.v.values["Slider_up"]))
        elif slider == "Slider_left":
            if int(self.v.values["Slider_left"]) > int(self.v.values["Slider_right"]):
                self.v.window["Slider_left"].Update(value=int(self.v.values["Slider_right"]))
        elif slider == "Slider_right":
            if int(self.v.values["Slider_left"]) > int(self.v.values["Slider_right"]):
                self.v.window["Slider_right"].Update(value=int(self.v.values["Slider_left"]))

        self.plot()

    def see_changes(self):

        self.plot()
        self.m.img_result_copy = self.m.img_result[int(self.v.values["Slider_up"]):int(self.v.values["Slider_down"]),
                                                   int(self.v.values["Slider_left"]):int(self.v.values["Slider_right"])]

        # Plot
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.axis(False)
        plt.title('RESULTING IMAGE')
        ax.imshow(self.m.img_result_copy, cmap="gray", aspect=self.m.get_aspect())
        self.m.out_img_plot = draw_figure(self.v.window["IMAGE-OUT"].TKCanvas, fig, self.m.out_img_plot)
