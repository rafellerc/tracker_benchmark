import getopt
import sys
import os

import numpy as np
from PIL import Image
from config import *
# from scripts import *

from scripts.model.result import Result
from scripts.model.sequence import Sequence
from scripts.butil import seq_config, eval_results, load_results, extra
from scripts.bscripts import *

#######################
####################### DEBUGGER - REMEMBER TO REMOVE
#######################
import pdb
######################
######################


def main(argv):
    trackers = os.listdir(TRACKER_SRC)
    evalTypes = ['OPE', 'SRE', 'TRE']
    loadSeqs = 'TB50'
    seqs = []
    try:
        opts, args = getopt.getopt(argv, "ht:e:s:", ["tracker=", "evaltype=",
                                                     "sequence="])
    except getopt.GetoptError:
        print('usage : run_trackers.py -t <trackers> -s <sequences>',
              '-e <evaltypes>')
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            print('usage : run_trackers.py -t <trackers> -s <sequences>',
                  '-e <evaltypes>')
            sys.exit(0)
        elif opt in ("-t", "--tracker"):
            trackers = [x.strip() for x in arg.split(',')]
            # trackers = [arg]
        elif opt in ("-s", "--sequence"):
            loadSeqs = arg
            if loadSeqs != 'All' and loadSeqs != 'all' and loadSeqs != 'tb50' \
               and loadSeqs != 'tb100' and loadSeqs != 'cvpr13':
                loadSeqs = [x.strip() for x in arg.split(',')]
        elif opt in ("-e", "--evaltype"):
            evalTypes = [x.strip() for x in arg.split(',')]
            # evalTypes = [arg]

    if SETUP_SEQ:
        print('Setup sequences ...')
        seq_config.setup_seqs(loadSeqs)
    if sys.version_info >= (3, 0):
        testname = input("Input Test name : ")
    else:
        testname = raw_input("Input Test name : ")
    print('Starting benchmark for {0} trackers, evalTypes : {1}'.format(
          len(trackers), evalTypes))
    for evalType in evalTypes:
        seqNames = seq_config.get_seq_names(loadSeqs)
        seqs = seq_config.load_seq_configs(seqNames)
        trackerResults = run_trackers(
            trackers, seqs, evalType, shiftTypeSet)
        for tracker in trackers:
            results = trackerResults[tracker]
            if len(results) > 0:
                evalResults, attrList = eval_results.calc_result(tracker,
                                                          seqs, results,
                                                          evalType)
                print("Result of Sequences\t -- '{0}'".format(tracker))
                for seq in seqs:
                    try:
                        print("\t\'{0}\'{1}".format(
                            seq.name, " "*(12 - len(seq.name))))
                        print("\taveCoverage : {0:.3f}%".format(
                            sum(seq.aveCoverage)/len(seq.aveCoverage) * 100))
                        print("\taveErrCenter : {0:.3f}".format(
                            sum(seq.aveErrCenter)/len(seq.aveErrCenter)))
                    except:
                        print("\t\'{0}\'  ERROR!!".format(seq.name))

                print("Result of attributes\t -- '{0}'".format(tracker))
                for attr in attrList:
                    print("\t\'{0}\'".format(attr.name))
                    print("\toverlap : {0:02.1f}%".format(attr.overlap))
                    print("\tfailures : {0:.1f}".format(attr.error))

                if SAVE_RESULT:
                    load_results.save_scores(attrList, testname)


def run_trackers(trackers, seqs, evalType, shiftTypeSet):
    """ Runs a set of trackers in a set of sequences according to the given
    evaluation protocol (evalType).

    Args:
        trackers: A list with all the names of trackers to be used.
        seqs: A list with all the sequences to be evaluated in.
        evalType: The evaluation protocol ['OPE', 'SRE' or 'TRE']
        shiftTypeSet: The list with the shifts to be applied in the SRE
            protocol. Generally defined in the config file.

    Returns:
        trackerResults:

    """
    # Get the path to the results folder for the current evalType
    tmpRes_path = RESULT_SRC.format('tmp/{0}/'.format(evalType))
    if not os.path.exists(tmpRes_path):
        os.makedirs(tmpRes_path)

    numSeq = len(seqs)
    numTrk = len(trackers)

    # print("Run trackers")
    # pdb.set_trace()
    trackerResults = dict((t, list()) for t in trackers)
    # for idxSeq in range(numSeq):
    for idxSeq, s in enumerate(seqs):
        # s = seqs[idxSeq]
        subSeqs, subAnno = seq_config.get_sub_seqs(s, 20.0, evalType)
        for idxTrk, t in enumerate(trackers):
            # t = trackers[idxTrk]
            if not os.path.exists(TRACKER_SRC + t):
                print('{0} does not exists'.format(t))
                sys.exit(1)
            if not OVERWRITE_RESULT:
                trk_src = os.path.join(RESULT_SRC.format(evalType), t)
                result_src = os.path.join(trk_src, s.name+'.json')
                # Checks if the result file already exists for the given tracker
                # and sequence. If it exists it loads it and exits the loop.
                if os.path.exists(result_src):
                    seqResults = load_results.load_seq_result(evalType, t, s.name)
                    trackerResults[t].append(seqResults)
                    continue
            seqResults = []
            seqLen = len(subSeqs)
            # print("Is this executing?")
            # pdb.set_trace()
            for idx in range(seqLen):
                print('{0}_{1}, {2}_{3}:{4}/{5} - {6}'.format(
                    idxTrk + 1, t, idxSeq + 1, s.name, idx + 1, seqLen,
                    evalType))
                rp = tmpRes_path + '_' + t + '_' + str(idx+1) + '/'
                if SAVE_IMAGE and not os.path.exists(rp):
                    os.makedirs(rp)
                subS = subSeqs[idx]
                subS.name = s.name + '_' + str(idx)
                    
                os.chdir(TRACKER_SRC + t)
                funcName = 'run_{0}(subS, rp, SAVE_IMAGE)'.format(t)
                try:
                    res = eval(funcName)
                except:
                    print('failed to execute {0} : {1}'.format(
                        t, sys.exc_info()))
                    os.chdir(WORKDIR)         
                    break
                os.chdir(WORKDIR)

                if evalType == 'SRE':
                    r = Result(t, s.name, subS.startFrame, subS.endFrame,
                               res['type'], evalType, res['res'], res['fps'],
                               shiftTypeSet[idx])
                else:
                    r = Result(t, s.name, subS.startFrame, subS.endFrame,
                               res['type'], evalType, res['res'], res['fps'],
                               None)
                try:
                    r.tmplsize = extra.d_to_f(res['tmplsize'][0])
                except:
                    pass
                # print("What is r")
                # pdb.set_trace()
                r.refresh_dict()
                seqResults.append(r)
            # end for subseqs
            if SAVE_RESULT:
                # print("Main file trace")
                # pdb.set_trace()
                load_results.save_seq_result(seqResults)

            trackerResults[t].append(seqResults)
        # end for tracker
    # end for allseqs
    return trackerResults

if __name__ == "__main__":
    main(sys.argv[1:])
