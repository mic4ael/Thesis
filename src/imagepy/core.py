from scipy import ndimage
from scipy.misc import imsave

from .utils import nearest_neighbours_scale


class Image(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self._image_arr = ndimage.imread(file_path)

    @property
    def size(self):
        return self._image_arr.shape[:2]

    def resize(self, size, new_file_name=None):
        self._image_arr = nearest_neighbours_scale(self._image_arr, size)
        if new_file_name:
            imsave(new_file_name, self._image_arr)

    def save(self, file_path=None):
        file_path_to_save = file_path or self.file_path
        imsave(file_path_to_save, self._image_arr)