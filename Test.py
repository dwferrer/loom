#!/usr/bin/python

import numpy as np
import scipy.special
import scipy.optimize

import Histogram
import Binning

#import matplotlib.pyplot as p

def TestHistogram():
    print("Testing Histogram.Histogram...")
    data = np.concatenate((np.linspace(0.0,10,20),np.linspace(0.0,10.0,5)))
    bins = np.linspace(0,10,7)

    OurCount = Histogram.Histogram(data,bins)[0]
    NPCount = np.histogram(data,bins)[0]
    np.testing.assert_array_almost_equal_nulp(OurCount,NPCount)
    print("\tPassed")

def TestHistogramWeighted():
    print("Testing Histogram.HistogramWeighted...")
    data = np.concatenate((np.linspace(0.0,10,20),np.linspace(0.0,10.0,5)))
    bins = np.linspace(0,10,7)
    weights = np.random.rand(data.shape[0])

    OurCount = Histogram.HistogramWeighted(data,bins,weights)[0]
    NPCount = np.histogram(data,bins,weights=weights)[0]
    np.testing.assert_array_almost_equal_nulp(OurCount,NPCount,nulp=10)
    print("\tPassed")

mu = 1.0

def gauss(x,sigma):
    return  1/(sigma*np.sqrt(2*np.pi)) *np.exp(-(x-mu)**2 /(2*sigma**2))

def TestBin():
    global mu

    print("Testing Binning.Bin")
    Ns = 128**3
    Ng = 128
    positions = np.random.rand(Ns,3)
    density = Binning.Bin(positions,Ng)[:Ng,:Ng,:Ng]
    np.testing.assert_almost_equal(density.sum(),Ns,err_msg="Total count not conserved.")
    print("\tPassed.")


    #Ng = Ng**3
    #nbins = 200
    #bins = np.linspace(density.min(),density.max(),nbins+1)
    #density_dist = Histogram.Histogram(density,bins)[0]/Ng
    #bin_center = (bins[1:]+bins[:-1])/2
    #bin_width = (bins[1:]-bins[:-1])
    #density_dist /=bin_width
    #mu = (1.0*Ns)/Ng
    #sigma = np.sqrt(mu)
    #popt,pcov = scipy.optimize.curve_fit(gauss,bin_center,density_dist,p0=sigma)

    #model_dist = gauss(bin_center,*popt)
    #chi2 = np.sum( ((density_dist-model_dist)/model_dist)**2)
    #print("Reduced Chi^2: " + str(chi2))
    #p.plot(bin_center,density_dist)

    #p.plot(bin_center,model_dist,"--")
    #p.show()

def run():
    TestHistogram()
    TestHistogramWeighted()
    TestBin()

if __name__ == "__main__":
    run()
