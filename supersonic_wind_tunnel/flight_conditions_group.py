import numpy as np 
from openmdao.api import Group, IndepVarComp
from lsdo_aircraft.atmosphere.atmosphere import Atmosphere
from lsdo_aircraft.atmosphere.atmosphere_group import AtmosphereGroup

class FlightConditionsGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        group = AtmosphereGroup(
            shape=shape,
            options_dictionary=Atmosphere
        )

        self.add_subsystem('atmosphere_group', group, promotes = ['*'])