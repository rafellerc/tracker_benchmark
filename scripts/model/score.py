from collections import OrderedDict
from config import SEQ_SRC, ATTR_DESC_FILE


class Score:
    """ Class that stores the information of the scores obtained by a given
    tracker/sequence/evalType.

    Attributes:
        name: (str) The name of the sequence attribute in consideration. 'ALL'
            stands for the mean accross all attributes. Other attributes are 
            ['IV','OPR','SV','OCC','DEF','MB','FM','IPR','OV','BC','LR'].
        desc: (str) The string with the description of the current attribute.
        tracker: (str) The name of the tracker used.
        evalType: (str) The name of the evaluation protocol used.
        seqs: (str) A list with the sequences evaluated.
        overlapScores: (list) A list with the overlap (IOU) scores in each 
            sequence. The values are between 0 and 1.
        errorNum: (float) A list with the displacement error, that is, the
            average distance in pixels between the center of the estimated and
            ground truth bounding boxes.
        overlap: (float) The average overlap in percentage terms.
        error: (float) The average displacement error.
        successRateList: A list with the success rate (percentage of frames
            on which the error was lower than a threshold).
    """

    def __init__(self, name, desc, tracker=None, evalType=None, seqs=[],
                 overlapScores=[], errorNum=[], overlap=0, error=0,
                 successRateList=[]):
        self.name = name
        self.desc = desc
        self.tracker = tracker
        self.evalType = evalType
        self.seqs = seqs
        self.overlapScores = overlapScores
        self.errorNum = errorNum
        self.overlap = overlap
        self.error = error
        self.successRateList = successRateList

        self.__dict__ = OrderedDict([
            ('name', self.name),
            ('desc', self.desc),
            ('tracker', self.tracker),
            ('evalType', self.evalType),
            ('seqs', self.seqs),
            ('overlap', self.overlap),
            ('error', self.error),
            ('overlapScores', self.overlapScores),
            ('errorNum', self.errorNum),
            ('successRateList', self.successRateList)])

    def refresh_dict(self):
        self.__dict__ = OrderedDict([
            ('name', self.name),
            ('desc', self.desc),
            ('tracker', self.tracker),
            ('evalType', self.evalType),
            ('seqs', self.seqs),
            ('overlap', self.overlap),
            ('error', self.error),
            ('overlapScores', self.overlapScores),
            ('errorNum', self.errorNum),
            ('successRateList', self.successRateList)])

    def __lt__(self, other):
        return self.name < other.name

    @staticmethod
    def getScoreFromLine(line):
        # Input Example : "DEF  Deformation - non-rigid object deformation."
        attr = line.strip().split('\t')
        name = attr[0]
        desc = attr[1]
        return Score(name, desc)

##########################################################


def getScoreList():
    srcAttrFile = open(SEQ_SRC + ATTR_DESC_FILE)
    attrLines = srcAttrFile.readlines()
    attrList = []
    for line in attrLines:
        attr = Score.getScoreFromLine(line)
        attrList.append(attr)
    return attrList
