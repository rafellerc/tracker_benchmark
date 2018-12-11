from config import *
import scripts.butil
def run_L1APG(seq, rp, bSaveImage):
    global m
    if m is None:
        print('Starting matlab engine...')
        m = matlab.engine.start_matlab()
    m.addpath(m.genpath('.', nargout=1), nargout=0)
    seq.init_rect = matlab.double(seq.init_rect)
    m.workspace['subS'] = seq.__dict__
    m.workspace['rp'] = os.path.abspath(rp)
    m.workspace['bSaveImage'] = bSaveImage
    func = 'run_L1APG(subS, rp, bSaveImage);'
    res = m.eval(func, nargout=1)
    res['res'] = scripts.butil.matlab_double_to_py_float(res['res'])
    # m.quit()
    return res
