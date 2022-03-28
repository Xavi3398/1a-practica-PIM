from segmentation import *
import glob
import pydicom
import numpy as np
from matplotlib import pyplot as plt


class Controls:

    def __init__(self, model, view):
        self.m = model
        self.v = view

    #  --------------------------------- View functions ----------------------------------

    def read_dcom_file(self):
        # Hide frame controls
        self.v.window["Frame_Elements"].Update(visible=False)

        # Read file
        self.m.file = self.v.values["File_Name"]
        self.m.dcm = pydicom.dcmread(self.m.file)

        # Delete tensor if exists
        self.m.tensor = None

        # Get dcom aspect ratio
        self.m.dim_y = float(self.m.dcm["PixelSpacing"][0])
        self.m.dim_x = float(self.m.dcm["PixelSpacing"][1])

        # Get dcom image
        self.m.img_dcm = np.rot90(self.m.dcm.pixel_array, k=2)
        self.m.img_result = self.m.img_dcm / np.max(self.m.img_dcm)
        self.m.img_result_copy = self.m.img_result

        # Plot image
        self.plot_original_image()

        # Set cropping slider values
        self.v.reset_sliders()

    def read_dcom_folder(self):
        # Show frame controls
        self.v.window["Frame_Elements"].Update(visible=True)

        self.m.file = self.v.values["Folder_Name"]
        imgs = []

        files = glob.glob(self.m.file + "/*.dcm")

        # Read files in folder
        for file in files:
            dcm = pydicom.dcmread(file)
            imgs.append([dcm.pixel_array, dcm["InstanceNumber"].value])

        # Order slices by instance number and get the ordered list of images
        imgs = sorted(imgs, key=lambda t: t[1])
        imgs = [img[0] for img in imgs]

        # Change order of axis (Y, X, Z) instead of (Z, Y, X)
        self.m.tensor = np.moveaxis(np.array(imgs), 0, -1)

        # Load first frame
        self.m.dcm = pydicom.dcmread(files[0])

        # Get aspect ratio
        self.m.dim_y = float(self.m.dcm["PixelSpacing"][0])
        self.m.dim_x = float(self.m.dcm["PixelSpacing"][1])
        self.m.dim_z = float(self.m.dcm["SliceThickness"].value)

        # Get img from file and rotate it
        self.m.img_dcm = np.rot90(self.m.dcm.pixel_array, k=2)
        self.m.img_result = self.m.img_dcm / np.max(self.m.img_dcm)
        self.m.img_result_copy = self.m.img_result

        # Plot image
        self.plot_original_image()

        # Set slider values
        self.v.reset_sliders()
        self.m.point = None

        # Set frame controls
        self.v.window["Frame"].Update(range=(0, self.m.tensor.shape[self.m.axis] - 1))
        self.v.reset_frame_controls()

    def plot_original_image(self):
        fig = plt.figure(figsize=(5, 4))
        ax = fig.add_subplot(111)
        ax.imshow(self.m.img_dcm, cmap='gray', aspect=self.m.get_aspect())
        ax.axis(False)
        plt.title('ORIGINAL IMAGE')
        self.m.in_img_plot = draw_figure(self.v.window["IMAGE-IN"].TKCanvas, fig, self.m.in_img_plot)

    def change_axis(self):

        if self.v.values["Axis"] == 'Front':
            self.m.axis = 0
        elif self.v.values["Axis"] == 'End':
            self.m.axis = 1
        elif self.v.values["Axis"] == 'Top':
            self.m.axis = 2

        # Update frame slider according to axis
        self.v.window["Frame"].Update(range=(0, self.m.tensor.shape[self.m.axis] - 1))

    def change_frame(self):
        self.m.frame = int(self.v.values["Frame"])

    def refresh_image_tensor(self):

        if self.m.axis == 0:
            self.m.img_dcm = np.rot90(self.m.tensor[self.m.frame, :, :], axes=(1, 0))
        elif self.m.axis == 1:
            self.m.img_dcm = np.rot90(self.m.tensor[:, self.m.tensor.shape[1] - 1 - self.m.frame, :], axes=(1, 0))
        elif self.m.axis == 2:
            self.m.img_dcm = np.rot90(self.m.tensor[:, :, self.m.frame], k=2)

        self.m.img_result = self.m.img_dcm / np.max(self.m.img_dcm)
        self.m.img_result_copy = self.m.img_dcm

        self.plot_original_image()
        self.v.reset_sliders()
        self.m.point = None

    def reset(self):

        self.m.img_result = self.m.img_dcm / np.max(self.m.img_dcm)
        self.m.img_result_copy = self.m.img_result

        # Point of segmentation
        self.m.point = None

    def apply(self):
        self.m.img_result = self.m.img_result_copy
        self.v.reset_sliders()
        self.m.point = None
