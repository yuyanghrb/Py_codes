#!/usr/bin/env python
# coding: utf-8

# # How to make targeted offers to customers
# 
# This tutorial includes everything you need to set up IBM Decision Optimization CPLEX Modeling for Python (DOcplex), build a Mathematical Programming model, and get its solution by solving the model with IBM ILOG CPLEX Optimizer.
# 
# Table of contents:
# 
# -  [Describe the business problem](#Describe-the-business-problem)
# *  [How decision optimization (prescriptive analytics) can help](#How-decision-optimization-can-help)
# *  [Prepare the data](#Prepare-the-data)
# *  [Use decision optimization](#Use-IBM-Decision-Optimization-CPLEX-Modeling-for-Python)
#     -  [Step 1: Set up the prescriptive model](#Step-1:-Set-up-the-prescriptive-model)
#         * [Define the decision variables](#Define-the-decision-variables)
#         * [Set up the constraints](#Set-up-the-constraints)
#         * [Express the objective](#Express-the-objective)
#         * [Solve with Decision Optimization](#Solve-with-Decision-Optimization)
#     *  [Step 2: Analyze the solution and run an example analysis](#Step-2:-Analyze-the-solution)
# 

# ## Describe the business problem
# * The Self-Learning Response Model (SLRM) node enables you to build a model that you can continually update. Such updates are useful when building a model that assists with predicting which offers are most appropriate for customers and the probability of offers being accepted. These sorts of models are most beneficial in customer relationship management, such as marketing applications or call centers.
# * This example is based on a fictional banking company. 
# * The marketing department wants to achieve more profitable results in future campaigns by matching the right offer of financial services to each customer. 
# * In particular, the data science department identified the characteristics of customers who are most likely to respond favorably based on previous offers and responses and to promote the best current offer based on the results and now need to compute the best offering plan.
# <br>
# 
# A set of business constraints have to be respected:
# 
# * You have a limited budget to run a marketing campaign based on "gifts", "newsletter", "seminar"...
# * You want to determine which is the best way to contact the customers.
# * You need to identify which customers to contact.

# ## How decision optimization can help
# 
# * Prescriptive analytics technology recommends actions based on desired outcomes, taking into account specific scenarios, resources, and knowledge of past and current events. This insight can help your organization make better decisions and have greater control of business outcomes.  
# 
# * Prescriptive analytics is the next step on the path to insight-based actions. It creates value through synergy with predictive analytics, which analyzes data to predict future outcomes.  
# 
# * Prescriptive analytics takes that insight to the next level by suggesting the optimal way to handle that future situation. Organizations that can act fast in dynamic conditions and make superior decisions in uncertain environments gain a strong competitive advantage.  
# <br/>
# 
# + For example:
#     + Automate complex decisions and trade-offs to better manage limited resources.
#     + Take advantage of a future opportunity or mitigate a future risk.
#     + Proactively update recommendations based on changing events.
#     + Meet operational goals, increase customer loyalty, prevent threats and fraud, and optimize business processes.

# ## Prepare the data
# 
# The predictions show which offers a customer is most likely to accept, and the confidence level that they will accept, depending on each customer’s details.
# 
# For example:
# (139987, "Pension", 0.13221, "Mortgage", 0.10675) indicates that customer Id=139987 will certainly not buy a _Pension_ as the level is only 13.2%, 
# whereas
# (140030, "Savings", 0.95678, "Pension", 0.84446) is more than likely to buy _Savings_ and a _Pension_ as the rates are 95.7% and 84.4%.
# 
# This data is taken from a SPSS example, except that the names of the customers were modified.
# 
# A Python data analysis library, [pandas](http://pandas.pydata.org), is used to store the data. Let's set up and declare the data.

# In[1]:


import pandas as pd

names = {
    139987 : "Guadalupe J. Martinez", 140030 : "Michelle M. Lopez", 140089 : "Terry L. Ridgley", 
    140097 : "Miranda B. Roush", 139068 : "Sandra J. Wynkoop", 139154 : "Roland Guérette", 139158 : "Fabien Mailhot", 
    139169 : "Christian Austerlitz", 139220 : "Steffen Meister", 139261 : "Wolfgang Sanger",
    139416 : "Lee Tsou", 139422 : "Sanaa' Hikmah Hakimi", 139532 : "Miroslav Škaroupka", 
    139549 : "George Blomqvist", 139560 : "Will Henderson", 139577 : "Yuina Ohira", 139580 : "Vlad Alekseeva", 
    139636 : "Cassio Lombardo", 139647 : "Trinity Zelaya Miramontes", 139649 : "Eldar Muravyov", 139665 : "Shu T'an", 
    139667 : "Jameel Abdul-Ghani Gerges", 139696 : "Zeeb Longoria Marrero", 139752 : "Matheus Azevedo Melo", 
    139832 : "Earl B. Wood", 139859 : "Gabrielly Sousa Martins", 139881 : "Franca Palermo"}


