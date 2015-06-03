#!/usr/bin/python

import numpy as np
import scipy.weave
from scipy.weave.converters import c_spec


import Configuration

#bin a set of positions  on to a three dimensional grid of size gridN1d.
#NOTE: The resulting density array is padded to allow in-place r2c/c2r transforms
#       This should be transparent to the user unless she wishes to access it
#       in a flattened manner.
def Bin(positions,gridN1d,boxsize = 1.0,dt = np.float64(),method = "tsc",rfft=False):
    assert(method == "tsc","Other binning methods have not been added. Please request them or check back later")
    positions = positions[:,0:3]
    positions = np.ascontiguousarray(positions,dtype=dt)
    N = positions.shape[0]

    #we pad the array to make in place rfft based convolutions easier

    density = np.ascontiguousarray(np.zeros((gridN1d,gridN1d,2*(gridN1d/2+1)),dtype = dt))

    codefile = open(Configuration.loompath +"/csrc/inline_tsc.cc","rb")
    tsc_code = codefile.read().format(FLOAT=c_spec.num_to_c_types[dt.dtype.char],gridN1D = gridN1d)
    codefile.close()

    Configuration.weave(tsc_code,
            ["positions","N","density","boxsize"],
            locals())
    if rfft:
        return density
    else:
        return density[:gridN1d,:gridN1d,gridN1d]







