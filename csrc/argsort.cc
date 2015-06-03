sarray = data;
size_t count = 1;
for(int d = 0; d < Ddata; d++) count*=Ndata[d];

#ifdef HAS_TBB
tbb::parallel_sort(idx,idx+count,comp);
#else
std::sort(idx,idx+count,comp);
#endif

