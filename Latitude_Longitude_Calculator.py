import numpy as np
import numpy
import math
import sys
import csv
import itertools
import math
import pandas
import datetime
from datetime import date
import os

df = pandas.read_csv('writeout.csv')
del df['Unnamed: 0']

df['LAT'] = np.nan
df['LONG'] = np.nan
df['q'] = np.nan
df['LONGconst'] = np.nan
df['TotalTime'] = np.nan

p = 2457388.5

for index, row in df.iterrows():

    k = df['RA'][index]/24*2*math.pi
    q = float(k - math.pi - df['doy'][index]/365.25689*2*math.pi - 2*math.pi*df['TIME'][index])
    df['q'][index] = q
    df['LONG'][index] = 360/(2*math.pi)*float(df['q'][index])

    df['TotalTime'][index] = df['TT'][index] - p
    df['LONGconst'][index] = df['TotalTime'][index]*1.00273781191135448*360%360

os.remove('writeout.csv')
df.to_csv('writeout.csv')