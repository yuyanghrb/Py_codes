# pick items in a long list to form a new list
myBigList = list(range(1000))
short_list = list( myBigList[i] for i in [87, 342, 217, 998, 500] )

# Multi-dimesion lists
WEEKDAYS = list(range(1,8))
ASHIFTS = list(range(1,33))
ADICTS = [(i,j) for i in ASHIFTS for j in WEEKDAYS]
TestDicts = [(i, j, k) for i in WEEKDAYS[1:3] for j in WEEKDAYS[3:5] for k in WEEKDAYS[5:6]]        


# Appending the same string to a list in Python
Stores = ['store' + str(i) for i in list(range(5))]
