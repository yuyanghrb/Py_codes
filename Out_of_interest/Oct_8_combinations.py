# how_many_drop_delivery_combination
# solve a problem
# 提问一个有趣的数学问题：一个骑手要送五个外卖，有五个商家五个用户，那么有多少种排列组合方式？ 

#%%
Time_slot = list(range(1,11))

Jobs = ['Pick1', 'Pick2', 'Pick3', 'Pick4', 'Pick5',
        'Out1', 'Out2', 'Out3', 'Out4', 'Out5']

All_list = [['Pick1', 'Pick2', 'Pick3', 'Pick4', 'Pick5',
            'Out1', 'Out2', 'Out3', 'Out4', 'Out5']]

for i1 in Time_slot:
    for i2 in Time_slot:
        for i3 in Time_slot:
            for i4 in Time_slot:
                for i5 in Time_slot:
                    for i6 in Time_slot:
                        for i7 in Time_slot:
                            for i8 in Time_slot:
                                for i9 in Time_slot:
                                    for i10 in Time_slot:
                                        if len(set([i1, i2, i3, i4, i5, i6, i7, i8, i9, i10])) == 10:
                                            if i6 > i1 and i7 > i2 and i8 > i3 and i9 > i4 and i10 > i5:
                                                All_list.append([i1, i2, i3, i4, i5, i6, i7, i8, i9, i10])

# %%
print(len(All_list))