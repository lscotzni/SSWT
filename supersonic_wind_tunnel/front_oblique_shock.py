from openmdao.api import Group, ExecComp, BalanceComp

class FrontObliqueShockGroup(Group):
    def initialize(self):
        self.options.declare('shape', types = tuple)

    def setup(self):
        shape = self.options['shape']

        bal = self.add_subsystem('alpha_lower_balance', BalanceComp())
        bal.add_balance('beta_2')

        comp = ExecComp(
            'alpha_2 = 180/pi * arctan(' + 
                '2*power(tan(beta_2 * pi/180),-1.0) * ' + 
                '(power(Mu_inf*sin(beta_2 * pi/180),2.0) - 1.0) / ' + 
                '(2 + Mu_inf**2 * (gamma + cos(2*beta_2 * pi/180))))'
            ,
            shape=shape
        )
        self.add_subsystem('front_lower_shock_angle_comp', comp, promotes = ['*'])