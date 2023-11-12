from components.simulatable import Simulatable
from components.serializable import Serializable

class FC_system(Serializable, Simulatable):
    '''
    Provides method for calculation of FC system energy and efficiency
    '''

    def __init__(self, timestep, input_link, input_link1, input_link2, input_link3, file_path):
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
            print('Attention: No json file for FC_system specified')

        # Integrate simulatable class for time indexing
        Simulatable.__init__(self)

        # Integrate input power
        self.input_link = input_link
        self.input_link1 = input_link1
        self.input_link2 = input_link2
        self.input_link3 = input_link3

        # [s] Timestep
        self.timestep = timestep

    def calculate(self):

        # Get input energy for FC system component (air compressor, pump, stack)
        self.Energy_sum = -self.input_link.Energy_stack + (-self.input_link1.power_aircompressor+(-self.input_link2.power_pump)) / self.efficiency_bf

        # Get efficiency of FC system
        if self.Energy_sum == 0:
            self.efficiency_system = 0
        else:
            self.efficiency_system = (self.input_link3.efficiency_bc * (-self.input_link3.power_stack) - (
                -self.input_link1.power_aircompressor) - (-self.input_link2.power_pump)) / self.Energy_sum
            #print('efficiency_system: ', self.efficiency_system)
