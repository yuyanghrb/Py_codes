#!/usr/bin/env python
# coding: utf-8

# # Store_Retailer Problem Description
# 
# A retail development company just renovates some shopping complexes and wants to fill the stores with new retailers. 
# 
# ### Input data
# The store area size (in square feet) information is in Stores.csv file and the retailer information is in Retailers.csv file. For each retailer, it has requirements of the store size both lower bound and upper bound and the rent per square is also different. 
# 
# ### Limitations and Goal
# * One store can at most be assigned to one retailer.
# * One retailer can at most have one store.
# * The assigned store area should match the retailer requirement.
# * Maximize the total rental income from the stores.
# 
# ## Step 1 Read input data from csv files
# use pandas package to read the online csv file and show the data

# In[1]:



import types
import pandas as pd
from botocore.client import Config
import ibm_boto3

def __iter__(self): return 0

# @hidden_cell
# The following code accesses a file in your IBM Cloud Object Storage. It includes your credentials.
# You might want to remove those credentials before you share your notebook.
client_c68f29c221f24a0b8693acb944035ef4 = ibm_boto3.client(service_name='s3',
    ibm_api_key_id='RgBB8q_8H3uh7SmqQzLi9wcj4XY7vD3vJ1rxA5cyCEId',
    ibm_auth_endpoint="https://iam.bluemix.net/oidc/token",
    config=Config(signature_version='oauth'),
    endpoint_url='https://s3-api.us-geo.objectstorage.service.networklayer.com')

body = client_c68f29c221f24a0b8693acb944035ef4.get_object(Bucket='cplexdemos-donotdelete-pr-g7ecmafjtgb6kx',Key='Retailers.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )

df_data_1 = pd.read_csv(body)
df_data_1.head()


# In[2]:



body = client_c68f29c221f24a0b8693acb944035ef4.get_object(Bucket='cplexdemos-donotdelete-pr-g7ecmafjtgb6kx',Key='Stores.csv')['Body']
# add missing __iter__ method, so pandas accepts body as file-like object
if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )

df_data_2 = pd.read_csv(body)
df_data_2.head()


# In[3]:


# Read Data

RetailData = df_data_1
StoreData = df_data_2

Stores = list(StoreData.index)
Retailers = list(RetailData.index)

StoRange = range(0, len(Stores))
RtlRange = range(0,len(Retailers))


# ## Step 2 Set up the optimization model
# ### Create the model object
# All objects of the model belong to one model instance.

# In[4]:


# first import the Model class from docplex.mp
from docplex.mp.model import Model
import warnings
warnings.filterwarnings('ignore')

# setup IBM Decision Optimization environment

url = "https://api-oaas.docloud.ibmcloud.com/job_manager/rest/v1/"
key = "api_e115662d-0b4e-46f8-b8f1-b4d0f0d43484"

from docplex.mp.context import Context
context = Context.make_default_context()

context.solver.docloud.url = url
context.solver.docloud.key = key
context.solver.agent = 'docloud'


# create one model instance, with a name
mdl = Model("Stores_Retailer_Demo", checker='on', context=context)


# ### Define the decision variables
# * The actions, plans and choices are which store will be assigned to which retailer.
# * We use two dimension matrix to represent the choices as x[Store, Retailer].
# * x[Store, Retailer] is defined as binary variables, either 0 or 1.
# * if x[i, j]=1, it means that assign store i to retailer j. Otherwise x[i, j] = 0.

# In[5]:


# add variables
x = mdl.binary_var_matrix(StoRange, RtlRange)


# ### Set up the Constraints
# * One store can at most be assigned to one retailer.
# * One retailer can at most have one store.
# * The assigned store area should match the retailer requirement.

# In[6]:


# add constrains for One store can at most be assigned to one retailer.
mdl.add_constraints(mdl.sum(x[i,j] for j in RtlRange) <=1 for i in StoRange)

# add constrains for One retailer can at most have one store.
mdl.add_constraints(mdl.sum(x[i,j] for i in StoRange) <=1 for j in RtlRange)

# if the size does not match, set the corresponding x[i,j] to 0.
for i in StoRange:
    for j in RtlRange:
        if StoreData['Area'][Stores[i]] < RetailData['Min'][Retailers[j]]         or StoreData['Area'][Stores[i]] > RetailData['Max'][Retailers[j]]:
            mdl.add_constraint(x[i,j] == 0)


# ### Express the objective
# Maximize the total rent income. (Use area_size*rent_per_sqft)

# In[7]:


# set the objective
Total_Rent = mdl.sum(x[i,j]* RetailData['Rent'][Retailers[j]]*StoreData['Area'][Stores[i]] 
                     for i in StoRange for j in RtlRange)

mdl.maximize(Total_Rent)


# ### Solve the model 
# Also show the optimzation value

# In[8]:


s = mdl.solve()
mdl.report()
d1 = mdl.objective_value


# # Step 3 Print the detailed assignment plan

# In[9]:


for i in StoRange:
    for j in RtlRange:
        if x[i,j].solution_value >= 0.5:
            print('Store %s sign Retailer %s' %(Stores[i], Retailers[j]))


# In[ ]:




