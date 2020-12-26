from openmdao.api import Group, ExecComp

class MomentBalanceGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        comp = ExecComp(
            'P1 = pressure_MPa * power( ' + 
            '(1 + (gamma-1)/2 * Mu_inf**2) / ' + 
            '(1 + (gamma-1)/2 * Mu_1**2)' + 
            ', gamma/(gamma-1))'
            ,
            shape = shape
        )
        self.add_subsystem('upper_plate_pressure_comp', comp, promotes = ['*'])

        comp = ExecComp(
            'P2 = pressure_MPa * ' + 
            '(2*gamma*(Mu_inf*cos(beta_2 * pi/180))**2 - (gamma-1)) / ' + 
            '(gamma+1)'  
            ,
            shape = shape
        )
        self.add_subsystem('lower_plate_pressure_comp', comp, promotes = ['*'])

        comp = ExecComp(
            'delta_P = P2 - P1'
            ,
            shape = shape
        )
        self.add_subsystem('pressure_moment_comp', comp, promotes = ['*'])

        comp = ExecComp(
            'weight_moment = plate_density * 9.81 * cos(alpha * pi/180)'
            ,
            shape = shape
        )
        self.add_subsystem('weight_moment_comp', comp, promotes = ['*'])

        comp = ExecComp(
            'moment_balance = abs(delta_P - weight_moment)'
            ,
            shape = shape
        )
        self.add_subsystem('moment_balance_comp', comp, promotes = ['*'])