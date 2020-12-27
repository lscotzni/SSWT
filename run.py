'''
This code finds the relationship between the deflection angle and
the Mach Number of the flow in a supersonic wind tunnel for a flat plate
as well as flow coefficients (lift, drag, pressure)

For future reference, we also want to incorporate a diamond or rounded airfoils
'''

import numpy as np 
import openmdao.api as om 

from openmdao.api import Problem, Group, IndepVarComp

from supersonic_wind_tunnel.flow_conditions_group import FlowConditionsGroup
from supersonic_wind_tunnel.front_oblique_shock import FrontObliqueShockGroup
from supersonic_wind_tunnel.front_PM_expansion import FrontPMExpansionGroup
from supersonic_wind_tunnel.moment_balance import MomentBalanceGroup

n = 1
shape = (n,n)
# find = 'mach_number' # or 'angle'
# temp_dependence = 'false' # or 'true'

'''
The find option is used to pinpoint whether we want to find the Mach Number or deflection angle
The temp_dependence option tells us if calorically perfect (cst. gamma = 1.4) or calorically
imperfect (gamma = f(T))
We will try to implement these later, start with the simple case of constant gamma and finding Mach number
'''

prob = Problem()
model = Group()

# Defining Groups/Connections for Model ------------------------------------------------------------------------------
global_variable = IndepVarComp()
global_variable.add_output('altitude', val = 0., units = 'm') # Can change to simulate conditions at different altitudes
global_variable.add_output('plate_length', val = 1., units = 'm')
global_variable.add_output('plate_mass_per_unit_span', val = 2.87/9.81 * 101325.0, units = 'kg/m')
global_variable.add_output('gamma', val = 1.4) 
global_variable.add_output('alpha', val = 19., units = 'deg') # Deflection angle of plate in degrees (from the horizontal)
global_variable.add_output('Mu_inf', val = 3.0) # Freestream mach number
prob.model.add_subsystem('global_variables_comp', global_variable, promotes = ['*'])

flow_conditions_group = FlowConditionsGroup(
    shape = shape,
)
prob.model.add_subsystem('flow_conditions_group', flow_conditions_group, promotes = ['*'])

front_PM_expansion_group = FrontPMExpansionGroup(
    shape = shape,
)
prob.model.add_subsystem('front_PM_expansion_group', front_PM_expansion_group, promotes = ['*'])

prob.model.connect('alpha','alpha_upper_balance.rhs:Mu_1')
prob.model.connect('delta_nu_upper','alpha_upper_balance.lhs:Mu_1')
prob.model.connect('alpha_upper_balance.Mu_1','Mu_1')

front_oblique_shock_group = FrontObliqueShockGroup(
    shape = shape,
)
prob.model.add_subsystem('front_oblique_shock_group', front_oblique_shock_group, promotes = ['*'])

prob.model.connect('alpha_lower_balance.beta_2','beta_2')
prob.model.connect('alpha_2','alpha_lower_balance.lhs:beta_2')
prob.model.connect('alpha','alpha_lower_balance.rhs:beta_2')

moment_balance_group = MomentBalanceGroup(
    shape = shape,
)
prob.model.add_subsystem('moment_balance_group', moment_balance_group, promotes = ['*'])

# Design Variables, Constraints and Objective ------------------------------------------------------------
prob.model.add_design_var('Mu_inf', lower = 1.,scaler = 10)
prob.model.add_design_var('alpha_lower_balance.beta_2', lower = 0., upper = 90., scaler = 100)

prob.model.add_constraint('P1', lower = 0.)
prob.model.add_constraint('P2', lower = 0.)
prob.model.add_constraint('alpha_upper_balance.Mu_1', lower = 1.)
# prob.model.add_constraint('alpha_lower_balance.beta_2', lower = 0., upper = 90.)

prob.model.add_objective('moment_balance')

prob.setup()

# Optimizer, Driver and Setup ----------------------------------------------------------------------------


prob.model.front_PM_expansion_group.nonlinear_solver = om.NewtonSolver()
prob.model.front_PM_expansion_group.linear_solver = om.DirectSolver()

prob.model.front_PM_expansion_group.nonlinear_solver.options['iprint'] = 2
prob.model.front_PM_expansion_group.nonlinear_solver.options['maxiter'] = 100
prob.model.front_PM_expansion_group.nonlinear_solver.options['solve_subsystems'] = True

prob.model.front_oblique_shock_group.nonlinear_solver = om.NewtonSolver()
prob.model.front_oblique_shock_group.linear_solver = om.DirectSolver()

prob.model.front_oblique_shock_group.nonlinear_solver.options['iprint'] = 2
prob.model.front_oblique_shock_group.nonlinear_solver.options['maxiter'] = 100
prob.model.front_oblique_shock_group.nonlinear_solver.options['solve_subsystems'] = True


# prob.model.nonlinear_solver = om.NewtonSolver()
# prob.model.linear_solver = om.DirectSolver()

# prob.model.nonlinear_solver.options['iprint'] = 2
# prob.model.nonlinear_solver.options['maxiter'] = 100
# prob.model.nonlinear_solver.options['solve_subsystems'] = True

# old way
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP' # 'COBYLA', 'SLSQP'
prob.driver.options['tol'] = 1e-7
prob.driver.opt_settings['maxiter'] = 100
prob.driver.options['disp'] = True





# Initial guesses
# prob['alpha_upper_balance.Mu_1'] = 3.3308
# prob['alpha_lower_balance.beta_2'] = 43.
prob['alpha_upper_balance.Mu_1'] = 5.0
prob['alpha_lower_balance.beta_2'] = 59.

# prob.run_model()
prob.run_driver()


# Printing values to check solution
print(prob['pressure_MPa'])
print(prob['P1'])
print(prob['P2'])
print(prob['alpha_upper_balance.Mu_1'])
print(prob['plate_mass_per_unit_span'])
print(prob['delta_P'])
print(prob['weight_moment'])
print(prob['moment_balance'])

print('----------------------------------------------------')

print(prob['alpha_2'])

print(prob['alpha_upper_balance.Mu_1'])
print(prob['alpha_lower_balance.beta_2'])
print(prob['Mu_inf'])