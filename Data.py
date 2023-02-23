import xarray as xr
import matplotlib.pyplot as plt

ds = xr.open_mfdataset('~/Downloads/air.2m.gauss.*.nc') #Reanalysis data the '*' is a placeholder for any files with the same format to be used.
ds1 = xr.open_dataset('~/Downloads/JFK.nc') #observed data (chnaged from .csv to .nc in another script
JFK = ds['air'].sel(lat=40.64, method= 'nearest').sel(lon=73.78, method= 'nearest')-273. #-273 changes units from kelvin to celsius
JFK1 = ds1['TAVG']
JFK_celsius=(JFK1-32.)*5./9.  #from farenheit to celsius
plt.figure()
JFK.plot.line() # will plot a line for the data we wont be analysing  this
plt.plot(ds1['DATE'], JFK_celsius)

#plt.figure()
#JFK.groupby('time.year').mean('time').plot.line()
#london.groupby('time.year').mean('time').plot.line()
JFK.to_netcdf('JFK.air_temp.nc') #converts to a new file for the specific loctaion and weather.
plt.show()


