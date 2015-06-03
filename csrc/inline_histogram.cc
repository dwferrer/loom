//fast c based histogram code for generating the 1-d histogram of an array destructively. Requires Intel's tbb to be included and linked seperately, along with std::algorithm



{FLOAT} * c_data =  data;//({FLOAT} *)  PyArray_DATA(PyArray_GETCONTIGUOUS(data));

unsigned long long int count = 1;

for(int d = 0; d < Ddata; d++) count*=Ndata[d];

//{FLOAT} * data = ({FLOAT} *)  PyArray_DATA((PyArrayObject *)c_data);

#ifdef HAS_TBB
tbb::parallel_sort(data,data+count);
#else
std::sort(data,data+count);
#endif

{FLOAT} * cbins = bins;

double * counts = bincounts;

int nbins = Nbins [0] -1;



#pragma omp parallel for schedule(dynamic,1)
for( int b = 0; b < nbins; b++){{
    {FLOAT} * p_low = std::lower_bound(data,data+count,bins[b]);
    {FLOAT} * p_high;
    if(b <nbins-1)
        p_high = std::lower_bound(data,data+count,bins[b+1]);
    else
        p_high = std::upper_bound(data,data+count,bins[b+1]);

    long long unsigned int b_low =  p_low - data;
    long long unsigned int b_high = p_high -data;
    
    double bincount = b_high - b_low;
    counts[b] += bincount;
}}





