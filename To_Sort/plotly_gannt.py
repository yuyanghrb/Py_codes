
import plotly as py
import plotly.figure_factory as ff
 
pyplt = py.offline.plot
 
df = [dict(Task = "项目1", Start = '2019-02-01', Finish = '2019-05-28'),
      dict(Task = "项目2", Start = '2019-03-05', Finish = '2019-04-15'),
      dict(Task = "项目3", Start = '2019-03-20', Finish = '2019-05-30')]
 
fig = ff.create_gantt(df)
pyplt(fig, filename='test1.html')
