import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x = pyo.Var(within=pyo.PositiveReals)
model.y = pyo.Var(within=pyo.PositiveReals)

model.nVars = pyo.Param(initialize=4)
model.N = pyo.RangeSet(model.nVars)
model.zvars = pyo.Var(model.N, within=pyo.Binary)


model.sillybound = pyo.Constraint(expr = model.x + model.y <= 2*model.zvars[1])

model.obj = pyo.Objective(expr = 20 * model.x)

opt = SolverFactory('cplex')
opt.solve(model) 

model.pprint() 

print ("------------- extend obj --------------") 
model.obj.expr += 10 * model.y

opt = SolverFactory('cplex') 
opt.solve(model) 
model.pprint() 
