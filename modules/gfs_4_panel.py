import io
from datetime import datetime, timedelta, timezone
import xarray as xr
from siphon.catalog import TDSCatalog
import metpy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt

data_url = 'https://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best'

current_time = datetime.now(timezone.utc)

# get best GFS dataset with siphon
gfs = TDSCatalog(data_url)
best_ds = gfs.datasets[0]
ds = xr.open_dataset(best_ds.access_urls['OPENDAP'])
ice = ds.metpy.parse_cf('Ice_cover_surface')

first_ice = ice.isel(time=0)
print(first_ice)

fig = plt.figure(figsize=(12, 10))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.STATES.with_scale('50m'), linewidth=0.5)

cf = ax.contourf(first_ice.lon, first_ice.lat, first_ice, transform=ccrs.PlateCarree(), zorder=0, cmap='coolwarm')
plt.show()
