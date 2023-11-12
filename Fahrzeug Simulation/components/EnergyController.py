from components.simulatable import Simulatable
from components.serializable import Serializable


class EnergyController(Simulatable, Serializable):
    '''
    Provides the method for energy management strategy of battery and fuel cell system

    '''

    def __init__(self, timestep, input_link, input_link1):
        '''

        Parameters
        ----------
        timestep: int. Simulation timestep in seconds
        input_link: class. Class of component which supplies input power (route.profile_day module)
        input_link1: class. Class of component which supplies input power (vehicle module)
        '''

        # Integrate simulatable class for time indexing
        Simulatable.__init__(self)

        # Integrate input power
        self.input_link = input_link
        self.input_link1 = input_link1

        # Timestep
        self.timestep = timestep


    def calculate(self):
        '''
        Method to calculate the power of battery and fuel cell stack

        -------

        '''
        # Acceleration phase
        if self.input_link.acceleration[self.time] > 0:
            # motor
            if self.input_link1.power_drive > 0:
                self.EC_power_battery = self.input_link1.power * 0.3 + self.input_link1.power_battery_electric
                self.EC_power_fuelcell = self.input_link1.power * 0.7
                self.power = self.EC_power_battery

            # generator
            if self.input_link1.power_drive <= 0:
                self.EC_power_battery = self.input_link1.power + self.input_link1.power_battery_electric
                self.EC_power_fuelcell = 0
                self.power = self.EC_power_battery

        # Constant speed and braking phase
        else:
            # motor
            if self.input_link1.power_drive > 0:
                self.EC_power_battery = self.input_link1.power_battery_electric
                self.EC_power_fuelcell = self.input_link1.power
                self.power = self.EC_power_battery

            # generator
            if self.input_link1.power_drive <= 0:
                self.EC_power_battery = self.input_link1.power + self.input_link1.power_battery_electric
                self.EC_power_fuelcell = 0
                self.power = self.EC_power_battery