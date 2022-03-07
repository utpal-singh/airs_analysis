"""
Copyright (C) 2014 The HDF Group

This example code illustrates how to access and visualize a GESDISC AIRS 
HDF-EOS2 Grid in Python (PyHDF).

If you have any questions, suggestions, or comments on this example, please use
the HDF-EOS Forum (http://hdfeos.org/forums).  If you would like to see an
example of any other NASA HDF/HDF-EOS data product that is not listed in the
HDF-EOS Comprehensive Examples page (http://hdfeos.org/zoo), feel free to
contact us at eoshelp@hdfgroup.org or post it at the HDF-EOS Forum
(http://hdfeos.org/forums).

Usage:  save this script and run

    python AIRS.py

The AIRS HDF-EOS2 file must either be in your current working directory
 or in a directory specified by the environment variable HDFEOS_ZOO_DIR.

"""

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
from pyhdf.SD import SD, SDC

# Open file.
FILE_NAME = 'AIRS.2021.02.01.L3.RetStd_IR028.v7.0.4.0.G21066221513.hdf'
hdf = SD(FILE_NAME, SDC.READ)

# List available SDS datasets.
print (type(hdf.datasets()))

# Read dataset.
DATAFIELD_NAME='CH4_VMR_A'
data3D = hdf.select(DATAFIELD_NAME)
data = data3D[11,:,:]

# Read geolocation dataset.
lat = hdf.select('Latitude')
latitude = lat[:,:]
lon = hdf.select('Longitude')
longitude = lon[:,:]

# Handle fill value.
attrs = data3D.attributes(full=1)
fillvalue=attrs["_FillValue"]

# fillvalue[0] is the attribute value.
fv = fillvalue[0]
data[data == fv] = np.nan
data = np.ma.masked_array(data, np.isnan(data))

# Draw an equidistant cylindrical projection using the low resolution
# coastline database.
m = Basemap(projection='cyl', resolution='l',
            llcrnrlat=-90, urcrnrlat = 90,
            llcrnrlon=-180, urcrnrlon = 180)
m.drawcoastlines(linewidth=0.5)
m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180., 181., 45.), labels=[0, 0, 0, 1])
x, y = m(longitude, latitude)
m.pcolormesh(x, y, data)
cb = m.colorbar()
cb.set_label('Unit:%')

plt.title('{0}\n {1} at H20PrsLvls=11'.format(FILE_NAME, DATAFIELD_NAME))
fig = plt.gcf()
# Show the plot window.
# plt.show()

# Save plot.
pngfile = "{0}.py.png".format(FILE_NAME)
fig.savefig(pngfile)


