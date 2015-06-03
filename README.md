# loom
Python package for binning 3d data, computing fast histograms, and calculating powerspectra.


Requires:
    *python 2.7 or higher
    *numpy
    *scipy
    *gcc

Recommended:
    *icc
    *Intel TBB
    *numpy/scipy compiled with intel compilers


Installation:
    Unpack and put loom directory in a place in your python path, e.g. /usr/local/lib/python2.7/site-packages/. Execute loom.Test.run(). 

    Loom will attemp to detect your configuration and set its config files accordingly. You can re-run this process by running python loom/Configure.py, or by deleting the generated config.ini.


Configuration:
    To change loom's configuration from the automatically detected one, modify config.ini in the loom directory. Keywords in the file will be passed to numpy's distutils when building the c sources. 

Using loom:

    **loom.Binning**

    Module for binning a set of three dimensional points onto a grid. There is one method:

    
    Binning.Bin(positions, gridN1d, boxsize = 1.0, dt = np.float64(), method = "tsc", rfft=False)

    positions:
    The points to be binned. A (n,3) numpy.ndarray of any data type that c will implicitly cast to dt.

    gridN1d:
    The size of one edge of the cubic grid to bin data to. Positive Integer.

    dt:
    A numpy.dtype to use for the output density array. Should usually be np.float64() or np.float32()

    method:
    The name of the  binning method to use. Currently only Triangular Shaped Cloud ("tsc") is supported.

    Eventual types will include:
    "ngp": Nearest grid point. 0th order binning kernel.
    "cic": Cloud in cell. 1st order binning kernel.
    "tsc": Triagular shaped cloud. 2nd order binning kernel.
        And possibly others if I have need of them or by request. 

    rfft:
    Whether to pad the output density array for in place real-to-complex fourier transforms. Useful if you are going to find the power spectrum of the density. Avoid unless you know what you are doing. 


    **loom.Histogram**
    Module for computing fast, low-overhead weighted and unweighted histograms.

    Histogram.Histogram( data, bins, no_copy=False):
    Returns the unweighted histogram of the flattened ndarray data. 

    data:
    Input nd array

    bins:
    array of bin edges to bin the data in to. For n bins, bins should have length n+1

    no_copy:
    Whether to make a copy of the data before computing the histogram. If true, data will be modified durring the calculation. Use this if memory is constrained and you will not perform further operations on data

    returns:
        bin_counts: The number of counts in the corresponding bin
        bins:The bins passed initially. Used to provide drop-in compatibility with numpy.hist

    Histogram.HistogramWeighted( data, bins, weights, sidx=None, no_copy = False):
    Computes the histogram of data into bins weighted by weights. All identicaly named arguments and returns behave as above.

    weights:
    An nd-array of the same type and shape as data containing the weight for each element.

    sidx:
        The permutation of indices that will sort data. Is created if not passed, and returned with results. Since running histograms on the same data with different weights will produce identical versions of this, you can pass one from a previous call of HistogramWeighted to avoid recomputing it. Otherwise should be avoided

    returns:
    bin_counts
    bins
    sidx:
    See description under arguments


