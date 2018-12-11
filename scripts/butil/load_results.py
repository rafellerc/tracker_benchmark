import os
import sys
import json

import config
from scripts.model.result import Result
from scripts.model.score import Score
# from config import *
# from scripts import *

##########DEBUG
import pdb


def save_seq_result(result):
    """ Saves the results of given tracker/sequence/evalType in the
    corresponding folder inside /results, as a .json file that contains all
    the basic information in the Result object.
    
    Args:
        result: A list containing the Result object. NOTE: Why a list with a
            single element?
    NOTE: As it currently stands, this function writes single list into the 
    .json file, not actually making use of the json structure.
    """
    tracker = result[0].tracker
    seqName = result[0].seqName
    evalType = result[0].evalType
    src = config.RESULT_SRC.format(evalType) + tracker
    if not os.path.exists(src):
        os.makedirs(src)
    try:
        string = json.dumps(result, default=lambda o: o.__dict__)
    except:
        print(map(type, result[0].__dict__.values()))
        sys.exit()
    fileName = src + '/{0}.json'.format(seqName)
    resultFile = open(fileName, 'w')
    resultFile.write(string)
    resultFile.close()


def save_scores(scoreList, testname=None):
    """ Saves the scores contained in the scoreList into a .json file inside
    the /scores folder.
    
    Args:
        scoreList: A list with Score objects.
    """
    tracker = scoreList[0].tracker
    evalType = scoreList[0].evalType
    trkSrc = config.RESULT_SRC.format(evalType) + tracker
    if testname is None:
        scoreSrc = trkSrc + '/scores'
    else:
        scoreSrc = trkSrc + '/scores_{0}'.format(testname)
    if not os.path.exists(scoreSrc):
        os.makedirs(scoreSrc)
    for score in scoreList:
        string = json.dumps(score, default=lambda o: o.__dict__)
        fileName = scoreSrc + '/{0}.json'.format(score.name)
        scoreFile = open(fileName, 'w')
        scoreFile.write(string)
        scoreFile.close()


def load_all_results(evalType):
    resultSRC = config.RESULT_SRC.format(evalType)
    trackers = os.listdir(resultSRC)
    resultList = dict()
    for tracker in trackers:
        results, attrs = load_result(evalType, tracker)
        resultList[tracker] = (results, attrs)

    return resultList


def load_result(evalType, tracker):
    resultSRC = config.RESULT_SRC.format(evalType)
    print('Loading \'{0}\'...'.format(tracker))
    src = os.path.join(resultSRC, tracker)
    resultNames = os.listdir(src)
    attrs = []
    results = []
    for name in resultNames:
        if name == 'attributes':
            attrSrc = os.path.join(src, name)
            attrNames = os.listdir(attrSrc)
            for attrName in attrNames:
                attrFile = open(os.path.join(attrSrc, attrName))
                string = attrFile.read()
                j = json.loads(string)
                attr = Attribute(**j)
                attr.successRateList = map(lambda o:o*100, attr.successRateList)
                attrs.append(attr)
                attrs.sort()
        elif name.endswith('.json'):
            resultFile = open(os.path.join(src, name))
            string = resultFile.read()
            jsonList = json.loads(string)
            if type(jsonList) is list:
                results.append([Result(**j) for j in jsonList])
            elif type(jsonList) is dict:
                results.append([Result(**jsonList)])
    print('({0} seqs)'.format(len(resultNames) - 1))
    return results, attrs


def load_seq_result(evalType, tracker, sequence):
    resultSRC = config.RESULT_SRC.format(evalType)
    print('Loading {0}/{1}...'.format(tracker, sequence))
    src = os.path.join(resultSRC, tracker)
    result_src = os.path.join(src, sequence+'.json')
    resultFile = open(result_src)
    string = resultFile.read()
    # pdb.set_trace()
    jsonList = json.loads(string)
    if type(jsonList) is list:
        return [Result(**j) for j in jsonList]
    elif type(jsonList) is dict:
        return [Result(**jsonList)]
    return None


def load_all_scores(evalType, testname):
    resultSRC = config.RESULT_SRC.format(evalType)
    trackers = os.listdir(resultSRC)
    attrList = [(t, load_scores(evalType, t, testname)) for t in trackers]
    return attrList


def load_scores(evalType, tracker, testname):
    resultSRC = config.RESULT_SRC.format(evalType)
    print('Loading \'{0}\'...'.format(tracker))
    src = os.path.join(resultSRC, tracker+'/scores_{0}'.format(testname))
    attrNames = os.listdir(src)
    attrs = []
    for attrName in attrNames:
        attrFile = open(os.path.join(src, attrName))
        string = attrFile.read()
        j = json.loads(string)
        attr = Score(**j)
        attr.successRateList = map(lambda o: o*100, attr.successRateList)
        attrs.append(attr)
        attrs.sort()
    return attrs
