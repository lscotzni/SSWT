import numpy as np 
from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import PowerCombinationComp

from lsdo_aircraft.atmosphere.temperature_comp import TemperatureComp
from lsdo_aircraft.atmosphere.pressure_comp import PressureComp
from lsdo_aircraft.atmosphere.density_comp import DensityComp
from lsdo_aircraft.atmosphere.sonic_speed_comp import SonicSpeedComp
# from lsdo_aircraft.atmosphere.viscosity_comp import ViscosityComp # may be able to remove

class FlowConditionsGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)
        self.options.declare('find', types = str)

    def setup(self):
        shape = self.options['shape']
        # find = self.options['find']

        comp = PowerCombinationComp(
            shape=shape,
            out_name='altitude_km',
            coeff=1.e-3,
            powers_dict=dict(altitude=1., ),
        )
        self.add_subsystem('altitude_km_comp', comp, promotes=['*'])

        comp = TemperatureComp(shape=shape)
        self.add_subsystem('temperature_comp', comp, promotes=['*'])

        comp = PressureComp(shape=shape)
        self.add_subsystem('pressure_comp', comp, promotes=['*'])

        comp = DensityComp(shape=shape)
        self.add_subsystem('density_comp', comp, promotes=['*'])

        comp = SonicSpeedComp(shape=shape)
        self.add_subsystem('sonic_speed_comp', comp, promotes=['*'])

        # comp = ViscosityComp(shape=shape)
        # self.add_subsystem('viscosity_comp', comp, promotes=['*'])
        # if find == 'angle':
        #     comp = PowerCombinationComp(
        #     shape=shape,
        #     out_name='speed',
        #     powers_dict=dict(
        #         mach_number=1.,
        #         sonic_speed=1.,
        #     ),
        #     )
        #     self.add_subsystem('speed_comp', comp, promotes=['*'])

        #     comp = PowerCombinationComp(
        #         shape=shape,
        #         out_name='dynamic_pressure',
        #         coeff=0.5,
        #         powers_dict=dict(
        #             density=1.,
        #             speed=2.,
        #         ),
        #     )
        #     self.add_subsystem('dynamic_pressure_comp', comp, promotes=['*'])
        # else:
        #     pass


        

        # need to edit mach number comp in atmosphere to find speed given sonic speed and mach number (input)
        # then connect this output speed to the dynamic_pressure_comp speed input