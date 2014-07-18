from imagepy import Image
from imagepy.exceptions import FileNotFoundException
from nose.tools import raises


@raises(FileNotFoundException)
def create_image_wrong_path_test():
    m = Image('testPath.png')

def create_image_correct_rel_path_test():
    m = Image('test1.png')
    assert(m.name == 'test1.png')