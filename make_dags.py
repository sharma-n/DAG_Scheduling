from os import system
from itertools import product

minalpha = 20
maxalpha = 50
n = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 250, 300, 350, 400]
fat = [0.1, 0.4, 0.8]
density = [0.2, 0.8]
regularity = [0.2, 0.8]
jump = [1,2,4]

keys = ['n', 'fat', 'density', 'regularity', 'jump']
values = [n, fat, density, regularity, jump]

for v in product(*values):
    param = dict(zip(keys, v))
    filename = 'dag/{}_{}_{}_{}_{}.dot'.format(param['n'],
        param['fat'],
        param['density'],
        param['regularity'],
        param['jump'])
    param = dict(zip(keys, v))
    system("daggen-master/daggen -n {} --fat {} --density {} --regular {} --jump {} --minalpha {} --maxalpha {} --dot -o {} >/dev/null 2>&1".format(
        param['n'],
        param['fat'],
        param['density'],
        param['regularity'],
        param['jump'],
        minalpha,
        maxalpha,
        filename
    ))