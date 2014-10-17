from scipy import ndimage, zeros
from scipy.misc import imsave

from .utils import nearest_neighbours_scale, rotate_image, get_image_size, check_image
from .filters import median_filter

from imagepy.exceptions import WrongArgumentType


class Image(object):
    def __init__(self, file_path=None, file_array=None):
        self.file_path = None
        self._image_arr = None
        if file_path:
            self.file_path = file_path
            self._image_arr = ndimage.imread(file_path)

        if file_array is not None:
            if check_image(file_array):
                self._image_arr = file_array
            else:
                raise WrongArgumentType('File array if provided must be of ndarray type')

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

    def median_filter(self):
        self._image_arr = median_filter(self._image_arr)

    def save(self, file_path=None):
        file_path_to_save = file_path or self.file_path
        imsave(file_path_to_save, self._image_arr)

    @classmethod
    def new(cls, size):
        def check_arguments(f_args):
            if any([True for arg in f_args if arg <= 0]):
                raise WrongArgumentType('One of provided arguments is negative!')

        check_arguments(size)
        img = zeros(size[::-1] + (3, ))
        return Image(file_array=img)

    @classmethod
    def copy(cls, image_arr):
        return Image(file_array=image_arr)

    @property
    def size(self):
        return self.width, self.height