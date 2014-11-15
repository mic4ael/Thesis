__author__ = 'mic4ael'

from .utils import check_is_image, get_image_size, median
from .exceptions import WrongArgumentType

import numpy as np


class Filter(object):
    divisor = 0
    mask = [[1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]]

    @classmethod
    def apply_filter(cls, image):
        if check_is_image(image):
            width, height = get_image_size(image)
            result = np.zeros((height, width, 3), dtype=image.dtype)

            for y in range(len(cls.mask), height - len(cls.mask)):
                for x in range(len(cls.mask[0]), width - len(cls.mask[0])):
                    neighbours = cls._get_adjacent_pixels_arr(image, x, y)
                    dst_r, dst_g, dst_b = cls._get_dest_rgb(neighbours)
                    result[y][x] = [dst_r, dst_g, dst_b]

            return result

        raise WrongArgumentType('Argument must be of image type')

    @classmethod
    def _get_adjacent_pixels_arr(cls, image, x, y):
        mask_width, mask_height = len(cls.mask[0]), len(cls.mask)
        x0, y0 = (x - (mask_width - 1) / 2), (y - (mask_height - 1) / 2)
        ret = None
        for i in range(mask_height):
            neighbours = image[y0 + i][x0:x0 + mask_width]
            if ret is not None:
                ret = np.concatenate((ret, neighbours))
            else:
                ret = neighbours

        return ret

    @classmethod
    def _get_dest_rgb(cls, arr):
        sum_f = lambda n: sum([i[n] for i in arr])
        return tuple([sum_f(index) / cls.divisor for index in range(3)])


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


class SquareFilter(Filter):
    divisor = 25
    mask = [[1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1]]


class MedianFilter(Filter):
    @classmethod
    def _get_dest_rgb(cls, neighbours):
        return tuple([median(i) for i in list(zip(*neighbours))])


class MaxFilter(Filter):
    @classmethod
    def _get_dest_rgb(cls, neighbours):
        return tuple([max(i) for i in list(zip(*neighbours))])


class MinFilter(Filter):
    @classmethod
    def _get_dest_rgb(cls, neighbours):
        return tuple([min(i) for i in list(zip(*neighbours))])