data = [(139987, "Pension", 0.13221, "Mortgage", 0.10675), (140030, "Savings", 0.95678, "Pension", 0.84446), (140089, "Savings", 0.95678, "Pension", 0.80233), 
                        (140097, "Pension", 0.13221, "Mortgage", 0.10675), (139068, "Pension", 0.80506, "Savings", 0.28391), (139154, "Pension", 0.13221, "Mortgage", 0.10675), 
                        (139158, "Pension", 0.13221, "Mortgage", 0.10675),(139169, "Pension", 0.13221, "Mortgage", 0.10675), (139220, "Pension", 0.13221, "Mortgage", 0.10675), 
                        (139261, "Pension", 0.13221, "Mortgage", 0.10675), (139416, "Pension", 0.13221, "Mortgage", 0.10675), (139422, "Pension", 0.13221, "Mortgage", 0.10675), 
                        (139532, "Savings", 0.95676, "Mortgage", 0.82269), (139549, "Savings", 0.16428, "Pension", 0.13221), (139560, "Savings", 0.95678, "Pension", 0.86779), 
                        (139577, "Pension", 0.13225, "Mortgage", 0.10675), (139580, "Pension", 0.13221, "Mortgage", 0.10675), (139636, "Pension", 0.13221, "Mortgage", 0.10675), 
                        (139647, "Savings", 0.28934, "Pension", 0.13221), (139649, "Pension", 0.13221, "Mortgage", 0.10675), (139665, "Savings", 0.95675, "Pension", 0.27248), 
                        (139667, "Pension", 0.13221, "Mortgage", 0.10675), (139696, "Savings", 0.16188, "Pension", 0.13221), (139752, "Pension", 0.13221, "Mortgage", 0.10675), 
                        (139832, "Savings", 0.95678, "Pension", 0.83426), (139859, "Savings", 0.95678, "Pension", 0.75925), (139881, "Pension", 0.13221, "Mortgage", 0.10675)]

products = ["Car loan", "Savings", "Mortgage", "Pension"]
productValue = [100, 200, 300, 400]
budgetShare = [0.6, 0.1, 0.2, 0.1]

availableBudget = 500
channels =  pd.DataFrame(data=[("gift", 20.0, 0.20), ("newsletter", 15.0, 0.05), ("seminar", 23.0, 0.30)], columns=["name", "cost", "factor"])


# Offers are stored in a [pandas DataFrame](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

# In[2]:


offers = pd.DataFrame(data=data, index=range(0, len(data)), columns=["customerid", "Product1", "Confidence1", "Product2", "Confidence2"])
offers.insert(0,'name',pd.Series(names[i[0]] for i in data))


# Customize the display of this data and show the confidence forecast for each customer.

# In[3]:


CSS = """
body {
    margin: 0;
    font-family: Helvetica;
}
table.dataframe {
    border-collapse: collapse;
    border: none;
}
table.dataframe tr {
    border: none;
}
table.dataframe td, table.dataframe th {
    margin: 0;
    border: 1px solid white;
    padding-left: 0.25em;
    padding-right: 0.25em;
}
table.dataframe th:not(:empty) {
    background-color: #fec;
    text-align: left;
    font-weight: normal;
}
table.dataframe tr:nth-child(2) th:empty {
    border-left: none;
    border-right: 1px dashed #888;
}
table.dataframe td {
    border: 2px solid #ccf;
    background-color: #f4f4ff;
}
    table.dataframe thead th:first-child {
        display: none;
    }
    table.dataframe tbody th {
        display: none;
    }
"""


# In[4]:


from IPython.core.display import HTML
HTML('<style>{}</style>'.format(CSS))

from IPython.display import display
try: 
    display(offers.drop('customerid',1).sort_values(by='name')) #Pandas >= 0.17
except:
    display(offers.drop('customerid',1).sort('name')) #Pandas < 0.17


# ## Use IBM Decision Optimization CPLEX Modeling for Python
# 
# Create the optimization model to select the best ways to contact customers and stay within the limited budget.

# ### Step 1: Set up the prescriptive model
# 
# Set up the prescriptive model using the Mathematical Programming (docplex.mp) modeling package. 
# 
# #### Create the model

# In[5]:


from docplex.mp.model import Model

mdl = Model(name="marketing_campaign")


# #### Define the decision variables
# - The integer decision variables `channelVars`, represent whether or not a customer will be made an offer for a particular product via a particular channel.
# - The integer decision variable `totaloffers` represents the total number of offers made.
# - The continuous variable `budgetSpent` represents the total cost of the offers made.

# In[6]:


try: # Python 2
    offersR = xrange(0, len(offers))
    productsR = xrange(0, len(products))
    channelsR = xrange(0, len(channels))
