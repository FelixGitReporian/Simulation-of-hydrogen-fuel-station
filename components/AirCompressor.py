from components.simulatable import Simulatable
from components.serializable import Serializable


class AirCompressor(Serializable,Simulatable):
    '''
    Provides the method for power calculation of air compressor
    Model is based on curve-fitting via OriginPro software

    Attributes
    ----------
    Serializable: class. In order to load/save component parameters in json format
    Simulatable : class. In order to get time index of each Simulation step
    '''

    def __init__(self, timestep, input_link, file_path = None):
        '''

        Parameters
        ----------
        timestep: int. Simulation timestep in seconds
        input_link: class. Class of component which supplies input power
        file_path: json file to load air compressor parameters
        '''
        # Read air compressor parameter from json file
        if file_path:
            self.load(file_path)

        else:
            print('Attention: No json file for air compressor specified')

        # Integrate Simulatable class for time indexing
        Simulatable.__init__(self)

        # Integrate input power
        self.input_link = input_link

        # [s] Timestep
        self.timestep = timestep

    def calculate(self):
        '''
        Air compressor model:
        Method to calculate the power of air compressor
        Curve-fitting via OriginPro (R2 = 0.9979)
        -------

        '''
        # idle
        if self.input_link.power_stack == 0:
            self.power_aircompressor = 0

        # work mode
        else:
            self.power_aircompressor =  -(self.power_aircompressor_a * (-self.input_link.power_stack) ** self.power_aircompressor_c \
                                   /(self.power_aircompressor_b ** self.power_aircompressor_c + (-self.input_link.power_stack) ** self.power_aircompressor_c))
