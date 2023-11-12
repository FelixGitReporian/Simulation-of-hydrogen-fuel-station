from components.simulatable import Simulatable
from components.serializable import Serializable

class FC_system(Serializable, Simulatable):
    '''
    Provides method for calculation of FC system energy and efficiency
    '''

    def __init__(self, timestep, input_link, input_link1, input_link2, input_link3, file_path_FC, file_path_AC,file_path_pump):
        '''

        Parameters
        ----------
        timestep: int. Simulation timesteps in second
        input_link: class. Class of component which supplies input power
        file_path: json file to load pump parameters
        input_link=self.fuelcell
        input_link1=self.aircompressor
        input_link2=self.pump
        input_link3=self.boostconverter
        '''

        # Read pump parameter from json file
        if file_path_FC:
            self.load(file_path_FC)

        else:
            print('Attention: No json file for FC_system specified')
        if file_path_AC:
                self.load(file_path_AC)

        else:
            print('Attention: No json file for AirCompressor specified')

        if file_path_pump:
                self.load(file_path_pump)
        else:
            print('Attention: No json file for pump specified')

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

        '''
        Air compressor model:
        Method to calculate the power of air compressor
        Curve-fitting via OriginPro (R2 = 0.9979)
        -------
        '''
        # idle
        if self.input_link3.power_stack == 0:
            self.power_aircompressor = 0

        # work mode
        else:
            self.power_aircompressor = -(
                        self.power_aircompressor_a * (-self.input_link3.power_stack) ** self.power_aircompressor_c \
                        / (self.power_aircompressor_b ** self.power_aircompressor_c + (
                    -self.input_link3.power_stack) ** self.power_aircompressor_c))

        '''
        Pump model:
        Method to calculate the power of pump
        Curve-fitting via OriginPro (R2 = 0.7517)
        -------
        '''
        # idle
        if self.input_link3.power_stack == 0:
            self.power_pump = 0

        # work mode
        else:
            self.power_pump = -(self.power_pump_a + self.power_pump_b * (-self.input_link3.power_stack))