import xarray as xr
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import pdb
from sklearn.linear_model impot LinearRegression
import seaborn as sns

ds = xr.open_mfdataset('JFK.air_temp.nc') # Reanalysis
ds1 = xr.open_dataset('~/Downloads/JFK.nc')# Observed data
#JFK = ds['air'].sel(lat=40.64, method= 'nearest').sel(lon=73.78, method= 'nearest')-273.
JFK = ds['air']
JFK1 = ds1['TAVG']
JFK_celsius=(JFK1-32.)*5./9. #check units using an application such as panoply
plt.figure()
JFK.plot.line()
plt.plot(ds1['DATE'], JFK_celsius)

#plt.figure()
#JFK.groupby('time.year').mean('time').plot.line()
#london.groupby('time.year').mean('time').plot.line()
#JFK.to_netcdf('JFK.air_temp.nc')
#plt.show()

dates_reanalysis = ds['time']
dates_obv = ds1["DATE"]
plt.figure()
summer_temps_ob = []   # creating an array to be used later in the code
summer_temps_reanalysis = [] #'[]' meant to be empty



for date_idx in tqdm(range(len(dates_obv))):  # here is the for loop making sure we are using the correct time frame
    date_to_check = dates_obv[date_idx]
    if date_to_check.dt.season=='JJA': #'JJA' here means June, July, August (summer months/ whenever the sporting event is held
        Temp_obv= JFK_celsius[date_idx] #doing this means the code doesn't have to go through every day and speeds up the whole process.
        try:
            Temp_Re = JFK.sel(time=date_to_check)
            plt.plot(Temp_Re, Temp_obv, marker= 'x', linestyle = 'none') #This is the scatter plot of reanalysis Vs. Observed values
            if np.isfinite(Temp_obv.values) and np.isfinite(Temp_Re.values): #This part here ensures that we only use days with recorded values.
                summer_temps_ob.append(Temp_obv.values)
                summer_temps_reanalysis.append(Temp_Re.values)
        except KeyError:  #If there is an error this will simply skip those values
            pass


Y = np.array(summer_temps_ob) #This sets up the linear regression by creating an array for the 2 different data sets
X = np.array(summer_temps_reanalysis)
m, b = np.polyfit(X, Y, 1) #creating the line of best fit/ linear regression
plt.plot(X, m * X + b) # plots the line of best fit (Y = m * X + b)

#model = LinearRegression().fit(X,Y)


