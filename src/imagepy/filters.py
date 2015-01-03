__author__ = 'mic4ael'

from .operations import check_is_image, get_image_size, median, \
    assert_pixel_value

from .exceptions import WrongArgumentType

from itertools import chain

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
                    result[y, x] = cls._get_dest_rgb(neighbours)

            return result

        raise WrongArgumentType('Argument must be of image type')

    @classmethod
    def _get_adjacent_pixels_arr(cls, image, x, y):
        mask_width, mask_height = len(cls.mask[0]), len(cls.mask)
        x0, y0 = (x - (mask_width - 1) // 2), (y - (mask_height - 1) // 2)
        ret = None
        for i in range(mask_height):
            neighbours = image[y0 + i][x0:x0 + mask_width]
            if ret is not None:
                ret = np.concatenate((ret, neighbours))
            else:
                ret = neighbours

        return ret

    @classmethod
    def _get_dest_rgb(cls, image_arr):
        mask = list(chain.from_iterable(cls.mask))
        sum_f = lambda n: sum([val[n] * mask[index] for index, val in enumerate(image_arr)])
        return [assert_pixel_value(sum_f(index) // cls.divisor) for index in range(3)]


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


class SharpeningFilter(Filter):
    divisor = 3
    mask = [[0, -2, 0],
            [-2, 11, -2],
            [0, -2, 0]]


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


__all__ = [str(element) for element in dir() if element.endswith('Filter')]