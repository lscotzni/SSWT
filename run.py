'''
This code finds the relationship between the deflection angle and
the Mach Number of the flow in a supersonic wind tunnel for a flat plate
'''

import numpy as np 
import openmdao.api as om 

from openmdao.api import Problem, Group, IndepVarComp

n = 1
shape = (n,n)
find = 'angle' # or Mach
'''
The find option is used to pinpoint whether we want to find the Mach Number or deflection angle
'''

prob = Problem()

global_variable = IndepVarComp()
global_variable.add_output('altitude', val = 0.) # Can change to simulate conditions at different altitudes
if find == 'angle':
    global_variable.add_output('Mach')
elif find == 'Mach':
    global_variable.add_output('angle')
prob.model.add_subsystem('global_variables_comp', global_variable, promotes = ['*'])