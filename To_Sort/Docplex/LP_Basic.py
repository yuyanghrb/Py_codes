url = 'https://api-oaas.docloud.ibmcloud.com/job_manager/rest/v1/'
key = 'api_24bb3a6b-64bc-491a-b224-0fb07cf971a4'

from docplex.mp.model import Model

# start model
m = Model('Demo_name')

# variable define
desk = m.continuous_var(name='desk')
cell = m.continuous_var(name='cell')

# write constraints
m.add_constraint(desk >= 100)
m.add_constraint(cell >= 100)
ct_assembly = m.add_constraint( 0.2 * desk + 0.4 * cell <= 400)
ct_painting = m.add_constraint( 0.5 * desk + 0.4 * cell <= 490)

# objective value
m.maximize(12 * desk + 20 * cell)

# check model infomation
m.print_information()

# solve the model
s = m.solve(url=url, key=key)
assert s is not None, "model can't solve"

m.report()
m.print_solution()
# print(s)

# # output to test
# sol = m.solve()
# print(sol)
