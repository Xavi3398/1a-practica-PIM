import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def color_mask(mask, color):
    mask_rgb = np.zeros(shape=(mask.shape[0], mask.shape[1], 3), dtype='uint8')
    for channel in range(3):
        mask_rgb[:, :, channel] = (mask * color[channel]).astype('int')
    return mask_rgb


def painter(img1, img2, alpha2):
    return (img1.astype('float') * (1 - alpha2) + img2.astype('float') * alpha2).astype('uint8')


def get8n(point, shape):

    neighbors = []
    y, x = point
    shape_x = shape[1] - 1
    shape_y = shape[0] - 1
    points = [[-1, -1], [-1, 0], [-1, 1],
              [0, -1], [0, 1],
              [1, -1], [1, 0], [1, 1]]

    for y1, x1 in points:
        x2 = x + x1
        y2 = y + y1
        if 0 < x2 < shape_x and 0 < y2 < shape_y:
            neighbors.append((y2, x2))

    return neighbors


def region_growing(img, origin):
    res = np.zeros(shape=img.shape, dtype=img.dtype)
    pending = [origin[::-1]]
    processed = set()

    while len(pending) > 0:

        point = pending.pop(0)
        res[point] = 1

        for p in get8n(point, img.shape):
            if p not in processed and img[point]:
                processed.add(p)
                pending.append(p)

    return res


def draw_figure(canvas, figure, tk_agg):
    delete_figure_agg(tk_agg)
    tk_agg = FigureCanvasTkAgg(figure, canvas)
    tk_agg.draw()
    tk_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return tk_agg


def delete_figure_agg(tk_agg):
    if tk_agg is not None:
        tk_agg.get_tk_widget().forget()
        plt.close('all')
