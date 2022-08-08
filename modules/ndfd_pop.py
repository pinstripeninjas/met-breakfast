import io
from datetime import datetime, timedelta, timezone
import xarray as xr
import numpy as np
from siphon.catalog import TDSCatalog
import metpy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pygrib

# url to best NDFD dataset
data_url = 'https://thredds.ucar.edu/thredds/catalog/grib/NCEP/NDFD/NWS/CONUS/NOAAPORT/latest.xml?dataset=grib/NCEP/NDFD/NWS/CONUS/NOAAPORT/NDFD_NWS_CONUS_2p5km_20220807_0000.grib2'

ndfd_catalog = TDSCatalog(data_url)
ndfd = ndfd_catalog.datasets[0]
ds = xr.open_dataset(ndfd.access_urls['OPENDAP'])
# print(ds)
data_var = ds.metpy.parse_cf('Maximum_temperature_height_above_ground_12_Hour_Maximum')
print(data_var)
# gribs = pygrib.open(ndfd)
# gribs.seek(0)
# for grib in gribs:
#     print(grib)


fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(1, 1, 1, projection=data_var.metpy.cartopy_crs)
cf = ax.contourf(data_var.x, data_var.y, data_var.isel(time3=0, height_above_ground=2.), levels=np.arange(0, 101, 5), cmap='inferno')
ax.contour(data_var.x, data_var.y, data_var.isel(time3=0, height_above_ground=2.), colors='white', levels=np.arange(0, 110, 20))
ax.coastlines(color='black', resolution='50m')
ax.add_feature(cfeature.STATES.with_scale('50m'))
plt.colorbar(cf, orientation='horizontal')