#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

RawData = pd.read_csv("https://raw.githubusercontent.com/yyucresco/demo_data/master/Retailers.csv", index_col=0)

RawData.head()


# In[2]:


def df_2d_list(_df_name):
    _rows, _cols = _df_name.shape
    _result_list = [] 
    for i in range(_rows):
        _row_list = []
        _row_list.append(_df_name.index[i])
        for j in range(_cols):
            _row_list.append(_df_name.iloc[(i,j)])
        _result_list.append(_row_list)
    return _result_list
List1 = df_2d_list(RawData)


# In[6]:


List1[1]


# In[45]:


def out_fun(number):
    print('it runs out!')
    return number*5


class store:
    def __init__(self, *args):
        # read a list as input arguments
        arg = args[0]
        self.name = arg[0]
        self.min = arg[1]
        #print('Min is '+str(self.min))
        self.max = arg[2]
        self.rate = arg[3]
        self.avg = (self.min + self.max)/2
        self.in1 = self.fun1()
        
        self.out1 = out_fun(self.rate)
    def add_var(self):
        print('Add Store variables here')
        
    def fun1(self):
        print('it runs in! ')
        return self.min*10
    
class big_store(store):
    def big_func(self):
        print('This is a big store')


# In[46]:


big_store1 = big_store(List1[2])

big_store1.in1


# In[35]:


big_store1.big_func()


# In[36]:


big_store1.avg


# In[28]:


store1 = store(List1[1])


# In[30]:


List1[1]


# In[29]:


store1.avg


# In[26]:


store1.add_var()


# In[20]:


store_list = []
for item in List1:
    store_list.append(store(item))


# In[22]:


store_list[2].name


# In[ ]:




