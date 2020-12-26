from openmdao.api import Group, ExecComp, BalanceComp

class FrontPMExpansionGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        bal = self.add_subsystem('alpha_upper_balance', BalanceComp())
        bal.add_balance('Mu_1')

        comp = ExecComp(
            'nu_1 = power((gamma+1)/(gamma-1),0.5) * ' + 
            '180/pi * arctan(power((gamma-1)/(gamma+1)*(Mu_1**2-1),0.5)) - ' + 
            '180/pi * arctan(power((Mu_1**2-1),0.5))'
            ,
            shape=shape
        )
        self.add_subsystem('front_upper_PM_expansion_comp', comp, promotes = ['*'])

        comp = ExecComp(
            'nu_inf = power((gamma+1)/(gamma-1),0.5) * ' + 
            '180/pi * arctan(power((gamma-1)/(gamma+1)*(Mu_inf**2-1),0.5)) - ' + 
            '180/pi * arctan(power((Mu_inf**2-1),0.5))'
            ,
            shape=shape
        )
        self.add_subsystem('front_freestream_PM_expansion_comp', comp, promotes = ['*'])

        comp = ExecComp(
            'delta_nu_upper = nu_1 - nu_inf'
            ,
            shape = shape
        )
        self.add_subsystem('front_PM_expansion_delta_comp', comp, promotes = ['*'])


# NOTES:
# check whether arctan works with degrees or radians; we need result
# in degrees since the PM expansion equation operates using degrees