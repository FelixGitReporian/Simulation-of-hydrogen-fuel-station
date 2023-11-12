import pandas as pd
import math

from components.simulatable import Simulatable
from components.serializable import Serializable

class Vehicle(Serializable, Simulatable):
    '''
    Provides all relevant methods for the calculation of battery performance

    Attributes
    ----------
    Serializable: class. In order to load/save component parameters in json format
    Simulatable: class. In order to get time index of each Simulation step
    input_link: class. Class of component which supplies input power
    file_path: json file. Battery parameter load file

    Methods
    -------
    start
    calculate
    vehicle_driving_resistance
    vehicle_motor_electric
    vehicle_motor_fuelcell
    vehicle_loader_electric
    vehicle_loader_diesel
    '''


    def __init__(self, timestep, input_link, file_path = None):
        '''
        Parameters
        ----------
        timestep: int. Simulation timestep in seconds
        input_link: class. Class of component which supplies input power
        file_path : json file to load vehicle parameters
        '''

        # Read vehicle component parameters from json file
        if file_path:
            self.load(file_path)

        else:
            print('Attention: No json file for vehicle model specified')

        # Integrate simulatable class for time indexing
        Simulatable.__init__(self)
        # Integrate input power
        self.input_link = input_link
        # Timestep
        self.timestep = timestep

        ## Basic parameters vehicle
        # Payload vehicle [kg], m_max-m_empty

        # Initial accumulated vehicle mass (mass_empty + waste mass)
        self.mass_empty = 1850.0

        # Gravity [m/s2]
        self.grafity = 9.81

        # Read data_motor_efficiency file
        self.data = pd.read_csv('data/components/data_motor_efficiency.csv')

        # Create the list of data x,y,z
        self.x_data = list(self.data['x'])
        self.y_data = list(self.data['y'])
        self.z_data = list(self.data['z'])

        self.specification = self.specification


    def calculate(self):
        '''
        Method calculates all vehicle performance parameters by calling implemented methods

        Parameters
        ----------
        None
        '''
        # Vehicle mass, add and get mass of container from route curve
        #self.mass_cum = self.mass_cum + self.input_link.container_mass[self.time]

        ## Vehicle is in operating (driving(1) or working(2)) mode
        if self.input_link.phase_type[self.time] != 0:
            # Vehicle loader
            # if loader is active load curve column loader is set to 1

            # Get vehicle loader power of lifter
            #self.vehicle_loader()

            # Get vehicle driving resistance
            self.vehicle_driving_resistance()

            # Get required vehicle motor efficiency, power, incl. losses
            self.vehicle_motor()

            # Define vehicle power:
            #    power --> goes to connected class
            #    power_electric / power_fuelcell for evaluation

            if self.specification == 'vehicle_fuelcell':
                self.power = (-1) * self.power_motor
                self.power_battery_electric = (-1) * (self.power_aux / self.efficiency_converter)

            else:
                print('No vehicle type specified')

        ## Vehicle is in charge modus
        else:
            self.power_drive = 0
            self.power_motor = 0
            self.power = self.input_link.charger_power[self.time]


    def vehicle_driving_resistance(self):
        '''
        Vehicle driving resistance: Method calculates the driving resistance power of vehicle [W]

        Parameters
        ----------
        None
        '''
        # Overall vehicle mass with increase for rotational mass  [kg]

        self.mass_rotational = self.mass_empty

        # Air resistance [N]
        self.F_air = 0.5 * self.rho_air * self.cw * self.front_area * (self.input_link.speed[self.time])**2
        # Rolling resistance [N]
        self.F_r = self.mass_rotational * self.grafity * self.cr * math.cos(self.alpha)
        # Slope resistance [N]
        self.F_sl= self.mass_rotational * self.grafity * math.sin(self.alpha)
        # Acceleration resistance [N]
        self.F_a = self.mass_rotational * self.input_link.acceleration[self.time]
        # the vehicle propulsion force [N]
        self.F_p = self.F_air + self.F_r + self.F_sl + self.F_a

        # Vehicle mechanical power demand [W]
        self.power_drive = ((self.F_air + self.F_r + self.F_sl + self.F_a) * self.input_link.speed[self.time])


    def vehicle_motor(self):
        '''
        Vehicle motor model:
        Method calculates the electric motor efficiency [-] and input power [W]

        Parameters
        ----------
        None
        '''

        # Motor speed [rpm]
        self.W_m = self.input_link.speed[self.time] * self.k_r / self.R_wh * 60

        ## motor efficiency [-]
        if self.power_drive == 0:
            # Torque [Nm]
            self.torque = 0
            self.efficiency_motor = 0.9

        else:
            self.torque = self.F_p * self.efficiency_transmission * self.R_wh / self.k_r
            self.efficiency_motor = self.search(self.W_m, self.torque)


        if self.specification == 'vehicle_fuelcell':
            # Drivetrain efficiency [1] (motor efficiency, transmission efficiency)
            self.eta_drivetrain = self.efficiency_motor * self.efficiency_transmission
            # Engine in motor mode and below maximum motor power
            if self.power_drive > 0 and self.power_drive < self.power_motor_max:
                # Motor inlet power [W]
                self.power_motor = self.power_drive / self.eta_drivetrain

            # Engine in motor mode and above maximum motor power
            elif self.power_drive > 0 and self.power_drive > self.power_motor_max:
                # Motor inlet power [W]
                #print('power_drive in motor max: ',self.power_drive)
                #print('power_motor in motor max: ',self.power_motor)
                self.power_motor = self.power_drive / self.eta_drivetrain
                self.power_motor_max_overflow = 1
                print('vehicle engine in motor mode exceeds maximum engine power!')


            # Engine in generator mode and lower than maximum motor power
            elif self.power_drive <= 0 and self.power_drive > -self.power_motor_max:
                # Motor inlet power [W]
                self.power_motor = self.power_drive * self.eta_drivetrain

            # Engine in generator mode and higher than maximum motor power
            elif self.power_drive <= 0 and self.power_drive < -self.power_motor_max:
                # Motor inlet power [W]
                #print('power_drive in generator: ', self.power_drive)
                #print('power_motor in generator: ', self.power_motor)
                self.power_motor = - self.power_motor_max
                self.power_motor_max_overflow = -1
                print('vehicle engine in generator mode exceeds maximum engine power!')

            # Engine with no power or in generator mode & above maximum motor power
            else:
                self.power_motor = 0


        else:
            print('no vehicle specification defined in json file!')


    def search(self, x, y):
        '''
        Get the corresponding efficiency by looking up the 'data_motor_efficiency' table
        the data in the table is extracted from the motor efficiency map

        Parameters
        ----------
        x: motor speed [rpm]
        y: motor torque [Nm]

        -------

        '''
        # Take the absolute value and integer for x, y data
        x, y = abs(int(x)), abs(int(y))

        # Ceil: 312-->312+8=320
        x += 20 - x // 1 % 20

        # If x is not in the range of the table, return 0.8
        if x < self.x_data[0] or x > self.x_data[-1]:
            return 0.8

        # If x is in the table
        if x in self.x_data:
            # Find the y corresponding to all x rows
            # Use the binary search method to find the index of the value closest to y
            if y < self.y_data[0] or y > self.y_data[-1]:
                return 0.8
            self.y_list = self.y_data[self.x_data.index(x):self.x_data.index(x + 20)]
            self.y_index = self.binary_search(self.y_list, y)

            # If y is not is in the table, return 0.8
            if self.y_index == None:
                return 0.8

            if x < self.x_data[0] or x > self.x_data[-1]:
                return 0.8

            # If y is in the range of table, return the z value corresponding to the y_index
            else:
                return self.z_data[self.y_index + self.x_data.index(x)]


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
            if self.target < y:
                # When the difference between the y value and the target value is less than 3,
                # return the corresponding index value
                if abs(self.target - y) < 3:
                    return self.mid
                # Compare the value on the right(decreasing sequence)
                else:
                    self.high = self.mid - 1

            # Value is smaller than the value in the middle position
            elif self.target > y:
                # When the difference between the y value and the target value is less than 3,
                # return the corresponding index value
                if abs(self.target - y) < 3:
                    return self.mid
                # Compare the value on the left(decreasing sequence)
                else:
                    self.low = self.mid + 1
            # Value is the target value in the middle position, return index value
            else:
                return self.mid