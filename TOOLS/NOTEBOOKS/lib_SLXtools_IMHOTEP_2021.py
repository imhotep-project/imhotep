#!/usr/bin/env  python
#=======================================================================
"""
StepHANIE Leroux
Collection of customed  tools related to  IMHOTEP project
"""
#=======================================================================

## standart libraries
import os,sys
import numpy as np

# xarray
import xarray as xr

#scipy
import scipy.signal as sps
import scipy.linalg as spl


# plot
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.colors import from_levels_and_colors
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def saveplt(fig,diro,namo,dpifig=300):
    fig.savefig(diro+namo, facecolor=fig.get_facecolor(),
                edgecolor='none',dpi=dpifig,bbox_inches='tight', pad_inches=0)
    plt.close(fig) 
    
    
def addcolorbar(fig,cs,ax,levbounds,levincr=1,tformat="%.2f",tlabel='',shrink=0.45,facmul=1.,orientation='vertical',tc='k',loc='lower right',wth="15%",bbta=(0.08, -0.1,0.9,0.2)):
    lmin = levbounds[0]
    lmax = levbounds[1]
    incr = levbounds[2]
    levels = np.arange(lmin,lmax,incr)
    cblev = levels[::levincr]
    
    if orientation =='horizontal':
        axins1 = inset_axes(ax,
                        height=wth,  # height : 5%
                            width="50%",
                        bbox_to_anchor=bbta,
                        bbox_transform=ax.transAxes,
                        borderpad=0)

    if orientation =='vertical':
        axins1 = inset_axes(ax,
                        height="50%",  # height : 5%
                            width="2%",
                        loc='center left',
                       borderpad=2)

    cb = fig.colorbar(cs,cax=axins1,
                                    extend='both',                   
                                    ticks=cblev,
                                    spacing='uniform',
                                    orientation=orientation,
                                    )
    
    new_tickslabels = [tformat % i for i in cblev*facmul]
    cb.set_ticklabels(new_tickslabels)
    cb.ax.set_xticklabels(new_tickslabels, rotation=70,size=10,color=tc)
    cb.ax.tick_params(labelsize=10,color=tc) 
    cb.set_label(tlabel,size=14,color=tc)
    

def mycolormap(levbounds,cm_base='Spectral_r',cu='w',co='k',istart=0):
    lmin = levbounds[0]
    lmax = levbounds[1]
    incr = levbounds[2]
    levels = np.arange(lmin,lmax,incr)
    if ( (cm_base=='NCL') | (cm_base=='MJO') | (cm_base=='NCL_NOWI') ):
        nice_cmap = slx.make_SLXcolormap(whichco=cm_base)
    else:
        nice_cmap = plt.get_cmap(cm_base)
    colors = nice_cmap(np.linspace(istart/len(levels),1,len(levels)))[:]
    cmap, norm = from_levels_and_colors(levels, colors, extend='max')
    cmap.set_under(cu)
    cmap.set_over(co)
    return cmap,norm

def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap



def make_SLXcolormap(reverse=False,whichco='MJO'):
    ''' Define a custom cmap .
    Parameters: 
    * Reverse (default=False). If true, will  create the reverse colormap
    * whichco (default='MJO': which colors to use. For now: only 'MJO', 'NCL', 'NCL_NOWI' available.
    ''' 

    ### colors to include in my custom colormap
    if whichco=='MJO':
        colors_NCLbipo=[(176,17,3,1),(255,56,8,1),(255,196,1,1),(255,255,255,1),(255,255,255,1),(13,176,255,1),(2,88,255,1),(0,10,174,1)]

    if whichco=='NCL':
        colors_NCLbipo=[(11,76,95),(0,97,128),(0,161,191),(0,191,224),(0,250,250),(102,252,252),(153,250,250),(255,255,255),(255,255,255),(252,224,0),(252,191,0),(252,128,0),(252,64,0),(252,33,0),(128,0,0),(0,0,0)]

    if whichco=='NCL_NOWI':
        colors_NCLbipo=[(11,76,95),(0,97,128),(0,161,191),(0,191,224),(0,250,250),(102,252,252),(153,250,250),(255,255,255),(252,224,0),(252,191,0),(252,128,0),(252,64,0),(252,33,0),(128,0,0),(0,0,0)]

    ### Call the function make_cmap which returns my colormap
    my_cmap_NCLbipo = make_cmap(colors_NCLbipo[:], bit=True)
    my_cmap_NCLbipo_r = make_cmap(colors_NCLbipo[::-1], bit=True)
    
    if reverse==True:
        my_cmap_NCLbipo = my_cmap_NCLbipo_r

    return(my_cmap_NCLbipo)



