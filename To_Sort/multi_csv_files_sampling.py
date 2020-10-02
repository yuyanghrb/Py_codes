#%% 
import os
from os import listdir
from os.path import isfile, join
import pandas as pd

mypath = os.getcwd() + '\\path'
os.chdir(mypath)

#%%
onlyfile = [f for f in listdir(mypath) if isfile(join(mypath, f))]

csv_files = []
csv_names = []

for filename in onlyfile:
    if filename.split('.')[1] == 'csv':
        csv_files.append(filename)
        csv_names.append(filename.split('.')[0])


#%% sampling
csv_short_dict = {}

for i in range(len(csv_names)):
    try:
        csv_short_dict[csv_names[i]] = pd.read_csv(csv_files[i], nrows=200, index_col=0)
    except:
        csv_short_dict[csv_names[i]] = pd.read_csv(csv_files[i], index_col=0)

#%%
try:
    os.mkdir('csv_sampling')
except:
    pass

os.chdir('csv_sampling')

for name in csv_names:
    new_name = name+'_sampling.csv'
    csv_short_dict[name].to_csv(new_name)

print('Sampling Done!')
# %%
