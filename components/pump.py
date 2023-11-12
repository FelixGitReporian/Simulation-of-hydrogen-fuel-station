from components.simulatable import Simulatable
from components.serializable import Serializable

class Pump(Serializable, Simulatable):
    '''
    Provides the method for power calculation of pump
    Model is based on curve-fitting via OriginPro software

    '''

    def __init__(self, timestep, input_link, file_path):
        '''

        Parameters
        ----------
        timestep: int. Simulation timesteps in second
        input_link: class. Class of component which supplies input power
        file_path: json file to load pump parameters
        '''

        # Read pump parameter from json file
        if file_path:
            self.load(file_path)

        else:
            print('Attention: No json file for pump specified')

        # Integrate simulatable class for time indexing
        Simulatable.__init__(self)

        # Integrate input power
        self.input_link = input_link

        # [s] Timestep
        self.timestep = timestep


    def calculate(self):
        '''
        Pump model:
        Method to calculate the power of pump
        Curve-fitting via OriginPro (R2 = 0.7517)
        -------

        '''
        # idle
        if self.input_link.power_stack == 0:
            self.power_pump = 0

        # work mode
        else:
            self.power_pump = -(self.power_pump_a + self.power_pump_b * (-self.input_link.power_stack))