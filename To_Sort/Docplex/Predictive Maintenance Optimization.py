#!/usr/bin/env python
# coding: utf-8

# # Predictive Maintenance Optimization 
# 
# This notebook illustrates how to combine predictive and decision optimization techniques.
# 
# While predictive models can be trained to accurately predict the failure distribution for assets, in practice this does not enable you to plan the predictive maintenance of these assets, especially if there are some operational constraints to consider, such as the availability of parts or limited maintenance crew size.
# 
# The combination of machine learning and decision optimization is essential in helping you solve this problem.
# 
# A complete description of the problem can be found in the article <a href="https://towardsdatascience.com/predictive-maintenance-scheduling-with-ibm-data-science-experience-and-decision-optimization-25bc5f1b1b99" target="_blank" rel="noopener noreferrer">Predictive Maintenance Scheduling with IBM Watson Studio Local and Decision Optimization</a>.
# 
# In this notebooks, you can use sample data to:
# 
# 1. load, transform and clean historical data
# 1. train a predictive model to predict failure
# 1. load new data and apply the predictive model
# 1. use model predictions as input for an optimization model, along with a description of the business constraints and objective in order to find an optimal maintenance plan
# 1. display the final optimal maintenance plan using brunel visualization
# 

# >This notebook requires the Commercial Edition of CPLEX engines, which is included in the Default Python 3.5 XS + Beta of DO  in Watson Studio.

# First import some of the packages you need to use.

# In[1]:


import sys
import types
import pandas as pd
from botocore.client import Config
import ibm_boto3

import brunel

def __iter__(self): return 0


# ## Historical Data
# 
# Load historical data, remove irrelevant data, and merge it to be used for model training.

# First load the machine data frame from historical data.
# 
# Machines have different characteristics such as:
# * capacity (how much they can produce per period),
# * remaining life is the number of period before recommended maintenance according to venfor,
# * cost and loss for maintenance and repair (in general the impact of repairing after failure is higher than the impact of maintaining before failure),
# * etc

# In[2]:


df_historical_machine = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/historical-machine.csv')
df_historical_machine.head()


# For the predictive algorithm training you only need a subset of these columns, so first do some cleaning.
# 
# The column 'life' represents the number of days before failure, according to the vendor's specifications.

# In[3]:


df_historical_machine = df_historical_machine[['id', 'remaining life']];
df_historical_machine.columns = ['id', 'life']
df_historical_machine = df_historical_machine.set_index(['id'])
df_historical_machine.head()


# Next, load the production for these machines.

# In[4]:


df_historical_production = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/historical-production.csv')
df_historical_production.head()


# The following is a chart representing the historical production for machine M-01.

# In[5]:


df_production_m01 = df_historical_production[df_historical_production.machine == 'M-01']
get_ipython().run_line_magic('brunel', "data('df_production_m01') x(day) y(production) line :: width=800, height=300")


# Reshape the data so that it can be used in training the predictive model.
# 
# Production will also be used as input for the predictive model as the level of production is certainly having an impact on possible failure.

# In[6]:


df_historical_production.columns = ['id', 'day', 'production']
df_historical_production = df_historical_production.pivot(index='id', columns='day', values='production')
df_historical_production['total'] = df_historical_production.values[:, 1:].sum(1)
df_historical_production.head()


# Next load the historical failure data for these machines.
# 
# The column 'mid' represents the number of days before failure, according to historical records.

# In[7]:


df_historical_mid = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/historical-mid.csv')
df_historical_mid.columns = ['id', 'mid']
df_historical_mid = df_historical_mid.set_index(['id'])
df_historical_mid.head()


# Now merge all data required for model training into one data frame.

# In[8]:


# merge all

df_historical = df_historical_machine.join(df_historical_production).join(df_historical_mid)
df_historical.head()


# Comparing the remaining life given by the vendor with the historical failure, you can see that there is indeed a significant difference which would be valuable to predict.

# In[9]:


for m in range(1,5):
    id = "M-0" + str(m);
    print (id)
    print ("Remaining life for ", id, ": " , df_historical.life[id])
    print ("Historical failure for ", id, ": " , df_historical.mid[id])


# The following is a chart that represents the deviation between the remaining life prediction from the vendor and the real failure, due to production trend.

# In[10]:


get_ipython().run_line_magic('brunel', "data('df_historical') x(life) y(mid) size(#count) :: width=800, height=300")


# ## Failure prediction model training
# 
# You now can train a simple linear regression model to predict the failure using vendor's remaining life indication and the planned production for the machine as features.

# In[11]:


from sklearn import linear_model

