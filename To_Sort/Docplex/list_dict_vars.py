import pandas as pd
from docplex.mp.model import Model

WEEKDAYS = list(range(1,8))
ASHIFTS = list(range(1,33))
ADICTS = [(i,j) for i in ASHIFTS for j in WEEKDAYS]

df_limit = pd.DataFrame(10, index=range(1,33),columns=WEEKDAYS)

m = Model('dict_defined_var')

new_vars = mdl.integer_var_dict(ADICTS, name= 'Var1')
for (i,day) in ADICTS:
        mdl.add_constraint(new_vars[(i,day)] <= df_limit[day][i])
        
TestDicts = [(i, j, k) for i in WEEKDAYS[1:3] for j in WEEKDAYS[3:5] for k in WEEKDAYS[5:6]]        
new_vars3 = mdl.continuous_var_dict(TestDicts, name= 'Var2')        
#%%
import os
dirpath = os.getcwd()

mdl.print_information()
lpfile_name = '/test1.lp'
mdl.export_as_lp(dirpath+lpfile_name)
