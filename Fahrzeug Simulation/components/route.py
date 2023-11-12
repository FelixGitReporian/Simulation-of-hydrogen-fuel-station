import pandas as pd
import numpy as np
from numpy.matlib import repmat
import math

from components.serializable import Serializable
import data_loader


class Route(Serializable):
    '''
    Route class, to construct Timeseries route DAY load
    Including: speed, acceleration, distance, loader_active, container_mass, charge_power, route_type

    Attributes
    ----------
    Serializable : class

    Methods
    -------
    get_profile
    drivephase
    workphase
    '''

    def __init__(self, timestep, data_route, file_path = None):
        '''
        Parameters:
            timestep: int [s]. simulation timestep
            data_route: dict. route data parameters
            file_path: json file. Battery parameter load file
        '''
        # Read component parameters from json file
        if file_path:
            self.load(file_path)

        else:
            print('Attention: No json file for route model specified')

        # Define durations as integer
        #self.t_wait = int(self.t_wait)

        # [s] Simulation timestep
        # ATTENTION: ROUTE class works only with a timstep of 1s
        self.timestep = timestep

        # Day route data
        self.data_route = data_route

        # Drivecycle data
        self.drivecycle = data_loader.DriveCycle()
        self.drivecycle.read_csv(self.drivecycle_file)
        self.route_acceleration = 0


    def get_profile(self):
        '''
        Method creates profile out of different phases:
            drivephase_there - 07:00 to XX:XX
            workphase - XX:XX to XX:XX
            drivephase_back - XX:XX to XX:XX

        Parameters
        ----------
        None
        '''
        # Call phase methods to create phase profiles
        self.df_drivephase = self.drivephase(self.data_route['duration'])
        #self.df_workphase = self.workphase()
        #self.df_drivephase_back = self.drivephase(self.data_route['distance_back'])

        df_main = pd.concat([self.df_drivephase],
                            ignore_index=True)

        self.profile_day = df_main


    def drivephase(self, phase_distance):
        '''
        Method creates drivephase load profile for drive there and drive back

        Parameters
        ----------
        None
        '''
        ## Input through function
        # Tour start point of driving cycle
        start = 0
        # Route needs to be finished inside driving cycle --> length(drivecycle_distance)

        # Define stopping distance for braking at end of drive there and drive back
        stopping_distance = 0

        #Get data from drivecycle and convert to numpy array
        drivecycle_speed = self.drivecycle.get_speed().values
        drivecycle_acceleration = self.drivecycle.get_acceleration().values
        drivecycle_distance = self.drivecycle.get_distance().values

        #print("drivecycle_distance: ", len(drivecycle_distance))
        #print("phase_distance: ", phase_distance)
        ## Get part of driving cycle
        # in case drive distance is shorter than dc distance
        if phase_distance <= len(drivecycle_distance):
            # get duration of first element smaller than the drive distance and stopping distance
            duration = self.data_route['duration']
            # Get spped/acceleration value of drive cycle till stopping event
            route_speed = drivecycle_speed[start : (start+duration)]
            route_acceleration = drivecycle_acceleration[start : (start+duration)]
            route_distance = drivecycle_distance[start : (start+duration)]

        # in case drive distance is longer than dc distance
        else:
            # get whole multiple of full cycles & the "rest" (decimal place) of the cycle
            duration = self.data_route['duration']
            rest = math.floor((duration - math.floor(duration)) * len(drivecycle_distance))

            # dc values are repeated to distance (whole multiple) & the "rest" (decimal place)
            route_speed = repmat(drivecycle_speed, 1, math.floor(duration)).flatten()
            route_speed = np.append(route_speed, drivecycle_speed[0:rest])
            print(len(route_speed))

            route_acceleration = repmat(drivecycle_acceleration, 1, math.floor(duration)).flatten()
            route_acceleration = np.append(route_acceleration, drivecycle_acceleration[0:rest])

            route_distance = repmat(drivecycle_distance, 1, math.floor(duration)).flatten()
            route_distance = np.append(route_distance, drivecycle_distance[0:rest])
        print(type(route_acceleration))
        self.acceleration = route_acceleration

        """
        ## Append stopping event to drive cycle
        # Define/get stopping acceleration, speed
        acceleration_stopping = -1
        speed_stopping = route_speed[-1]
        #distance_stopping = phase_distance - route_distance[-1]

        # Append speed, acceleration and distance value to route array
        while speed_stopping > abs(acceleration_stopping):
            route_speed = np.append(route_speed, (speed_stopping + acceleration_stopping))
            route_acceleration = np.append(route_acceleration, acceleration_stopping)
            route_distance = np.append(route_distance, (max(route_distance) + (speed_stopping-acceleration_stopping)))

            speed_stopping = speed_stopping + acceleration_stopping

        
        # Add loader active and container_mass fields to array with 0
        route_loader_active = route_distance * 0
        route_container_mass = route_distance * 0
        # Add route type & charger power with route phase length
        """
        route_type = np.ones(self.data_route['duration'])
        route_charger_power = np.zeros(self.data_route['duration'])

        ## Add results to DataFrame
        df_workphase = pd.DataFrame({'speed':route_speed,
                                     'acceleration':route_acceleration,
                                     'distance':route_distance,
                                     'phase_type':route_type,
                                     'charger_power':route_charger_power})
        return df_workphase