X_train = df_historical.iloc[: , :-1]
y_train = df_historical.iloc[: , -1]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(X_train, y_train)


# ## Apply trained predictive model on new operational data
# 
# Now load new machines, with known characteristics, including the remaining life prediction from the vendor, and predict their failure using the linear regression model.

# Load the machine table and perform some transformation.

# In[12]:


df_machine = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/machine.csv')
df_machine.head()


# In[13]:


# Keep only useful columns
df_machine_x = df_machine[['id', 'remaining life']];
df_machine_x.columns = ['id', 'life']
df_machine_x = df_machine_x.set_index(['id'])
df_machine_x.head()


# Load the planned production and perform a simple transformation.

# In[14]:


df_planned_production = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/planned_production.csv')
df_planned_production.columns = ['id', 'day', 'production']
df_planned_production.head()


# In[15]:


df_planned_production_x = df_planned_production.pivot(index='id', columns='day', values='production')
df_planned_production_x['total'] = df_planned_production_x.values[:, 1:].sum(1)
df_planned_production_x.head()


# Merge both data frames to get the structure that can be used with a machine learning model.

# In[16]:


X_test = df_machine_x.join(df_planned_production_x)
X_test.head()


# Predict the 'mid' column corresponding to most probable failure day.

# In[17]:


y_pred = regr.predict(X_test)


# In[18]:


X_test['mid'] = y_pred
X_test.head()


# In[19]:


get_ipython().run_line_magic('brunel', "data('X_test') x(life) y(mid) size(#count) :: width=800, height=300")


# ## Prepare predictions for optimization

# In[20]:


df_day = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/day.csv')
df_day.head()


# Transform the 'mid' most probable failure day into a failure probability distribution over time.

# In[21]:


import random
import numpy as np

n_days = df_day['id'].count()

data_failure = []
for machine in df_machine['id']:
    life = int(df_machine[df_machine.id==machine]['remaining life'])
    capacity = int(df_machine[df_machine.id==machine]['capacity'])
    base = random.randint(int(0.7*capacity), capacity)    
    x = [life]
    
    mid = int(X_test.mid[machine])

    #print (str(x) + " --> " + str(mid))
    
    spread = random.randint(2, 6)
    #print spread
    n = 1000
    #s = np.random.poisson(mid, n)
    s = np.random.normal(mid, spread/4., n)

    #print s
    data = [0 for i in range(n_days)]
    for i, day in np.ndenumerate(df_day['id']):
        t = 0
        for j in range(1000):
            if int(s[j])==i[0]:
                t = t+1                    
        data_failure.append((machine, day, int (100.*t/n)))       
        
df_predicted_failure = pd.DataFrame(data=data_failure, columns=['machine', 'day', 'failure'])
df_predicted_failure.head()


# And display, for example, the predicted failure for each period for machine  M-01.

# In[22]:


df_failure_m01 = df_predicted_failure[df_predicted_failure.machine == 'M-01']
get_ipython().run_line_magic('brunel', "data('df_failure_m01') x(day) y(failure) line :: width=800, height=300")


# Perform some transformation, for example creating a structure with the cumulative probability to fail before some given day.

# In[23]:


df_predicted_failure.reset_index(inplace=True)
df_predicted_failure = df_predicted_failure.set_index(['machine', 'day'])

df_planned_production.rename(columns={'id':'machine'}, inplace=True)
df_planned_production.reset_index(inplace=True)
df_planned_production = df_planned_production.set_index(['machine', 'day'])


# In[24]:


# first global collections to iterate upon
all_machines = df_machine['id'].values
all_days = df_day['id'].values

data_cumul_failure = []
for machine in all_machines:
    for i, d in np.ndenumerate(all_days):
        cumul = 0
        for i2, d2 in np.ndenumerate(all_days):
            if i2==i:
                break
            cumul += int(df_predicted_failure.failure[machine, d2])
        data_cumul_failure.append((machine, d, cumul))

df_cumul_failure = pd.DataFrame(data_cumul_failure, columns=['machine', 'day', 'cumul_failure'])
df_cumul_failure=df_cumul_failure.set_index(['machine', 'day'])
df_cumul_failure.head()


# Display this cumulative failure for the same M-01 machine.
# 
# Taken individually, the machine M-01 must certainly be maintained shortly before Day-10.

# In[25]:


df_cumul = df_cumul_failure.reset_index()
df_cumul_m01 = df_cumul[df_cumul.machine == 'M-01']
get_ipython().run_line_magic('brunel', "data('df_cumul_m01') x(day) y(cumul_failure) line :: width=800, height=300")


# ## Optimization of maintenance
# 
# Now you will create an optimization model to create the optimal maintenance plan, taking into account some constraints.

