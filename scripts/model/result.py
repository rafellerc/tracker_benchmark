from collections import OrderedDict
# from config import *


class Result:
    """ The class that summarizes the results of a tracker in a given sequence.
    The results are the collection of estimated bounding boxes for each one of
    the sequence's frames. It does not contain yet the comparison with the
    ground truth.

    Attributes:
        tracker: (str) The name of the tracker being used.
        seqName: (str) The name of the sequence in question.
        startFrame: (int) The first frame evaluated in the sequence. Indexing
            starts at 1.
        endFrame: (int) The last frame being evaluated.
        resType: (str) The format in which the results are given. 'rect' for
            example gathers the state in terms of the bounding box rectangles.
        evalType: (str) The evaluation protocol being used ['OPE', 'SRE', 'TRE']
        res: (list) A list with the results. In case of 'rect' resType, a list
            of 4 coordinate list of the BBs.
        fps: (float) The frame rate of the tracker. NOTE: Some of the trackers
            executables are not properly working with my system's clock (Ubuntu)
            and are giving nonsensical frame rates.
        shiftType:
        tmplsize:
    """
    def __init__(self, tracker, seqName, startFrame, endFrame, resType,
                 evalType, res, fps, shiftType=None, tmplsize=None):
        self.tracker = tracker
        self.seqName = seqName
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.resType = resType
        self.evalType = evalType
        self.res = res
        self.fps = fps
        self.shiftType = shiftType
        self.tmplsize = tmplsize

        self.__dict__ = OrderedDict([
            ('tracker', self.tracker),
            ('seqName', self.seqName),
            ('startFrame', self.startFrame),
            ('endFrame', self.endFrame),
            ('evalType', self.evalType),
            ('fps', self.fps),
            ('shiftType', self.shiftType),
            ('resType', self.resType),
            ('tmplsize', self.tmplsize),
            ('res', self.res)])

    def refresh_dict(self):
        self.__dict__ = OrderedDict([
            ('tracker', self.tracker),
            ('seqName', self.seqName),
            ('startFrame', self.startFrame),
            ('endFrame', self.endFrame),
            ('evalType', self.evalType),
            ('fps', self.fps),
            ('shiftType', self.shiftType),
            ('resType', self.resType),
            ('tmplsize', self.tmplsize),
            ('res', self.res)])
