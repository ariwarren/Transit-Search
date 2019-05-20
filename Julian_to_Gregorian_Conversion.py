import numpy as np
import numpy
import sys
import csv
import itertools
import math
import pandas
import datetime
from datetime import date
import os

dt = str(datetime.datetime.now())
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

f = open('timecoordinates', 'w')
f.write((DT[0]))
f.close()

a = (14 - float(month))//12
y = float(year) + 4800 - a
m = float(month) + 12*a - 3

curr_t = float(d) + (153*m + 2)//5 + 365*y + y//4 - y//100 + y//400 - 32045 - 0.5 + float(7)/24 + (float(minutes)*10/600)/24 +(float(seconds)*10/600*10/600)/24 + float(h)/24 

f = open('workfile', 'w')
f.write(str(curr_t))
f.close()

df = pandas.read_csv('writeout.csv')
del df['Unnamed: 0']


df['m'] = np.nan
df['doy'] = np.nan
df['t-doy'] = np.nan
df['test'] = np.nan
df['DATE'] = np.nan
df['DATE-num'] = np.nan
df['TIME'] = np.nan
df['DATE+TIME'] = np.nan

p = 2457388.5

for index, row in df.iterrows():
    
    if type(df['TT'][index]) == numpy.float64 and df['TT'][index] > 1:
        t = float(df['TT'][index]) - p
        df['t-doy'][index] = t
        df['test'] = 5
        df['doy'][index] = int(t) + 1
        if t < 365:
            y = 2015

            if date.today().year%4 == 0:
                if t<32:
                    m = 'January'
                    mn = 1
                    d = t + 1
                elif t<60:
                    m = 'February'
                    mn = 2
                    d = t + 1 - 32
                elif t<91:
                    m = 'March'
                    mn = 3
                    d = t + 1 - 60
                elif t<121:
                    m = 'April'
                    mn = 4
                    d = t + 1 - 91
                df['m'][index] = m

                df['DATE'][index] = m+' '+str(int(d))
                d_frac = d - int(d)
                df['TIME'][index] = df['TT'][index] - int(df['TT'][index])
                hours = d_frac*24
                hour = int(hours)
                if hour < 10:
                    Hour = str(0)+str(hour)
                else:
                    Hour = hour                
                hour_frac = hours - hour
                minutes = int(hour_frac*60)
                if minutes < 10:
                    Minutes = str(0)+str(minutes)
                else:
                    Minutes = minutes
                Time = str(Hour)+':'+str(Minutes)
                df['DATE+TIME'][index] = m+' '+str(int(d))+'    '+Time
                df['DATE-num'][index] = str(mn)+','+' '+str(d)
                    
                    
                
    else:
        print('-------------------------------------------------------')
        print(index)

os.remove('writeout.csv')

df.to_csv('writeout.csv')