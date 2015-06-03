#define wrap(_x,_N) ((_x<0)? ((_x)+_N ): ((_x>=_N)?(_x-_N):_x))
#define squ(x) ((x)*(x))

for(int n =0; n < N; n++){{
    {FLOAT} px = POSITIONS2(n,0)/boxsize * {gridN1D:d} +{gridN1D:d}/2;
    {FLOAT} py = POSITIONS2(n,1)/boxsize * {gridN1D:d} +{gridN1D:d}/2;
    {FLOAT} pz = POSITIONS2(n,2)/boxsize * {gridN1D:d} +{gridN1D:d}/2;

    //round to nearest cell center (we offset the grid .5 so we can use  floor instead of round)
    int ix = floor(px+.5);
    int iy = floor(py+.5);
    int iz = floor(pz+.5);

    //calculate distance to cell center
    {FLOAT} dx = ix - px;
    {FLOAT} dy = iy - py;
    {FLOAT} dz = iz - pz;

    //find the tsc weights for each dimension
    {FLOAT} wx = .75 -       squ(dx);
    {FLOAT} wxm1 = .5 * squ(.5 + dx);
    {FLOAT} wxp1 = .5 * squ(.5 - dx);
    {FLOAT} wy = .75 -       squ(dy);
    {FLOAT} wym1 = .5 * squ(.5 + dy);
    {FLOAT} wyp1 = .5 * squ(.5 - dy);
    {FLOAT} wz = .75 -       squ(dz);
    {FLOAT} wzm1 = .5 * squ(.5 + dz);
    {FLOAT} wzp1 = .5 * squ(.5 - dz);


    //find the wrapped x,y,z grid locations of the points we need to     change
    int ixm1 =wrap(ix-1,{gridN1D:d});
    int iym1 =wrap(iy-1,{gridN1D:d});
    int izm1 =wrap(iz-1,{gridN1D:d});
    int ixw = wrap(ix,  {gridN1D:d});
    int iyw = wrap(iy,  {gridN1D:d});
    int izw = wrap(iz,  {gridN1D:d});
    int ixp1 =wrap(ix+1,{gridN1D:d});
    int iyp1 =wrap(iy+1,{gridN1D:d});
    int izp1 =wrap(iz+1,{gridN1D:d});

    //change the 27 cells that the cloud touches
    DENSITY3(ixm1,iym1,izm1) += wxm1*wym1*wzm1;
    DENSITY3(ixw, iym1,izm1) += wx  *wym1*wzm1;
    DENSITY3(ixp1,iym1,izm1) += wxp1*wym1*wzm1;

    DENSITY3(ixm1,iyw ,izm1) += wxm1*wy  *wzm1;
    DENSITY3(ixw, iyw ,izm1) += wx  *wy  *wzm1;
    DENSITY3(ixp1,iyw ,izm1) += wxp1*wy  *wzm1;

    DENSITY3(ixm1,iyp1,izm1) += wxm1*wyp1*wzm1;
    DENSITY3(ixw, iyp1,izm1) += wx  *wyp1*wzm1;
    DENSITY3(ixp1,iyp1,izm1) += wxp1*wyp1*wzm1;

    DENSITY3(ixm1,iym1,izw ) += wxm1*wym1*wz;
    DENSITY3(ixw, iym1,izw ) += wx  *wym1*wz;
    DENSITY3(ixp1,iym1,izw ) += wxp1*wym1*wz;

    DENSITY3(ixm1,iyw ,izw ) += wxm1*wy  *wz;
    DENSITY3(ixw, iyw ,izw ) += wx  *wy  *wz;
    DENSITY3(ixp1,iyw ,izw ) += wxp1*wy  *wz;

    DENSITY3(ixm1,iyp1,izw ) += wxm1*wyp1*wz;
    DENSITY3(ixw, iyp1,izw ) += wx  *wyp1*wz;
    DENSITY3(ixp1,iyp1,izw ) += wxp1*wyp1*wz;

    DENSITY3(ixm1,iym1,izp1) += wxm1*wym1*wzp1;
    DENSITY3(ixw, iym1,izp1) += wx  *wym1*wzp1;
    DENSITY3(ixp1,iym1,izp1) += wxp1*wym1*wzp1;

    DENSITY3(ixm1,iyw ,izp1) += wxm1*wy  *wzp1;
    DENSITY3(ixw, iyw ,izp1) += wx  *wy  *wzp1;
    DENSITY3(ixp1,iyw ,izp1) += wxp1*wy  *wzp1;

    DENSITY3(ixm1,iyp1,izp1) += wxm1*wyp1*wzp1;
    DENSITY3(ixw, iyp1,izp1) += wx  *wyp1*wzp1;
    DENSITY3(ixp1,iyp1,izp1) += wxp1*wyp1*wzp1;
}}
