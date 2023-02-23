import xarray as xr
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
import pdb
from sklearn.linear_model import LinearRegression
import seaborn as sns

ds = xr.open_mfdataset('jfk_2100.nc') #Data for the future sceneraios for the years 2090-2100
ds1 = xr.open_dataset('~/Downloads/JFK.nc') #observed data
JFK = ds['tas']-273.
JFK1 = ds1['TAVG']
JFK_celsius=(JFK1-32.)*5./9.
plt.figure()
JFK.plot.line()
plt.plot(ds1['DATE'], JFK_celsius)



dates_reanalysis = ds['time'] #['*'] may be different for different data so check again using panoply what it is stored as in the file.
dates_obv = ds1["DATE"] # e.g here its called DATE not time in the  raw data
plt.figure()
summer_temps_ob = []
summer_temps_reanalysis = []



for date_idx in tqdm(range(len(dates_reanalysis))):
    date_to_check = dates_reanalysis[date_idx]
    if date_to_check.dt.season=='JJA':
        try:
            Temp_Re = JFK.sel(time=date_to_check)


            if np.isfinite(Temp_Re.values):
                summer_temps_reanalysis.append(Temp_Re.values)
        except KeyError:
            pass                                               #Here i have split it into two seperate for loops
                                                               #As in this script we are not plotting the statiscal relationship between observed and reanalysis
for date_idx in tqdm(range(len(dates_obv))):                   #However we still only want to run it over the summer period to save time
    date_to_check = dates_obv[date_idx]
    if date_to_check.dt.season=='JJA':
        Temp_obv= JFK_celsius[date_idx]
        if np.isfinite(Temp_obv.values):
                summer_temps_ob.append(Temp_obv.values)



#Plotting the pdfs(probabilty density function) compare the two

m = 0.25246057546843814     #using our values from the linear regression line of best fit for m and b
b =  20.610670444774332     # Type print(m) or print(b) in terminal to check
future_JFK = m*np.array(summer_temps_reanalysis)+ b  #this is our probability density function
sns.displot(future_JFK,bins=30, kde = True) #This plots the distribution as a pdf for the predicted scenario for the years 2090-2100


m = 0.25246057546843814
b = 20.610670444774332
future_JFK_ob = m*np.array(summer_temps_ob)+ b
sns.displot(future_JFK_ob, bins = 30, kde = True) #this is our pdf for observed values
plt.show()



