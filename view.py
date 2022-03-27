import PySimpleGUI as sg


class View:

    def __init__(self, model):
        self.m = model
        self.tab = None
        self.window = None
        self.values = None
        self.event = None

        self.set_layout()

    def read_input(self):
        self.event, self.values = self.window.read()
        self.tab = self.window['tabgrp'].Get()

    def set_layout(self):
        # Input image, with file browser
        file_list_column = [
            [
                sg.Text("DICOM File:"),
                sg.In(key="Text_Name", size=(25, 15)),
                sg.In(key="File_Name", enable_events=True, visible=False),
                sg.In(key="Folder_Name", enable_events=True, visible=False),
                sg.FileBrowse('File', target='File_Name', file_types=[["DICOM Files", "*.dcm"]]),
                sg.FolderBrowse('Folder', target='Folder_Name'),
                sg.Button("DICOM Info", key="DICOM-Info")
            ],
            [sg.Canvas(key="IMAGE-IN")],
            [sg.Canvas(key="IMAGE-OUT")]
        ]

        # Windowing
        windowing_layout = [
            [sg.Canvas(key="Histogram", pad=(50, 10))],
            [sg.Text("Min:", pad=((50, 0), (0, 0))),
             sg.Slider(key="Slider_min", default_value=0, pad=(30, 0), size=(43, 15), orientation="horizontal",
                       range=(0, 1), resolution=0.01, enable_events=True)],
            [sg.Text("Max:", pad=((50, 0), (5, 5))),
             sg.Slider(key="Slider_max", default_value=1, pad=(26, 5), size=(43, 15), orientation="horizontal",
                       range=(0, 1), resolution=0.01, enable_events=True)]
        ]

        # Cropping
        crop_layout = [
            [sg.Slider(key="Slider_left", default_value=0, pad=(130, 0), size=(38, 15), orientation="horizontal",
                       range=(0, 500), enable_events=True, trough_color='red')],
            [
                sg.Slider(key="Slider_up", default_value=0, pad=(0, 0), size=(18, 15), orientation="vertical",
                          range=(0, 500), enable_events=True, trough_color='green'),
                sg.Canvas(key="IMAGE-CROPPED"),
                sg.Slider(key="Slider_down", default_value=512, pad=(0, 0), size=(18, 15), orientation="vertical",
                          range=(0, 500), enable_events=True, trough_color='blue')
            ],
            [sg.Slider(key="Slider_right", default_value=512, pad=(130, 0), size=(38, 15), orientation="horizontal",
                       range=(0, 500), enable_events=True, trough_color='yellow')]
        ]

        # Segmentation
        segmentation_layout = [
            [sg.Canvas(key="Segmentation_Canvas", pad=(50, 10))],
            [sg.Text("Threshold:", pad=((50, 0), (0, 0))),
             sg.Slider(key="Slider_segmentation", default_value=0.1, pad=(26, 5), size=(43, 15),
                       orientation="horizontal",
                       range=(0, 1), resolution=0.01, enable_events=True)],
            [sg.Text("Type of image:", pad=((50, 0), (10, 0))),
             sg.Radio("BW mask", "Image_Type", key="BW_Type", default=False, pad=((10, 0), (10, 0))),
             sg.Radio("Gray mask", "Image_Type", key="Gray_Type", default=False, pad=((10, 0), (10, 0))),
             sg.Radio("Alpha mask", "Image_Type", key="Alpha_Type", default=True, pad=((10, 0), (10, 0)))],
            [sg.Text("Alpha:", pad=((50, 0), (0, 0))),
             sg.Slider(key="Slider_alpha", default_value=0.2, pad=(26, 5), size=(43, 15), orientation="horizontal",
                       range=(0, 1), resolution=0.01, enable_events=True)]
        ]

        # Tab group
        tabgrp = [
            [sg.TabGroup([[
                sg.Tab('Windowing', windowing_layout),
                sg.Tab('Crop', crop_layout),
                sg.Tab('Segmentation', segmentation_layout)
            ]], key="tabgrp", enable_events=True)],
            [sg.Button("See changes", key="See_changes", pad=((200, 0), (20, 0))),
             sg.Button("Apply", key="Apply", pad=((10, 0), (20, 0))),
             sg.Button("Reset", key="Reset", pad=((10, 0), (20, 0)))],
            [sg.Column(
                [[sg.Text("Frame:", pad=((30, 0), (0, 0)), key='Frame_Text'),
                  sg.Slider(key="Frame", default_value=0, pad=(0, 0), size=(35, 15), orientation="horizontal",
                            range=(0, 500), enable_events=True),
                  sg.Text("View:", pad=((30, 0), (0, 0)), key='Axis_Text'),
                  sg.Combo(['End', 'Front', 'Top'], key="Axis", default_value='Top', pad=(0, 0), enable_events=True),
                  sg.Button("Set", key="Tensor_Change", pad=(30, 0))]],
                visible=False,
                pad=(0, 20),
                key="Frame_Elements"
            )]
        ]

        # Full layout
        layout = [[
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(tabgrp),
        ]]

        self.window = sg.Window("Image Viewer", layout, return_keyboard_events=True)

    def reset_sliders(self):

        # Sliders of windowing tab
        self.window['Slider_min'].Update(value=0)
        self.window["Slider_max"].Update(value=1)

        # Sliders of cropping tab
        self.window["Slider_up"].Update(range=(0, self.m.img_result.shape[0]), value=0)
        self.window["Slider_down"].Update(range=(0, self.m.img_result.shape[0]), value=self.m.img_result.shape[0])
        self.window["Slider_left"].Update(range=(0, self.m.img_result.shape[1]), value=0)
        self.window["Slider_right"].Update(range=(0, self.m.img_result.shape[1]), value=self.m.img_result.shape[1])

    def reset_frame_controls(self):
        self.window["Frame"].Update(value=0)
        self.window["Axis"].Update(value='Top')