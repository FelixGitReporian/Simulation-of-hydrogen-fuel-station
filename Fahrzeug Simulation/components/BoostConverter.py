import pandas as pd

from components.simulatable import Simulatable
from components.serializable import Serializable

class BoostConverter(Serializable,Simulatable):
    '''
    Provides the boost converter efficiency and method for calculation of power of fuel cell stack

    Attributes
    ----------
    Serializable: class. In order to load/save component parameters in json format
    Simulatable : class. In order to get time index of each Simulation step

    '''

    def __init__(self, timestep, input_link):
        '''

        Parameters
        ----------
        timestep: int. Simulation timestep in seconds
        input_link: class. Class of component which supplies input power
        '''

        # Integrate Simulatable class for time indexing
        Simulatable.__init__(self)

        # Integrate input power
        self.input_link = input_link

        # [s] Timestep
        self.timestep = timestep

        # Read efficiency_bc file
        self.data = pd.read_csv('data/components/efficiency_bc.csv')

        # Create the list of data x,y,
        self.x_data = list(self.data['x'])
        self.y_data = list(self.data['y'])


    def calculate(self):
        '''
        Boost converter model;
        Method to calculate boost converter efficiency and power output of fuel cell stack
        -------

        '''
        # Get boost converter efficiency
        self.boost_converter_efficiency()

        ## Get fuel cell stack output power
        # idle
        if self.input_link.EC_power_fuelcell == 0:
            self.efficiency_bc = 0
            self.power_stack = 0

        # discharge
        if self.input_link.EC_power_fuelcell < 0:
            self.power_stack = self.input_link.EC_power_fuelcell / self.efficiency_bc
            #print('power_stack in BC.py: ', self.power_stack)

        # No charge model
        if self.input_link.EC_power_fuelcell > 0:
            self.input_link.EC_power_fuelcell = 0

    def boost_converter_efficiency(self):
        '''
        Boost converter model: Method to get the boost converter efficiency [-]
        -------

        '''
        self.efficiency_bc = self.search(self.input_link.EC_power_fuelcell)

    def search(self, x):
        '''
        Get the efficiency corresponding to the boost converter power output
        by looking up the 'efficiency_bc' table;

        The data in the table is based on curve fitting and calculations
        based on laboratory tests conducted by Henning Lohse-Busch, Kevin Stutenberg et al.
        on a 2016 Toyota Mirai fuel cell (FC) vehicle.

        Parameters
        ----------
        x: boost converter output power [kW]
        -------

        '''
        # Take the absolute value and integer for x data
        x = abs(int(x / 1000))
        #print("bc_eta: ", x)

        # If x is not in the range of the table, return 0.95
        if x > self.x_data[-1]:
            return 0.95

        # If x is in the table
        if x in self.x_data:
            # Use the binary search method to find the index of the value closest to x
            self.x_index = self.binary_search(self.x_data, x)

            # return the y value corresponding to the x_index
            return self.y_data[self.x_index]


    def binary_search(self, y_data_p, y):
        '''
        Use the binary search method to find the index of the value closest to y

        Parameters
        ----------
        y_data_p: the y value corresponding to all x rows
        y: y value

        -------

        '''
        # Basic settings
        self.low = 0
        self.high = len(y_data_p) - 1

        # Basic judgement
        while self.low <= self.high:

            # Adjust the middle position
            self.mid = (self.low + self.high) // 2
            self.target = y_data_p[self.mid]

            # Value is greater than the value in the middle position
            if self.target > y:
                # When the difference between the y value and the target value is less than 1,
                # return the corresponding index value
                if abs(self.target - y) < 1:
                    return self.mid
                # Compare the value on the right(decreasing sequence)
                else:
                    self.high = self.mid - 1

            # Value is smaller than the value in the middle position
            elif self.target < y:
                # When the difference between the y value and the target value is less than 1,
                # return the corresponding index value
                if abs(self.target - y) < 1:
                    return self.mid
                # Compare the value on the left(decreasing sequence)
                else:
                    self.low = self.mid + 1
            # Value is the target value in the middle position, return index value
            else:
                return self.mid