# One last input data frame you need are the parameters.

# In[26]:


df_parameters = pd.read_csv('https://raw.githubusercontent.com/achabrier/data/master/parameters.csv')
df_parameters.head()


# You will use the **docplex** Python package to formulate the optimization model.

# In[27]:


from docplex.mp.environment import Environment
env = Environment()
env.print_information()    


# Create a new optimization model.

# In[28]:


from docplex.mp.model import Model
mdl = Model(name="PredictiveMaintenance")


# Create decision variables:
# * (real) production (taking into account maintenance or failures) per machine and day
# * maintenance per machine and day

# In[29]:


production = mdl.continuous_var_matrix(keys1=all_machines, keys2=all_days, name=lambda ns: "Production_%s_%s" % (ns[0],ns[1]))
df_production = pd.DataFrame({'production': production})
df_production.index.names=['all_machines', 'all_days']

maintenance = mdl.binary_var_matrix(keys1=all_machines, keys2=all_days, name=lambda ns: "Maintenance_%s_%s" % (ns[0],ns[1]))
df_maintenance = pd.DataFrame({'maintenance': maintenance})
df_maintenance.index.names=['all_machines', 'all_days']


# Add some constraints linking real production with planned production and maintenance.

# In[30]:


for machine in all_machines:       
    maintenance_loss = int(df_machine[df_machine.id==machine]['maintenance loss'])/100.
    capacity = int(df_machine[df_machine.id==machine]['capacity'])
    for day in all_days:   
        prod = df_planned_production.production[machine, day]
        #mdl.add_if_then( maintenance[machine, day] == 1, production[machine, day]== 0 )
        #mdl.add_if_then( maintenance[machine, day] == 0, production[machine, day]== df_production[df_production.machine==machine][df_production.day==day] )
        if (prod <= capacity*(1-maintenance_loss)):
            mdl.add_constraint( production[machine, day] == prod )
        else:
            mdl.add_constraint( production[machine, day] == prod - (prod-capacity*(1-maintenance_loss))*maintenance[machine, day])
        


# Add other constraints:
# * Perform exactly one maintenance per machine
# * The number of maintenance jobs possible on the same day is limited by the crew size

# In[31]:


# One maintenance per machine
for machine in all_machines:       
    mdl.add_constraint( mdl.sum(maintenance[machine, day] for day in all_days) == 1)
    
maintenance_crew_size = int(df_parameters[df_parameters.id=='maintenance crew size']['value'])

# One maintenance at a time
for day in all_days:       
    mdl.add_constraint( mdl.sum(maintenance[machine, day] for machine in all_machines) <= maintenance_crew_size)


# Create some cost structures to be used for objectives.

# In[32]:


data_cost_maintenance = []
cost_kpis = []
# Cost of repair
for machine in all_machines:           
    #print machine
    life = int(df_machine[df_machine.id==machine]['remaining life'])
    capacity = int(df_machine[df_machine.id==machine]['capacity'])
    cost_of_maintenance = int(df_machine[df_machine.id==machine]['cost of maintenance'])
    maintenance_loss = int(df_machine[df_machine.id==machine]['maintenance loss'])/100.
    cost_of_repair = int(df_machine[df_machine.id==machine]['cost of repair'])
    repair_loss = int(df_machine[df_machine.id==machine]['repair loss'])/100.
    loss_per_life_day = int(df_machine[df_machine.id==machine]['loss per life day'])
    production_value_unit = int(df_machine[df_machine.id==machine]['production value unit'])
    
    previous_day = None
    for i, day in np.ndenumerate(all_days):
        cost = 0;
        prob_break_before = 0
        if (previous_day != None):
            prob_break_before = int(df_cumul_failure.cumul_failure[machine, previous_day])/100.
        previous_day = day
        
        #print prob_break_before
        
        # Cost of lost production if failure before maintenance
        for i2, day2 in np.ndenumerate(all_days):
            if (i2==i):
                break
            prob_break_day2 = int(df_predicted_failure.failure[machine, day2])/100.
            production_day2 = int(df_planned_production.production[machine, day2])
            if (production_day2 > capacity*(1-repair_loss)):
                cost += production_value_unit*prob_break_day2*(production_day2 - capacity*(1-repair_loss))
            
        # Cost of repair if breaking before maintenance
        cost += cost_of_repair*prob_break_before
        
        # Cost of maintenance
        cost += cost_of_maintenance*(1-prob_break_before)
        
        # Cost of lost production for maintenance
        production_day = int(df_planned_production.production[machine, day])
        if (production_day > capacity*(1-maintenance_loss)):
            cost += production_value_unit*(production_day - capacity*(1-maintenance_loss))
        
        # Cost of maintenance too early
        cost += loss_per_life_day*max(life-i[0], 0)
        
        #print cost
        data_cost_maintenance.append((machine, day, cost))
        
        cost_kpis.append(cost*maintenance[machine, day])
        
