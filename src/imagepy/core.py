from scipy import ndimage
from scipy import misc


class Image(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self._image_arr = ndimage.imread(file_path)

    @property
    def size(self):
        return self._image_arr.shape
