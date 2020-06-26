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

n = 1
shape = (n,n)
find = 'angle' # or 'mach_number'
'''
The find option is used to pinpoint whether we want to find the Mach Number or deflection angle
'''

prob = Problem()

model = Group()

global_variable = IndepVarComp()
global_variable.add_output('altitude', val = 0.) # Can change to simulate conditions at different altitudes
global_variable.add_output('plate_length', val = 0.)
global_variable.add_output('plate_mass', val = 0.)
if find == 'angle':
    global_variable.add_output('mach_number')
elif find == 'mach_number':
    global_variable.add_output('angle')
prob.model.add_subsystem('global_variables_comp', global_variable, promotes = ['*'])

flow_conditions_group = FlowConditionsGroup(
    shape = shape,
)
prob.model.add_subsystem('flow_conditions_group', flow_conditions_group, promotes = ['*'])






















prob.setup()
prob.run_model()