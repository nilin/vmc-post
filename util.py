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

def getruns(*path):
    return {root:getconfig(root)['notes'] for root,dirs,files in os.walk(os.path.join(*path)) if 'config.json' in files}

def sortruns(runs):
    return dict(sorted(runs.items(),key=lambda a:a[1]))

def getconfig(*path): 
    with open(os.path.join(*path,'config.json')) as f:
        return json.load(f)
    
def getnotes(*path):
    return getconfig(*path)['notes']
    
def getenergies(*path):
    return np.loadtxt(os.path.join(*path,'energy_noclip.txt'))
    
def getevalenergies(*path):
    return np.loadtxt(os.path.join(*path,'eval','energy.txt'))

def getevalenergy(*path):
    return np.loadtxt(os.path.join(*path,'eval','energy.txt'))[-10000:].mean()

def getvariances(*path):
    return np.loadtxt(os.path.join(*path,'variance.txt'))
    
def printnotes(runs):
    for r,n in runs.items():
        print(n)

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

def filter_notes(runs,regex):
    return {r:n for r,n in runs.items() if re.search(regex,n) is not None}

def filter_paths(runs,regex):
    return {r:n for r,n in runs.items() if re.search(regex,r) is not None}

def filter_configs(runs,property,regex):
    def getproperty(D,l):
        for key in l:
            if key in D:
                D=D[key]
            else:
                return None
        return D
    return {r:n for r,n in runs.items() if re.search(regex,getproperty(getconfig(r)[property])) is not None}

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
reference_energies['N']=-54.5879
reference_energies['O']=-75.065

def plotruns(logdir,runs,ref,smoothing=1000,cleannote=lambda s:s):
    for r,note in runs.items():
        c=get_optimizer_color(note)
        energies=getenergies(logdir,r)-ref
        energies=gausskernel(energies,smoothing)
        plt.plot(energies,label=cleannote(note),color=c)

# save

def savefig(*path):
    path=os.path.join(*path)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path),exist_ok=True)
    for suffix in ['.pdf']:
        plt.savefig(path+suffix,bbox_inches='tight')

optimizernames=['adam','kfac','minsr','proxsr']