cost_kpi = mdl.sum(cost_kpis)
mdl.add_kpi(cost_kpi, "Cost")

df_cost_maintenance = pd.DataFrame(data_cost_maintenance, columns=['machine', 'day', 'cost_maintenance'])
#print df_cost_maintenance

total_planned_production = mdl.sum(df_planned_production.production)
mdl.add_kpi(total_planned_production, "Total Planned Production")
total_production = mdl.sum(df_production.production)
mdl.add_kpi(total_production, "Total Production")


# Objective is depending of the strategy.
# * with strategy 1, the expected cost is directly minimized
# * with strategy 2, emulating some human decision-making, the maintenance are simply pushed near to the peak of failure probability. 

# In[33]:


strategy = int(df_parameters[df_parameters.id=='strategy']['value'])

if (strategy == 1):
    mdl.minimize(cost_kpi)
else:
    early = 10
    late = 1000
    temp = []     
    for machine in all_machines:           
        
        last_day = None
        for i, day in np.ndenumerate(all_days):
            last_day = day;
            cumul_failure = int(df_cumul_failure.cumul_failure[machine, day])
            if (cumul_failure > 0):                            
                temp.append(late * maintenance[machine, day] )
            else:
                temp.append(early * i[0] * maintenance[machine, day] )
        
    late_kpi = mdl.sum(temp)
    mdl.minimize(late_kpi)


# Print information on the model.
# 
# Even with this small didactic data set, the number of variables is higher than 1000 and hence the Commercial Edition of CPLEX needs to be used.

# In[34]:


mdl.print_information()


# You now can solve the model.
# 
# The engine log shows how fast the model is solved.

# In[35]:


s = mdl.solve(log_output=True)
assert s, "solve failed"
mdl.report()

all_kpis = [(kp.name, kp.compute()) for kp in mdl.iter_kpis()]
df_kpis = pd.DataFrame(all_kpis, columns=['kpi', 'value'])


# You can now access the solution value and create useful pandas data frames.

# In[36]:


df_production = df_production.production.apply(lambda v: v.solution_value)
df_production.head()


# In[37]:


df_maintenance = df_maintenance.maintenance.apply(lambda v: int(v.solution_value))
df_maintenance.head()


# In[38]:



df_production = df_production.to_frame()
df_production['machine'] = df_production.index.get_level_values('all_machines') 
df_production['day'] = df_production.index.get_level_values('all_days') 
df_production.columns = ['production', 'machine', 'day'] 
df_production = df_production.reset_index(drop=True)

df_maintenance = df_maintenance.to_frame()
df_maintenance['machine'] = df_maintenance.index.get_level_values('all_machines') 
df_maintenance['day'] = df_maintenance.index.get_level_values('all_days') 
df_maintenance.columns = ['maintenance', 'machine', 'day'] 
df_maintenance = df_maintenance.reset_index(drop=True)


# Display the maintenance plan.

# In[39]:


get_ipython().run_line_magic('brunel', "data('df_maintenance') x(day) y(machine)  bin(maintenance) color(maintenance) style('symbol:rect; size:100%; stroke:none')  :: width=1200, height=500")


# ### References
# * <a href="https://rawgit.com/IBMDecisionOptimization/docplex-doc/master/docs/index.html" target="_blank" rel="noopener noreferrer">CPLEX Modeling for Python documentation</a>
# * <a href="https://dataplatform.cloud.ibm.com/docs/content/getting-started/welcome-main.html" target="_blank" rel="noopener noreferrer">Watson Studio documentation</a>

# ### Authors
# 
# **Alain Chabrier**  IBM, France.

# <hr>
# Copyright © 2017-2018. This notebook and its source code are released under the terms of the MIT License.

# <div style="background:#F5F7FA; height:110px; padding: 2em; font-size:14px;">
# <span style="font-size:18px;color:#152935;">Love this notebook? </span>
# <span style="font-size:15px;color:#152935;float:right;margin-right:40px;">Don't have an account yet?</span><br>
# <span style="color:#5A6872;">Share it with your colleagues and help them discover the power of Watson Studio!</span>
# <span style="border: 1px solid #3d70b2;padding:8px;float:right;margin-right:40px; color:#3d70b2;"><a href="https://ibm.co/wsnotebooks" target="_blank" style="color: #3d70b2;text-decoration: none;">Sign Up</a></span><br>
# </div>
