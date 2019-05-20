import numpy as np
import sys
import csv
import itertools
import math
import pandas
import datetime
from datetime import date, tzinfo, timedelta
import os

dt = str(datetime.datetime.utcnow())
dT = dt.rsplit('-',2)
DT = dT[0:2]
DT.append(dT[2][0:2])
DT.append(dT[2][3:5])
DT.append(dT[2][6:8])
DT.append(dT[2][9:11])
DT.append(dT[2][12:18])
year = DT[0]
month = DT[1]
d = DT[2]
h = DT[3]
minutes = DT[4]
seconds = DT[5]

a = (14 - float(month))//12
y = float(year) + 4800 - a
m = float(month) + 12*a - 3

curr_t = float(d) + (153*m + 2)//5 + 365*y + y//4 - y//100 + y//400 - 32045 - 0.5  + (float(minutes)/60)/24 +(float(seconds)/3600)/24 + float(h)/24

f = open('workfile', 'w')
f.write(str(curr_t))
f.close()

import urllib2
response = urllib2.urlopen('http://exoplanets.org/csv-files/exoplanets.csv')
output = open('exoplanets.csv', 'wb')
output.write(response.read())
output.close()

df = pandas.read_csv("exoplanets.csv", low_memory = False)



df = df.iloc[:1643,(0,19,30,33,40,132,152,155,168,174,175,182,181,197,274,280,293,297)]
for index, row in df.iterrows():

    if str(df['TT'][index]) == 'nan':
        df.drop([index], axis=0, inplace = True)


for index, row in df.iterrows():

    if str(df['R'][index]) == 'nan':
        if str(df['MASS'][index]) != 'nan':
            x = (float(df['MASS'][index]))**2.04
            if x < 11.209:
                df['R'][index] = x
            else:
                df['R'][index] = 11.209
              
    if df['TT'][index] < curr_t:
        while df['TT'][index] < curr_t:
            df['TT'][index] = df['TT'][index] + df['PER'][index]
        
    if str(df['DEPTH'][index]) == 'nan' or df['DEPTH'][index] > 1:
        if str(df['R'][index]) != 'nan' and str(df['RSTAR'][index]) != 'nan':
            df['DEPTH'][index] = (0.0090788*float(df['R'][index])/float(df['RSTAR'][index]))**2
        else:
            df['DEPTH'][index] = 'nan'
            
for index, row in df.iterrows():           
            
    if df['TT'][index] < 2440000:
        print('too low')
        df['TT'][index] = df['TT'][index] + 2440000

df['Window_Lower'] = df['TT'] - (df['T14'])/2
df['Window_Upper'] = df['TT'] + (df['T14'])/2

df['Window'] = np.nan
for index, row in df.iterrows():
    df['Window'][index] = str(df['Window_Lower'][index]) + str(' - ') + str(df['Window_Upper'][index])
try:
    os.remove('writeout.csv')
except:
    pass
df.to_csv('writeout.csv')

execfile('Julian_to_Gregorian_Conversion.py')
print()
execfile('Latitude_Longitude_Calculator.py')

try:
    os.remove('writeout.csv')
except:
    pass
df.to_csv('writeout.csv')