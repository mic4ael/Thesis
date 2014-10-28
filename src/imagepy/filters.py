__author__ = 'mic4ael'

from .utils import check_is_image, get_image_size

import numpy as np


class Filter(object):
    divisor = 0
    mask = []

    @classmethod
    def apply_filter(cls, image):
        if check_is_image(image):
            width, height = get_image_size(image)
            result = np.zeros((height, width, 3), dtype=image.dtype)

            for y in range(5, height - 5):
                for x in range(5, width - 5):
                    conc_arr = cls._get_adjacent_pixels_arr(image, x, y)
                    dst_r, dst_g, dst_b = cls._get_dest_rgb(conc_arr)
                    result[y][x] = [dst_r, dst_g, dst_b]

            return result

        return None

    @classmethod
    def _get_adjacent_pixels_arr(cls, image, x, y):
        width, height = len(cls.mask[0]), len(cls.mask)
        return np.concatenate((image[y - ((height - 1) / 2)][x - ((width - 1) / 2):x + 1],
                               image[y][x - ((width - 1) / 2):x + 1],
                               image[y + ((height - 1) / 2)][x - ((width - 1) / 2):x + 1]))

    @classmethod
    def _get_dest_rgb(cls, arr):
        sum_f = lambda n, a: sum([i[n] for i in a])
        return (sum_f(0, arr) / cls.divisor,
                sum_f(1, arr) / cls.divisor,
                sum_f(2, arr) / cls.divisor)


class AverageFilter(Filter):
    divisor = 9
    mask = [[1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]]


class GaussianFilter(Filter):
    divisor = 16
    mask = [[1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]]


def average_filter(image):
    if check_is_image(image):
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