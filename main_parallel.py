from heft import HEFT
from randomHEFT import randomHEFT
from ipeft import IPEFT
from read_dag import read_dag

from os import cpu_count
from itertools import product
import pandas as pd
import pickle
import multiprocessing as mp
from glob import glob
import warnings
import logging

warnings.filterwarnings('ignore',category=RuntimeWarning)
logging.basicConfig(filename="Error.log", level=logging.DEBUG)

def solve(tuple_val):
    idx,filename = tuple_val
    print("Evaluating {}".format(idx))
    val = filename.split('/')[1].split('.dot')[0].split('_')
    ccr = [0.1, 0.25, 0.5, 0.8, 1, 2, 5, 8, 10, 15, 20, 25, 30]
    b = [0.1, 0.2, 0.5, 0.75, 1, 2]
    p = [4,8,16,32]
    param = dict(zip(keys, val))
    result = []
    for v2 in product(*[ccr, b, p]):
        param.update(dict(zip(['ccr','b','p'], v2)))

        for _ in range(n_trials):
            try:
                inputs = read_dag(filename, p=param['p'], b=param['b'], ccr=param['ccr'])
                param['makespan_HEFT'] = HEFT(input_list=inputs).makespan
                param['makespan_prop'] = randomHEFT(input_list=inputs).makespan
                param['makespan_IPEFT'] = IPEFT(input_list=inputs).makespan
                result.append(param.copy())
            except:
                logging.error("Error occured", exc_info=True)
                msg = 'filename: {}, ccr: {}, b: {}, n_nodes: {}, p: {}\ncomp_matrix:\n{} adj_matrix:\n{}'.format(
                    filename, param['ccr'], param['b'], inputs[0], inputs[1], inputs[2], inputs[3])
                logging.info(msg)
                print("Error! Info logged")
    
    return result


# n_trials = 5
# minalpha = 20
# maxalpha = 150
# n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400]
# fat = [0.1, 0.4, 0.8]
# density = [0.2, 0.8]
# regularity = [0.2, 0.8]
# jump = [1,2,4]
# ccr = [0.1, 0.25, 0.5, 0.8, 1, 2, 5, 8, 10, 15, 20, 25, 30]
# b = [0.1, 0.2, 0.5, 0.75, 1, 2]
# p = [4,8,16,32]

n_trials = 2


keys = ['n', 'fat', 'density', 'regularity', 'jump']

filenames = glob('dag/*.dot')

pool = mp.Pool(cpu_count())
print('Using {} cores'.format(cpu_count()))

columns = ['n', 'fat', 'density', 'regularity', 'jump', 'ccr','b','p', 'makespan_HEFT', 'makespan_prop', 'makespan_IPEFT']
data = []
chunk_size = len(filenames)//10
for i in range(10):
    if i==9:
        result_list = pool.map(solve, enumerate(filenames[i*chunk_size:]))
    else:
        result_list = pool.map(solve, enumerate(filenames[i*chunk_size:(i+1)*chunk_size]))
    data.extend([result for sublist in result_list for result in sublist])
    df = pd.DataFrame(data)
    with open('data.pkl', 'wb') as handle:
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Data saved!")