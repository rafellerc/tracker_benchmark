from collections import OrderedDict
# from config import *


class Sequence:
    """ This class contains the information for a single Sequence.

    Atributes:
        name: The name of the sequence. Ex: 'Basketball'
        path: The full path to the img/ folder inside the sequence's folder.
        startFrame: The number of the first frame of the video. Counting starts on 1.
        endFrame: The last frame of the video.
        attributes: The OTB attributes that apply to the sequence. In [IV, SV,
            OCC, DEF, MB, FM, IPR, OPR, OV, BC, LR]
        nz: (Apparently) it is the number of digits in each frame's name. For
            example, if the first file is 0001.jpg, 'nz' is 4
        ext: The extension of the file, normally jpg or png.
        imgFormat: The file extension for the images on the sequence
        gtRect: The list of all ground truth bounding boxes. Each bounding box
            is itself a list with 4 integers,
        init_rect: The initial bounding box of the target

    """

    def __init__(self, name, path, startFrame, endFrame, attributes, 
                 nz, ext, imgFormat, gtRect, init_rect):
        self.name = name
        self.path = path
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.attributes = attributes
        self.nz = nz
        self.ext = ext
        self.imgFormat = imgFormat
        self.gtRect = gtRect
        self.init_rect = init_rect
        self.__dict__ = OrderedDict([
            ('name', self.name),
            ('path', self.path),
            ('startFrame', self.startFrame),
            ('endFrame', self.endFrame),
            ('attributes', self.attributes),
            ('nz', self.nz),
            ('ext', self.ext),
            ('imgFormat', self.imgFormat),
            ('init_rect', self.init_rect),
            ('gtRect', self.gtRect)])