def printdatestringF(time,it,opt="hour"):
        '''
        Read time in xarray (datetime64 format) and return date in a set format (string)
        Parameters:
        time is the time coordinnate of an xarray, converted to index. For example time as input can be time = air.time.to_index() where air is the xarray of the temperature.
        it is the time index of the date to read and print
        '''    
        
        ## imports
        # xarray
        import xarray as xr
        
        if (time.hour[it]<12):
            adh=str("0")
        else:
            adh=str()
        if (time.month[it]<10):
            adm=str("0")
        else:
            adm=str()
        if (time.day[it]<10):
            add=str("0")
        else:
            add=str()    
            
        if (opt=="day"):
            retstring=str(time.year[it])+"-"+adm+str(time.month[it])+"-"+add+str(time.day[it])
        if (opt=="hour"):
            retstring=str(time.year[it])+"-"+adm+str(time.month[it])+"-"+add+str(time.day[it])+" "+adh+str(time.hour[it])+":00" 
        if (opt=="month"):
            retstring=str(time.year[it])+"-"+adm+str(time.month[it])
        if (opt=="year"):
            retstring=str(time.year[it])

        return(retstring)

    
"""
Functions for detrending xarray data.
FROM https://xrft.readthedocs.io/en/latest/_modules/xrft/detrend.html
"""

def detrend(da, dim, detrend_type="constant"):
    """
    Detrend a DataArray

    Parameters
    ----------
    da : xarray.DataArray
        The data to detrend
    dim : str or list
        Dimensions along which to apply detrend.
        Can be either one dimension or a list with two dimensions.
        Higher-dimensional detrending is not supported.
        If dask data are passed, the data must be chunked along dim.
    detrend_type : {'constant', 'linear'}
        If ``constant``, a constant offset will be removed from each dim.
        If ``linear``, a linear least-squares fit will be estimated and removed
        from the data.

    Returns
    -------
    da : xarray.DataArray
        The detrended data.

    Notes
    -----
    This function will act lazily in the presence of dask arrays on the
    input.
    """

    if dim is None:
        dim = list(da.dims)
    else:
        if isinstance(dim, str):
            dim = [dim]

    if detrend_type not in ["constant", "linear", None]:
        raise NotImplementedError(
            "%s is not a valid detrending option. Valid "
            "options are: 'constant','linear', or None." % detrend_type
        )

    if detrend_type is None:
        return da
    elif detrend_type == "constant":
        return da - da.mean(dim=dim)
    elif detrend_type == "linear":
        data = da.data
        axis_num = [da.get_axis_num(d) for d in dim]
        chunks = getattr(data, "chunks", None)
        if chunks:
            axis_chunks = [data.chunks[a] for a in axis_num]
            if not all([len(ac) == 1 for ac in axis_chunks]):
                raise ValueError("Contiguous chunks required for detrending.")
        if len(dim) == 1:
            dt = xr.apply_ufunc(
                sps.detrend,
                da,
                axis_num[0],
                output_dtypes=[da.dtype],
                dask="parallelized",
            )
        elif len(dim) == 2:
            dt = xr.apply_ufunc(
                _detrend_2d_ufunc,
                da,
                input_core_dims=[dim],
                output_core_dims=[dim],
                output_dtypes=[da.dtype],
                vectorize=True,
                dask="parallelized",
            )
        else:  # pragma: no cover
            raise NotImplementedError(
                "Only 1D and 2D detrending are implemented so far."
            )

    return dt



def _detrend_2d_ufunc(arr):
    assert arr.ndim == 2
    N = arr.shape

    col0 = np.ones(N[0] * N[1])
    col1 = np.repeat(np.arange(N[0]), N[1]) + 1
    col2 = np.tile(np.arange(N[1]), N[0]) + 1
    G = np.stack([col0, col1, col2]).transpose()

    d_obs = np.reshape(arr, (N[0] * N[1], 1))
    m_est = np.dot(np.dot(spl.inv(np.dot(G.T, G)), G.T), d_obs)
    d_est = np.dot(G, m_est)
    linear_fit = np.reshape(d_est, N)
    return arr - linear_fit
