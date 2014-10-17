__author__ = 'mic4ael'

from .utils import check_image, get_image_size

import numpy as np


def median_filter(image):
    if check_image(image):
        width, height = get_image_size(image)
        result = np.zeros((height, width, 3), dtype=image.dtype)
        for y in range(4, height - 3):
            for x in range(4, width - 3):
                conc_arr = np.concatenate((image[y - 1][x:x + 3],
                                           image[y][x:x + 3],
                                           image[y + 1][x:x + 3]))
                dst_r = sum([i[0] for i in conc_arr]) / 9
                dst_g = sum([i[1] for i in conc_arr]) / 9
                dst_b = sum([i[2] for i in conc_arr]) / 9
                result[y][x] = [dst_r, dst_g, dst_b]
                
        return result