except: # Python 3
    offersR = range(0, len(offers))
    productsR = range(0, len(products))
    channelsR = range(0, len(channels))

channelVars = mdl.binary_var_cube(offersR, productsR, channelsR)
totaloffers = mdl.integer_var(lb=0)
budgetSpent = mdl.continuous_var()


# #### Set up the constraints
# - Offer only one product per customer.
# - Compute the budget and set a maximum for it.
# - Compute the number of offers to be made.

# In[7]:


# Only 1 product is offered to each customer     
mdl.add_constraints( mdl.sum(channelVars[o,p,c] for p in productsR for c in channelsR) <=1
                   for o in offersR)

mdl.add_constraint( totaloffers == mdl.sum(channelVars[o,p,c] 
                                           for o in offersR 
                                           for p in productsR 
                                           for c in channelsR) )

mdl.add_constraint( budgetSpent == mdl.sum(channelVars[o,p,c]*channels.get_value(index=c, col="cost") 
                                           for o in offersR 
                                           for p in productsR 
                                           for c in channelsR) )

# Balance the offers among products   
for p in productsR:
    mdl.add_constraint( mdl.sum(channelVars[o,p,c] for o in offersR for c in channelsR) 
                       <= budgetShare[p] * totaloffers )
            
# Do not exceed the budget
mdl.add_constraint( mdl.sum(channelVars[o,p,c]*channels.get_value(index=c, col="cost") 
                            for o in offersR 
                            for p in productsR 
                            for c in channelsR)  <= availableBudget )  

mdl.print_information()


# #### Express the objective
# 
# Maximize the expected revenue.

# In[8]:


mdl.maximize(
    mdl.sum( channelVars[idx,p,idx2] * c.factor * productValue[p]* o.Confidence1  
            for p in productsR 
            for idx,o in offers[offers['Product1'] == products[p]].iterrows()  
            for idx2, c in channels.iterrows())
    +
    mdl.sum( channelVars[idx,p,idx2] * c.factor * productValue[p]* o.Confidence2 
            for p in productsR 
            for idx,o in offers[offers['Product2'] == products[p]].iterrows() 
            for idx2, c in channels.iterrows())
    )


# #### Solve the model
# 
# Depending on the size of the problem, the solve stage might fail and require the Commercial Edition of CPLEX engines, which is included in the premium environments in Watson Studio.

# In[9]:


s = mdl.solve()
assert s, "No Solution !!!"


# ### Step 3: Analyze the solution
# 
# First, display the **Optimal Marketing Channel per customer**.

# In[10]:


report = [(channels.get_value(index=c, col="name"), products[p], names[offers.get_value(o, "customerid")]) 
          for c in channelsR 
          for p in productsR 
          for o in offersR  if channelVars[o,p,c].solution_value==1]

assert len(report) == totaloffers.solution_value

print("Marketing plan has {0} offers costing {1}".format(totaloffers.solution_value, budgetSpent.solution_value))

report_bd = pd.DataFrame(report, columns=['channel', 'product', 'customer'])
display(report_bd)


# 
# Now **focus on seminar**.

# In[11]:


display(report_bd[report_bd['channel'] == "seminar"].drop('channel',1))


# 
# ## Summary
# 
# 
# You have learned how to set up and use IBM Decision Optimization CPLEX Modeling for Python to formulate a Mathematical Programming model and solve it with CPLEX.
# 

# ## References
# * <a href="https://rawgit.com/IBMDecisionOptimization/docplex-doc/master/docs/index.html" target="_blank" rel="noopener noreferrer">Decision Optimization CPLEX Modeling for Python documentation</a>
# * <a href="https://dataplatform.cloud.ibm.com/docs/content/getting-started/welcome-main.html?audience=wdp&context=wdp" target="_blank" rel="noopener noreferrer">Watson Studio documentation</a>
# * Need help with DOcplex or to report a bug? Go to <a href="https://developer.ibm.com/answers/smartspace/docloud" target="_blank" rel="noopener noreferrer">https://developer.ibm.com/answers/smartspace/docloud</a>
# 

# <hr>
# Copyright © 2017-2018. This notebook and its source code are released under the terms of the MIT License.

# <div style="background:#F5F7FA; height:110px; padding: 2em; font-size:14px;">
# <span style="font-size:18px;color:#152935;">Love this notebook? </span>
# <span style="font-size:15px;color:#152935;float:right;margin-right:40px;">Don't have an account yet?</span><br>
# <span style="color:#5A6872;">Share it with your colleagues and help them discover the power of Watson Studio!</span>
# <span style="border: 1px solid #3d70b2;padding:8px;float:right;margin-right:40px; color:#3d70b2;"><a href="https://ibm.co/wsnotebooks" target="_blank" style="color: #3d70b2;text-decoration: none;">Sign Up</a></span><br>
# </div>
