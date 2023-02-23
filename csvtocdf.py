import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_dataset('~/Downloads/JFK.nc')

JFK = ds['TAVG']

#JFK.plot.line()
plt.plot(ds['DATE'], JFK)
plt.figure()

#JFK.groupby('DATE.year').mean('DATE').plot.line()
plt.show()

