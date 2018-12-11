import os

import copy
import numpy as np
from config import SEQ_SRC, INIT_OMIT_FILE, USE_INIT_OMIT

"""OBSERVATION: It is pretty confusing to keep adding new attributes to the
Sequence class on a whim like this, besides not being able to rely on the class
definition to define the interface, it also keeps some of the attributes
unchanged even though the values no longer make sense (e.g. the 'gtRect' 
attribute in the subSeq's).
"""


def split_seq_TRE(seq, segNum, rect_anno):
    """
    Splits a sequence into (segNum) subsequences, following the TRE protocol,
    that is, the first subsequence is the sequence itself, and each new
    subsequence starts at a later frame and goes until the end of the sequence.

    Args:
        seg: The Sequence object of the current sequence
        segNum: The number of segments the sequence is to be divided into.
        rect_anno: The bounding boxes annotations list.
    
    Returns:
        subSeqs: A list of Sequence objects, each containing a subsequence of
            the original sequence. Each element doesn't follow completely the
            class prototype though, for example it simply copies the 'gtRect'
            info from the original seq (the gt information is stored in
            subAnno), and other fields are added, such as 'len', 'annoBegin' and
            's_frames'.
        subAnno: A list of the annotations for the subsequences in subSeqs.
    """
    # The minimum size of subsequence
    minNum = 20
    fileName = SEQ_SRC + seq.name + '/' + INIT_OMIT_FILE
    idxExclude = []
    # Somehow if there exists a 'init_omit.txt' file it excludes the frames 
    # contained in such file. But I've checked for all sequences in the /data
    # folder and no seq has any such file.
    if USE_INIT_OMIT and os.path.exists(fileName):
        idxExclude = np.loadtxt(fileName, dtype=int) - seq.startFrame + 1
        if not isinstance(idxExclude[0], np.ndarray):
            idxExclude = [idxExclude]

    # TODO see if it makes sense to use a list here instead of the original
    # iterator
    idx = list(range(1, seq.len + 1))

    for j in range(len(idxExclude)):
        begin = idxExclude[j][0] - 1
        end = idxExclude[j][1]
        idx[begin:end] = [0] * (end-begin)
    idx = [x for x in idx if x > 0]

    for i in range(len(idx)):
        r = rect_anno[idx[i] - 1]
        # My guess is that this removes any bounding boxes with negative or zero
        # valued coordinates. I don't know why we would remove the zero-valued
        # ones tho.
        if r[0] <= 0 or r[1] <= 0 or r[2] <= 0 or r[3] <= 0:
            # TODO set a print here to check if it ever enters this branch
            idx[i] = 0
    idx = [x for x in idx if x > 0]
    for i in reversed(range(len(idx))):
        if seq.len - idx[i] + 1 >= minNum:
            endSeg = idx[i]
            endSegIdx = i + 1
            break

    startFrIdxOne = np.floor(np.arange(1, endSegIdx, endSegIdx/(segNum-1)))
    startFrIdxOne = np.append(startFrIdxOne, endSegIdx)
    startFrIdxOne = [int(x) for x in startFrIdxOne]

    subAnno = []
    subSeqs = []

    for i in range(len(startFrIdxOne)):
        index = idx[startFrIdxOne[i] - 1] - 1
        subS = copy.deepcopy(seq)
        subS.startFrame = index + seq.startFrame
        subS.len = subS.endFrame - subS.startFrame + 1
        subS.annoBegin = seq.startFrame
        subS.init_rect = rect_anno[index]
        anno = rect_anno[index:]
        subS.s_frames = seq.s_frames[index:]
        subSeqs.append(subS)
        subAnno.append(anno)

    return subSeqs, subAnno
