import base64
from io import BytesIO
import xarray as xr
from siphon.catalog import TDSCatalog
import metpy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import scipy.ndimage as ndimage
# import config file for charts
from modules.config import chart_vars

data_url = 'https://thredds.ucar.edu/thredds/catalog/grib/NCEP/GFS/Global_0p25deg/catalog.xml?dataset=grib/NCEP/GFS/Global_0p25deg/Best'


def draw():
    # get best GFS dataset with siphon
    gfs = TDSCatalog(data_url)
    best_gfs = gfs.datasets[0]
    # slice to get the smaller area around the southwest
    try:
        ds = xr.open_dataset(best_gfs.access_urls['OPENDAP']).sel(lon=slice(360-120, 360-100, 2), lat=slice(40, 25, 2))
    except:
        return 'It did not work :('

    # create 4-panel figure
    fig = Figure(figsize=(10, 10), layout='tight')

    # class that manages the creation of the different charts
    class Chart:
        def __init__(self, variable):
            self.variable = variable
            self.data_var = ds.metpy.parse_cf(chart_vars[self.variable]['var_name'])
            print(self.data_var.dims)
            
        def add_to_fig(self, time_step):
            # create and design basemap for chart
            self.ax = fig.add_subplot(2, 2, chart_vars[self.variable]['position'], projection=self.data_var.metpy.cartopy_crs)
            self.ax.set_title(chart_vars[self.variable]['title'], fontsize=16)
            self.ax.coastlines(color='black', resolution='50m', zorder=1)
            self.ax.add_feature(cfeature.STATES.with_scale('50m'), zorder=1)
            
            # if need to select certain dim
            if chart_vars[self.variable]['dims']:
                self.data_var = self.data_var.isel(chart_vars[self.variable]['dims'])

            # fix to solve the variations in time, time1, etc and set the time step
            time_var = {}
            for dim in self.data_var.dims:
                if 'time' in dim:
                    time_var[dim] = time_step

            # establish correct time for the variable
            self.data_var = self.data_var.isel(time_var)

            # is there a second variable? If so, arrange data
            if chart_vars[self.variable]['second_var_name']:
                self.data_var_second = ds.metpy.parse_cf(chart_vars[self.variable]['second_var_name'])
                if chart_vars[self.variable]['second_var_dims']:
                    self.data_var_second = self.data_var_second.isel(chart_vars[self.variable]['second_var_dims'])
                # set the time
                self.data_var_second = self.data_var_second.isel(time_var)
                self.cf = self.ax.barbs(self.data_var.lon, self.data_var.lat, self.data_var, self.data_var_second, color='black', zorder=2)
            else:
                # draw the contour fill
                self.cf = self.ax.contourf(self.data_var.lon, self.data_var.lat, self.data_var, zorder=0, cmap=chart_vars[self.variable]['cmap'], alpha=chart_vars[self.variable]['alpha'])
                self.colorbar = fig.colorbar(self.cf, orientation='horizontal', shrink=0.75, pad=0.05)
                self.colorbar.set_label(chart_vars[self.variable]['units'], size='x-large')
            
            # if self.contour:
            #     self.contour_data = ds.metpy.parse_cf(self.contour)
            #     self.contour_data = self.contour_data.isel(isobaric1=10)
            #     #self.contour_data = ndimage.gaussian_filter(self.contour_data, sigma=1.5, order=0)
            #     self.ax.contour(self.contour_data.lon, self.contour_data.lat, ndimage.gaussian_filter(self.contour_data.isel(time=0), sigma=2), colors='white')
        
    # create chart instances
    pwat = Chart('pwat')
    pwat.add_to_fig(0)

    sbcape = Chart('sbcape')
    sbcape.add_to_fig(0)

    total_cloud = Chart('total_cloud')
    total_cloud.add_to_fig(0)

    temp_500 = Chart('temp_500')
    temp_500.add_to_fig(0)

    # Save figure to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"

    #plt.show()
