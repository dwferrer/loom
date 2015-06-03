#!/usr/bin/python

import numpy as np
import scipy.weave
from scipy.weave.converters import c_spec
import os

import Configuration

loompath = os.path.dirname(__file__)

def argsort(data,no_copy=False):
    if not no_copy:
        data = data.copy()
    codefile = open(loompath+"/csrc/argsort.cc","r")
    code = codefile.read().format(FLOAT = c_spec.num_to_c_types[data.dtype.char])
    codefile.close()

    auxcodefile = open(loompath+"/csrc/weighted_histogram_aux.cc","r")
    auxcode = auxcodefile.read().format(FLOAT = c_spec.num_to_c_types[data.dtype.char])
    auxcodefile.close()

    idx = np.ascontiguousarray(np.arange(data.size,dtype = np.uint64))

    Configuration.weave(code,
            ["data","idx"],
            locals(),
            support_code=auxcode)
    return idx


def Histogram(data,bins,no_copy=False):
    bins = np.ascontiguousarray(bins,dtype = data.dtype)
    bincounts = np.ascontiguousarray(np.zeros(bins.shape[0] -1,dtype = np.float64))
    if no_copy:
        data = np.ascontiguousarray(np.ravel(data))
    else:
        data = np.ascontiguousarray(np.ravel(np.copy(data)))

    codefile = open(loompath+"/csrc/inline_histogram.cc","r")
    code = codefile.read().format(FLOAT = c_spec.num_to_c_types[data.dtype.char])
    codefile.close()
    Configuration.weave(code,
            ["bins","data","bincounts"],
            locals())
    return bincounts, bins

def HistogramWeighted(data,bins,weights,sidx=None,no_copy = False):
    bins = np.ascontiguousarray(bins,dtype = data.dtype)
    bincounts = np.ascontiguousarray(np.zeros(bins.shape[0] -1,dtype = np.float64))
    if no_copy:
        data = np.ravel(data)
        weights = np.ravel(weights)
    else:
        data = np.ravel(data.copy())
        weights = np.ravel(weights)

    if sidx is None:
        sidx = argsort(data,no_copy=True)
    data = np.ascontiguousarray(data[sidx])
    weights = np.ascontiguousarray(weights[sidx],dtype=data.dtype)

    codefile = open(loompath+"/csrc/inline_histogram_weighted.cc","r")
    code = codefile.read().format(FLOAT = c_spec.num_to_c_types[data.dtype.char])
    codefile.close()

    auxcodefile = open(loompath+"/csrc/weighted_histogram_aux.cc","r")
    auxcode = auxcodefile.read().format(FLOAT = c_spec.num_to_c_types[data.dtype.char])
    auxcodefile.close()

    Configuration.weave(code,
            ["bins","data","weights","bincounts"],
            locals(),
            support_code=auxcode)
    return bincounts, bins,sidx
