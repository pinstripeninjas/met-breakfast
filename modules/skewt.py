import base64
from io import BytesIO
from datetime import datetime, timezone, timedelta
from urllib.error import HTTPError
from siphon.simplewebservice.wyoming import WyomingUpperAir
from metpy.units import units
import metpy.plots as plots
import metpy.calc as mpcalc
# documentation recommends using Figure constructor instead of pyplot
# this is to prevent memory leaks when using flask applications 
from matplotlib.figure import Figure

def draw():
    # Get current datetime and set hour to 12z
    sounding_time = datetime.now(timezone.utc)
    sounding_time = sounding_time.replace(hour=12, minute=0, second=0, microsecond=0)
    station = 'TUS'

    # Get upper air data for station if requested datetime is available
    df = None
    try:
        df = WyomingUpperAir.request_data(sounding_time, station)
    except HTTPError:
        return '<p>Sad times. The server is too busy to retrieve the skewT :(</p>'
    # if requested datetime is not available, get the previous 12z sounding
    except ValueError:
        sounding_time = sounding_time - timedelta(days=1)
        df = WyomingUpperAir.request_data(sounding_time, station)

    # function to set proper units
    def set_units(variable):
        return df[variable].values * units(df.units[variable])

    # create variables for all elements with units
    p = set_units('pressure')
    T = set_units('temperature')
    Td = set_units('dewpoint')
    u = set_units('u_wind')
    v = set_units('v_wind')

    # calculate some useful values
    parcel_path = mpcalc.parcel_profile(p, T[0], Td[0])
    cape_cin = mpcalc.cape_cin(p, T, Td, parcel_path)
    mucape_cin = mpcalc.most_unstable_cape_cin(p, T, Td)
    mucape_parcel = mpcalc.most_unstable_parcel(p, T, Td)
    print(cape_cin)
    print(mucape_cin)
    print(mucape_parcel)

    # mask data so wind barbs don't extend beyond the plot
    mask = p >= 100 * units.hPa

    # create plot
    fig = Figure(figsize=(8, 6), layout='tight')
    skew = plots.SkewT(fig)
    title_str = 'Tucson Skew-T' + sounding_time.strftime("%a, %B %d, %Y %H")
    skew.ax.set_title('Tucson Skew-T', loc='left')
    skew.ax.set_title(f'{sounding_time.strftime("%a, %B %d, %Y %H")}Z', loc='right')
    skew.ax.set_xlim(-50, 50)
    skew.plot_dry_adiabats(linewidth=1)
    skew.plot_moist_adiabats(linewidth=1)
    skew.plot_mixing_lines(linewidth=1)
    skew.plot(p, T, 'red')
    skew.plot(p, Td, 'green')
    skew.plot_barbs(p[mask][::7], u[mask][::7], v[mask][::7], linewidth=1)
    skew.plot(p, parcel_path, color='black')
    skew.shade_cape(p, T, parcel_path)
    skew.shade_cin(p, T, parcel_path)

    # Save figure to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format='png', transparent='true')
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return f"<img src='data:image/png;base64,{data}'/>"
