#%% 
import os
from os import listdir
from os.path import isfile, join
import pandas as pd

mypath = os.getcwd()
onlyfile = [f for f in listdir(mypath) if isfile(join(mypath, f))]

csv_files = []
csv_names = []

for filename in onlyfile:
    if filename.split('.')[1] == 'csv':
        csv_files.append(filename)
        csv_names.append(filename.split('.')[0])

# for src in csv_files:
#     print(src)

# print()
# print()

# for name in csv_name:
#     print(name)

# %%
csv_df_dict = {}
csv_short_dict = {}

for i in range(len(csv_names)):
    csv_df_dict[csv_names[i]] = pd.read_csv(csv_files[i])
    csv_short_dict[csv_names[i]] = pd.read_csv(csv_files[i], nrows=10)

# %%
for key in csv_df_dict.keys():
    print(key)

# %%
cols_name_dict={}
shape_dict = {}

for key in csv_short_dict.keys():
    cols_name_dict[key] = list(csv_short_dict[key].columns)
    shape_dict[key] = csv_df_dict[key].shape


# %%
col_set_counts_dict = {}

for key in csv_names:
    temp_list = []
    for col in cols_name_dict[key]:
        col_len = len(set(list(csv_df_dict[key][col])))
        temp_list.append(col_len)
    col_set_counts_dict[key] = temp_list



# %%
import pickle

with open('col_set_counts_dict.pkl', 'wb') as handle:
    pickle.dump(col_set_counts_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


# with open('filename.pickle', 'rb') as handle:
#     b = pickle.load(handle)


# %%
