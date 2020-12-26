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

global_variable = IndepVarComp()
global_variable.add_output('altitude', val = 0.) # Can change to simulate conditions at different altitudes
global_variable.add_output('plate_density', val = 0.)
global_variable.add_output('gamma', val = 1.4)
# if find == 'angle':
#     global_variable.add_output('freestream_mach_number', val = 2.4)
# elif find == 'mach_number':
#     global_variable.add_output('deflection_angle', val = 19.) # deflection angle of plate in degrees
global_variable.add_output('alpha', val = 19.) # deflection angle of plate in degrees
global_variable.add_output('Mu_inf', val = 2.4)
prob.model.add_subsystem('global_variables_comp', global_variable, promotes = ['*'])

flow_conditions_group = FlowConditionsGroup(
    shape = shape,
    # find = find,
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



# --------------------------

prob.setup()

# Initial guesses
prob['alpha_upper_balance.Mu_1'] = 3.3308
prob['alpha_lower_balance.beta_2'] = 43.
prob['plate_density'] = 2.87/9.81 * 0.101325

prob.run_model()

print(prob['pressure_MPa'])
print(prob['P1'])
print(prob['P2'])
print(prob['alpha_upper_balance.Mu_1'])
print(prob['delta_P'])
print(prob['weight_moment'])
print(prob['moment_balance'])
