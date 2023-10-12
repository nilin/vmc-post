import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import json
import re

import os, json
import numpy as np
import re

# loading functions

def getconfig(*path): 
    try:
        with open(os.path.join(*path,'config.json')) as f:
            return json.load(f)
    except:
        return {"notes":""}
    
def getenergies(*path):
    with open(os.path.join(*path,'energy_noclip.txt'),'r') as f:
        return np.array([float(l) for l in f])
    
def getevalenergies(*path):
    with open(os.path.join(*path,'eval','energy.txt'),'r') as f:
        return np.array([float(l) for l in f])

def getevalenergy(*path):
    with open(os.path.join(*path,'eval','energy.txt'),'r') as f:
        return np.mean(np.array([float(l) for l in f])[-5000:])

#def getevalenergy(*path):
#    with open(os.path.join(*path,'eval','statistics.json'),'r') as f:
#        return float(json.load(f)['average'])

def getvariances(*path):
    with open(os.path.join(*path,'variance.txt'),'r') as f:
        return np.array([float(l) for l in f])
    

# defaults

#pick color based on notes
def get_optimizer_color(notes):
    if 'kfac' in notes:
        return 'b'
    if 'minsr' in notes:
        return 'r'
    if 'proxsr' in notes:
        return 'darkred'
    return 'k'

#how to display labels
def cleanlabel(name):
    name = re.sub(r"\(.*?\)|\[.*?\]", "", name)
    name = name.replace('_',' ')
    return name




"""requirements and exclusions for run names
reqs=[('good',),('new','recent')]
excl=['bad','outdated']
"""
def filter_runs(runs,reqs=None,excl=None):
    if reqs is None: reqs=[]
    if excl is None: excl=[]
    runs={r:n for r,n in runs.items() if all([any([option in n for option in req]) for req in reqs])}
    runs={r:n for r,n in runs.items() if all([not e in n for e in excl])}
    runs=dict(sorted(runs.items(),key=lambda a:a[1]))
    return runs

# processing

def gausskernel(y,smoothing=10):
    k=smoothing
    s=np.exp(-(np.arange(-k,k)/k)**2)
    s=s/np.sum(s)
    return np.convolve(y,s,mode='valid')

def variance(x):
    if len(x)==0: return 0
    return np.mean(np.array(x)**2)-np.mean(np.array(x))**2

# reference data

reference_energies=dict(
    LiH=-8.070548,
    # at 3.015 Bohr, https://pubs.aip.org/aip/jcp/article/134/6/064117/645489/Very-accurate-potential-energy-curve-of-the-LiH
    #
    #H4=-2.029502,
    # for single determinant
    #H4_single_det=-2.029502,
    H4=-2.034218,
    #H4=-2.04,
    # at 4.0 Bohr
    #
    C=-37.8450,
    #
    #
    N2=-109.2021
    #N2=-109.1827
    # 1 det
    #
    # Li2=
    # at 2.6730 Angstrom = 5.0512379 Bohr, https://cccbdb.nist.gov/exp2x.asp?casno=14452596
    #
)


# save

def savefig(*path):
    path=os.path.join(*path)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path),exist_ok=True)
    for suffix in ['.pdf']:
        plt.savefig(path+suffix,bbox_inches='tight')