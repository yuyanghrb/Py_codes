from docplex.mp.advmodel import AdvModel

adv_mdl = AdvModel('Matrix_Model')

x = adv_mdl.continuous_var(name = 'x')
y = adv_mdl.continuous_var(name = 'y')
z = adv_mdl.continuous_var(name = 'z')

A = [[1, 2, 3],
     [4, 5, 6]]
Xs = [x, y, z] # where x, y, and z are decision variables (size 3), and

B = [100, 200] # a sequence of numbers (size 2)
adv_mdl.matrix_constraints(A, Xs, B, 'GE')


L = [101, 102]
U = [201, 202]

# adv_mdl.range_constraints(A, Xs, L, U)

adv_mdl.set_objective('min', x+y+z)

adv_mdl.export_as_lp('test_file.lp')


#%%
# adv_mdl.solve()