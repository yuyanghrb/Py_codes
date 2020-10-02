import pandas as pd

# Read Data
StoreData = pd.read_csv("https://raw.githubusercontent.com/yyucresco/demo_data/master/Stores.csv", 
                        index_col=0)
RetailData = pd.read_csv("https://raw.githubusercontent.com/yyucresco/demo_data/master/Retailers.csv",
                         index_col=0)

Stores = list(StoreData.index)
Retailers = list(RetailData.index)

StoRange = range(0, len(Stores))
RtlRange = range(0,len(Retailers))


# first import the Model class from docplex.mp
from docplex.mp.model import Model

mdl = Model("Stores_Retailer_Demo")

# add variables
x = mdl.binary_var_matrix(StoRange, RtlRange)

# add constrains for One store can at most be assigned to one retailer.
mdl.add_constraints(mdl.sum(x[i,j] for j in RtlRange) <=1 for i in StoRange)

# add constrains for One retailer can at most have one store.
mdl.add_constraints(mdl.sum(x[i,j] for i in StoRange) <=1 for j in RtlRange)

# if the size does not match, set the corresponding x[i,j] to 0.
for i in StoRange:
    for j in RtlRange:
        if StoreData['Area'][Stores[i]] < RetailData['Min'][Retailers[j]] \
        or StoreData['Area'][Stores[i]] > RetailData['Max'][Retailers[j]]:
            mdl.add_constraint(x[i,j] == 0)


# set the objective
Total_Rent = mdl.sum(x[i,j]* RetailData['Rent'][Retailers[j]]*StoreData['Area'][Stores[i]] 
                     for i in StoRange for j in RtlRange)

mdl.maximize(Total_Rent)

# solve the model
s = mdl.solve()
mdl.report()
d1 = mdl.objective_value

# print detail plan
for i in StoRange:
    for j in RtlRange:
        if x[i,j].solution_value >= 0.5:
            print('Store %s sign Retailer %s' %(Stores[i], Retailers[j]))
