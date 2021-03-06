# - [ ] @TODO: (2017-07-14) rewrite the _build_df method of CCD to work with SQLlite
# use spell id as unique id
%load_ext autoreload
%autoreload

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.graphics.mosaicplot import mosaic

import sqlite3

from inspectEHR.utils import load_spec
from inspectEHR.CCD import CCD
from inspectEHR.data_classes import DataRaw, ContMixin, CatMixin


# ccd = CCD(os.path.join('data-raw', 'anon_public_da1000.JSON'), random_sites=True)
refs = load_spec(os.path.join('data-raw', 'N_DataItems.yml'))

# - [ ] @TODO: (2017-07-14)
# - need a _load_from_sqlite method (i.e. connect to sqlite)
import sqlite3
conn = sqlite3.connect('ccd.db')
c = conn.cursor()

# - then once connected need an extract a _build_df (which just queries sqlite)
# given NHICcode and byvar build df for item1d or item2d
nhic_code = "NIHR_HIC_ICU_0108"
sql = "SELECT * FROM item_tb WHERE NHICcode == '{}'".format(nhic_code)
df = pd.read_sql_query('SELECT * FROM item_tb WHERE NHICcode = ?', conn, params=(nhic_code, ))
df.shape
df.columns
df = df[['site_id', 'episode_id', 'value', 'time']]
df.dtypes
# Now merge on byvar from infotb
infotb = pd.read_sql_query('SELECT * FROM infotb', conn)
infotb.head()
infotb.dtypes
jk = ['site_id', 'episode_id']
# outer join will be equivalent to preserving missingness
res = pd.merge(df, infotb, left_on=jk, right_on=jk, how='outer')
res.head()
res.shape
# use spell as primary key??
df = res[['spell', 'value', 'time', 'site_id']]
df.head()

# Now tidy
df.rename(columns={'spell': 'id', 'site_id': 'byvar'}, inplace=True)
df.shape
df.set_index('id', inplace=True)
df.head()

df.shape
conn.close()

# Generate data for testing
# Heart rate
n0108 = ccd.extract('NIHR_HIC_ICU_0108', as_type=np.int)
n0108 = ccd.extract('NIHR_HIC_ICU_0108', as_type=np.int, drop_miss=False)
d0108 = DataRaw(n0108, spec=refs['NIHR_HIC_ICU_0108'])
d0108.inspect()
d0108.plot()
d0108.plot(by=True)
df = d0108.gap_startstop(ccd)

# Lactate
n0122 = ccd.extract('NIHR_HIC_ICU_0122', as_type=np.float)
d0122 = DataRaw(n0122, spec=refs['NIHR_HIC_ICU_0122'])
df = d0122.gap_startstop(ccd)
sns.kdeplot(df['stop'].dropna())
# Sex
n0093 = ccd.extract('NIHR_HIC_ICU_0093', as_type=np.str)
d0093 = DataRaw(n0093, spec=refs['NIHR_HIC_ICU_0093'])
d0093.inspect()
d0093.plot()
d0093.plot(by=True)
d0093.plot(mosaic=True)

# Height
n0017 = ccd.extract('NIHR_HIC_ICU_0017', as_type=np.str)
n0017 = ccd.extract('NIHR_HIC_ICU_0017', as_type=np.str, drop_miss=False)


%load_ext autoreload
%autoreload
from inspectEHR.data_classes import DataRaw, ContMixin, CatMixin

# Trying dynamic class initiation to make available the correct methods
# d0108 = DataRaw(n0108, refs['NIHR_HIC_ICU_0108'])
del d0108
d0108 = DataRaw(n0108, spec=refs['NIHR_HIC_ICU_0108'])
d0108.data_complete()
d0108.data_frequency()
d0108.plot_frequency()
# d0108 = DataRaw(n0108, refs['NIHR_HIC_ICU_0108'])
sns.kdeplot(d0108.data_frequency()['time_diff'])
sns.kdeplot(d0108.data_frequency()['time_diff'], plot=True)

dt = d0108.dt.copy()
dt.head()
dt['time_diff'] = dt.groupby(level=0)[['time']].diff().astype('timedelta64[s]') / 3600
dt.groupby(level=0)[['time_diff']].mean()

dt.index.groupby()
d1 = dt.reset_index().groupby('index')[['time']].diff()
d1.head()
type(d1)
len(d1)
dt.assign(tdiff=d1)
dt['tdiff'] = d1
dt.head()
dt.shape()
d1
d2 = pd.concat([dt, d1], axis=1)

dt.tail()
dt.dtypes
dt.groupby
dt.shape
dt.reset_index().groupby('index')['time'].shift(1)
dt['time_f1'] = dt.reset_index().groupby('index')['time'].shift(1)
dt.shape
dt.head()
type(d0108)
d0108.spec
print(d0108)
d0108.inspect()
d0108.plot()
d0108.plot(by=True)


# Method for plotting using byvar
# dt = d0108.dt
# for name, grp in dt.groupby('byvar'):
#     sns.kdeplot(dt['value'])
# plt.show()



%autoreload
from inspectEHR.data_classes import DataRaw

d0017 = DataRaw(n0017, spec=refs['NIHR_HIC_ICU_0017'])
d0017.inspect()
d0017.plot(by=True)
d0017.dt['value'].isnull().value_counts()
d0017.data_complete()
d0017.data_frequency()
d0017.spec
dt = d0017.dt
dt.head()
dt.dtypes
dt.shape


dt['value'].isnull().value_counts()
dt.index
dt.loc['value']

d0093 = DataRaw(n0093, spec=refs['NIHR_HIC_ICU_0093'])
dt = d0093.dt
dt.head()


d0093._prep_miss()
d0093.data_complete()
d0093.data_frequency()

print(d0093)
d0093.inspect()
d0093.plot()
d0093.plot(by=True, col_wrap=2)
dt = d0093.dt
dt.head()
dt['value']
sns.countplot(dt['value'])
dt['value'].plot(kind='bar')
plt.show()


type(d0108)
print(d0108)
