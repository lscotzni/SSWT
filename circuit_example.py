import openmdao.api as om
from openmdao.test_suite.scripts.circuit_analysis import Circuit

p = om.Problem()
model = p.model

model.add_subsystem('ground', om.IndepVarComp('V', 0., units='V'))

# replacing the fixed current source with a BalanceComp to represent a fixed Voltage source
# model.add_subsystem('source', om.IndepVarComp('I', 0.1, units='A'))
model.add_subsystem('batt', om.IndepVarComp('V', 1.5, units='V'))
bal = model.add_subsystem('batt_balance', om.BalanceComp())
bal.add_balance('I', units='A', eq_units='V')

model.add_subsystem('circuit', Circuit())
model.add_subsystem('batt_deltaV', om.ExecComp('dV = V1 - V2', V1={'units':'V'},
                                               V2={'units':'V'}, dV={'units':'V'}))

# current into the circuit is now the output state from the batt_balance comp
model.connect('batt_balance.I', 'circuit.I_in')
model.connect('ground.V', ['circuit.Vg','batt_deltaV.V2'])
model.connect('circuit.n1.V', 'batt_deltaV.V1')

# set the lhs and rhs for the battery residual
model.connect('batt.V', 'batt_balance.rhs:I')
model.connect('batt_deltaV.dV', 'batt_balance.lhs:I')

p.setup()

###################
# Solver Setup
###################

# change the circuit solver to RunOnce because we're
# going to converge at the top level of the model with newton instead
p.model.circuit.nonlinear_solver = om.NonlinearRunOnce()
p.model.circuit.linear_solver = om.LinearRunOnce()

# Put Newton at the top so it can also converge the new BalanceComp residual
newton = p.model.nonlinear_solver = om.NewtonSolver()
p.model.linear_solver = om.DirectSolver()
newton.options['iprint'] = 2
newton.options['maxiter'] = 20
newton.options['solve_subsystems'] = True
newton.linesearch = om.ArmijoGoldsteinLS()
newton.linesearch.options['maxiter'] = 10
newton.linesearch.options['iprint'] = 2

# set initial guesses from the current source problem
p['circuit.n1.V'] = 9.8
p['circuit.n2.V'] = .7

p.run_model()

print(p['circuit.n1.V'])
print(p['circuit.n2.V'])
print(p['circuit.R1.I'])
print(p['circuit.R2.I'])
print(p['circuit.D1.I'])