from scipy import ndimage, zeros
from scipy.misc import imsave
from scipy.ndimage.measurements import histogram

from .utils import nearest_neighbours_scale, rotate_image, \
    get_image_size, check_is_image, vertical_reflection, \
    horizontal_reflection, rgb_split, invert_image, image_gray_scale,\
    image_thresholding, add_gaussian_noise, salt_and_pepper_noise

from imagepy.exceptions import WrongArgumentType


class Image(object):
    def __init__(self, file_path=None, file_array=None):
        self.file_path = None
        self._image_arr = None

        if file_path:
            self.file_path = file_path
            self._image_arr = ndimage.imread(file_path, mode='RGB')

        if file_array is not None:
            if check_is_image(file_array):
                self._image_arr = file_array
            else:
                raise WrongArgumentType('File array if provided must be of ndarray type')

        self.r, self.g, self.b = rgb_split(self._image_arr)
        # ndimage.shape returns tuple where first element is height, then width
        if self._image_arr is not None:
            self.width, self.height = get_image_size(self._image_arr)

    def resize(self, size):
        self._image_arr = nearest_neighbours_scale(self._image_arr, size)
        self.width, self.height = size

    def rotate(self, angle):
        self._image_arr = rotate_image(self._image_arr, angle)

    def thumbnail(self, size):
        if (isinstance(size, (tuple, list)) and len(size) != 2) \
                or (not isinstance(size, (tuple, list))):
            raise WrongArgumentType('Argument must be iterable and its size must be equal 2')
        width, height = size
        if width < self.width and height < self.width:
            self.width, self.height = size
            self._image_arr = nearest_neighbours_scale(self._image_arr, size)

    def apply_filter(self, filter_cls):
        self._image_arr = filter_cls.apply_filter(self._image_arr)

    def save(self, file_path=None):
        file_path_to_save = file_path or self.file_path
        imsave(file_path_to_save, self._image_arr)

    def horizontal_reflection(self):
        self._image_arr = horizontal_reflection(self._image_arr)

    def vertical_reflection(self):
        self._image_arr = vertical_reflection(self._image_arr)

    def get_pixel_at(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            raise Exception

        return self._image_arr[y][x]

    def histogram(self):
        return histogram(self._image_arr, 0, 1, 50)

    def invert(self):
        invert_image(self._image_arr)

    def gray_scale(self):
        image_gray_scale(self._image_arr)

    def gaussian_noise(self, mean=6, variance=36):
        self._image_arr = add_gaussian_noise(self._image_arr, mean, variance)

    def salt_and_pepper_noise(self, min_v=0, max_v=255):
        image_gray_scale(self._image_arr)
        salt_and_pepper_noise(self._image_arr, min_v, max_v)

    def point_operation(self, func):
        image_gray_scale(self._image_arr)
        for y in range(self.height):
            for x in range(self.width):
                pixel = self._image_arr[y][x]
                new_val = func(pixel[0])
                self._image_arr[y][x] = [new_val for i in range(3)]

    def threshold(self, threshold):
        image_gray_scale(self._image_arr)
        image_thresholding(self._image_arr, threshold)

    @classmethod
    def new(cls, size):
        def check_arguments(f_args):
            if any([True for arg in f_args if arg <= 0]):
                raise WrongArgumentType('One of provided arguments is <= 0!')

        check_arguments(size)
        img = zeros(size[::-1] + (3, ))
        return Image(file_array=img)

    @classmethod
    def copy(cls, image_arr):
        return Image(file_array=image_arr)

    @property
    def size(self):
        return self.width, self.height

    @property
    def rgb_channels(self):
        return self.r, self.g, self.b
