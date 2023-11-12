import math
from components.simulatable import Simulatable
from components.serializable import Serializable


class Fuelcell(Serializable,Simulatable):
    '''
    Provides all relevant methods for the calculation of fuel cell stack performance


    Attributes
    ----------
    Serializable: class. In order to load/save component parameters in json format
    Simulatable: class. In order to get time index of each Simulation step

    Methods
    -------

    '''
    def __init__(self, timestep, input_link, input_link1, input_link2, file_path = None):
        '''

        Parameters
        ----------
        timestep: int. Simulation timesteps in second
        input_link: class. Class of component which supplies input power
        file_path: json file to load fuel cell parameters
        '''

        # Read fuel cell stack parameters from json file
        if file_path:
            self.load(file_path)

        else:
            print('Attention: No json file for fuel cell module specified')

        # Integrate simulatable class for time index
        Simulatable.__init__(self)

        # Integrate input power
        self.input_link = input_link
        self.input_link1 = input_link1
        self.input_link2 = input_link2

        # Timestep [s]
        self.timestep = timestep

        ##Basic parameters
        self.specification = self.specification


    def calculate(self):

        # Get fuel cell stack efficiency
        self.calc_efficiency_stack()

        # Get present massflow of h2
        if self.input_link.power_stack < 0 and self.efficiency_stack > 0.01:
            self.Energy_stack = self.input_link.power_stack / self.efficiency_stack
            self.massflow_h2 = -(self.Energy_stack / self.HHV)
            #print('self.massflow_h2: ', self.massflow_h2)
        else:
            self.Energy_stack = 0
            self.massflow_h2 = 0


    def calc_efficiency_stack(self):
        '''
        Fuel cell stack efficiency model:
        Method to calculate the efficiency of fuel cell stack
        Curve-fitting via OriginPro (R2 = 0.95632)
        -------

        '''
        # idle
        if self.input_link.power_stack == 0:
            self.efficiency_stack = 0

        # discharge mode
        if self.input_link.power_stack < 0 and self.input_link.power_stack > - self.power_stack_max:
            self.efficiency_stack = 0.01 * (self.efficiency_stack_y0 + self.efficiency_stack_A
                                * (1 / (1 + math.exp(-(-self.input_link.power_stack / 1000 - self.efficiency_stack_xc
                                + self.efficiency_stack_w1 / 2) / self.efficiency_stack_w2)))
                                * (1 - 1 / (1 + math.exp(-(-self.input_link.power_stack / 1000 - self.efficiency_stack_xc
                                - self.efficiency_stack_w1 / 2) / self.efficiency_stack_w3))))
            #print('efficiency_stack: ',self.efficiency_stack)


        if self.input_link.power_stack <0 and self.input_link.power_stack < -self.power_stack_max:
            self.efficiency_stack = 0.01 * (self.efficiency_stack_y0 + self.efficiency_stack_A
                                * (1 / ( 1 + math.exp(-(-self.input_link.power_stack / 1000 - self.efficiency_stack_xc
                                + self.efficiency_stack_w1 / 2) / self.efficiency_stack_w2)))
                                * (1 - 1 / ( 1 + math.exp(-(-self.input_link.power_stack / 1000 - self.efficiency_stack_xc
                                - self.efficiency_stack_w1 / 2) / self.efficiency_stack_w3))))
            print('Fuel cell stack power exceeds maximum stack power!')
            print(- self.input_link.power_stack)

        # no charge mode
        if self.input_link.power_stack > 0:
            self.efficiency_stack = 0

