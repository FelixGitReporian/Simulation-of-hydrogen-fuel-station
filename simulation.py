from datetime import datetime
import pandas as pd
import numpy as np
from collections import OrderedDict

from components.simulatable import Simulatable

from components.route import Route
from components.vehicle import Vehicle
from components.power_component import Power_Component
from components.battery import Battery
from components.EnergyController import EnergyController
from components.BoostConverter import BoostConverter
from components.AirCompressor import AirCompressor
from components.pump import Pump
from components.FuelCell import Fuelcell
from components.FC_system import FC_system
from components.charger import Charger
from components.power_component import Power_Component
from components.battery import Battery
from components.fuelcell_charger_battery import Charger_fc
import pickle


class Simulation(Simulatable):
    """
    Central Simulation class, where vehicle energy system is constructed
    Extractable system power flows are defined here

    Attributes
    ----------
    Simulatable : class. In order to simulate system

    Methods
    -------
    simulate
    """

    def __init__(self, data_route):
        '''
        Parameters
        ----------
        data_route: dict - route profile parameter:
            container_mass: float [kg].     Mass of container
            containers_sum: int [1].        Number of containers of collection route
            stops_sum: int [1].             Number of stops of route
            distance_there: float [m].      Route phase distance of transfer drive to collection from recycling hub
            distance_back: float [m].       Route phase distance of transfer drive from collection to recycling hub
            distance_collection: float [m]. Route phase distance of collection phase
            overall_distance: float [m].    Overall route distance
        '''

        ## Define simulation parameters
        # [s] Simulation timestep
        self.timestep = 1

        ## Create route profile
        self.route = Route(timestep=self.timestep,
                           data_route=data_route,
                           file_path='data/components/route_profile.json')
        self.route.get_profile()

        ## Initialize system component classes
        # Vehicle
        self.vehicle = Vehicle(timestep=self.timestep,
                               input_link=self.route.profile_day,
                               file_path='data/components/vehicle_fuelcell.json')

        self.duration = data_route['duration']
        self.routen_profil = data_route["routenprofil"]
        #print(type(self.routen_profil))



        if self.vehicle.specification == 'vehicle_fuelcell':

            # Energy Controller
            self.energycontroller = EnergyController(timestep=self.timestep,
                                                     input_link=self.route.profile_day,
                                                     input_link1=self.vehicle)

            # Boost Converter
            self.boostconverter = BoostConverter(timestep=self.timestep,
                                                 input_link=self.energycontroller)

            # Air Compressor
            self.aircompressor = AirCompressor(timestep=self.timestep,
                                               input_link=self.boostconverter,
                                               file_path='data/components/air compressor.json')

            # Pump
            self.pump = Pump(timestep=self.timestep,
                             input_link=self.boostconverter,
                             file_path='data/components/pump.json')

            # Fuel Cell
            self.fuelcell = Fuelcell(timestep=self.timestep,
                                     input_link=self.boostconverter,
                                     input_link1=self.aircompressor,
                                     input_link2=self.pump,
                                     file_path='data/components/Fuelcell.json')

            # Battery Management System
            self.battery_management = Power_Component(timestep=self.timestep,
                                                      input_link=self.energycontroller,
                                                      input_link1=self.vehicle,
                                                      input_link2=self.aircompressor,
                                                      input_link3=self.pump,
                                                      file_path='data/components/battery_management.json')

            # Battery
            self.battery = Battery(timestep=self.timestep,
                                   input_link=self.battery_management,
                                   input_link1=self.route.profile_day,
                                   file_path='data/components/battery_lfp_fuel.json')

            #Fuel cell system
            self.FC_system = FC_system(timestep=self.timestep,
                                       input_link=self.fuelcell,
                                       input_link1=self.aircompressor,
                                       input_link2=self.pump,
                                       input_link3=self.boostconverter,
                                       file_path='data/components/FC_system.json')



            ## Initialize Simulatable class and define needs_update initially to True
            Simulatable.__init__(self, self.vehicle, self.energycontroller, self.boostconverter, self.aircompressor, self.pump, self.fuelcell, self.battery_management, self.battery, self.FC_system)

            self.needs_update = True



    def simulate(self):
        """
        Central simulation method, which :
            initializes all list containers to store simulation results
            iterates over all simulation timesteps and calls Simulatable.start/update/end()

        Parameters
        ----------
        Non
        """
        # Initialization of list containers to store simulation results

        # Timeindex
        self.timeindex = list()

        if self.vehicle.specification == 'vehicle_fuelcell':
            # Vehicle
            #self.vehicle_mass_cum = list()
            self.vehicle_power_drive = list()
            #self.vehicle_power_loader = list()
            self.vehicle_power_motor = list()
            # self.vehicle_power_electric = list()
            self.vehicle_efficiency_drivetrain = list()
            self.vehicle_torque = list()
            self.vehicle_W_m = list()
            # Energy Controller
            self.EC_power_battery = list()
            self.EC_power_fuelcell = list()
            # Boost Converter
            self.power_stack = list()
            self.efficiency_bc = list()
            # Air Compressor
            self.power_aircompressor = list()
            # Pump
            self.power_pump = list()
            # Fuel Cell
            self.efficiency_stack = list()
            self.efficiency_system = list()
            self.Energy_stack = list()
            self.massflow_h2 = list()
            self.Energy_sum =list()
            # BMS
            self.battery_management_power = list()
            self.battery_management_efficiency = list()
            # Battery
            self.battery_power = list()
            self.battery_efficiency = list()
            self.battery_power_loss = list()
            self.battery_state_of_charge = list()
            self.battery_temperature = list()
            self.energy_motor = list()
            self.energy_loader = list()
            # Fuelcell
            self.energy_recuperation_f = list()
            self.energy_battery = list()
            self.energy_battery_consumption = list()
            self.energy_stack = list()
            self.energy_stack_consumption = list()
            self.energy_aircompressor = list()
            self.energy_pump = list()
            self.energy_sum = list()
            self.energy_f = list()
            self.energy_per_km_f = list()
            self.energy_per_kg_f = list()
            self.mass_h2 = list()
            self.massflow_h2 = list()
            self.eta_charger = list()

            # As long as needs_update = True simulation takes place
            if self.needs_update:
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), ' Start')

                ## Call start method (inheret from Simulatable) to start simulation
                self.start()

                ## Iteration over all simulation steps
                for t in range(0, self.duration):#self.simulation_period_hours):
                    ## Call update method to call calculation method and go one simulation step further
                    self.update()

                    # Vehicle
                    #self.vehicle_mass_cum.append(self.vehicle.mass_cum)
                    self.vehicle_power_drive.append(self.vehicle.power_drive / 1000)
                    #self.vehicle_power_loader.append(self.vehicle.power_loader_motor / 1000)
                    self.vehicle_power_motor.append(self.vehicle.power_motor / 1000)
                    self.vehicle_efficiency_drivetrain.append(self.vehicle.eta_drivetrain)
                    self.vehicle_torque.append(self.vehicle.torque)
                    self.vehicle_W_m.append(self.vehicle.W_m)
                    # Energy Controller
                    self.EC_power_battery.append(self.energycontroller.EC_power_battery / 1000)
                    self.EC_power_fuelcell.append(self.energycontroller.EC_power_fuelcell / 1000)
                    # Boost Converter
                    self.power_stack.append(self.boostconverter.power_stack / 1000)
                    self.efficiency_bc.append(self.boostconverter.efficiency_bc)
                    # Air Compressor
                    self.power_aircompressor.append(self.aircompressor.power_aircompressor / 1000)
                    # Pump
                    self.power_pump.append(self.pump.power_pump / 1000)
                    # Fuel Cell
                    self.efficiency_stack.append(self.fuelcell.efficiency_stack)
                    self.efficiency_system.append(self.FC_system.efficiency_system)
                    self.Energy_stack.append(self.fuelcell.Energy_stack / 1000)
                    massflow_h2 = self.fuelcell.massflow_h2
                    if massflow_h2 <= 0:
                        pass
                    #elif massflow_h2 > 0.000902679830747531 or massflow_h2 == np.inf: #ergibt sich aus der maximalbetriebsleistung des des FC und dem Brennwert für H2
                    #    pass
                    #elif len(self.massflow_h2) == self.duration:
                    #    pass
                    #elif len(self.massflow_h2) <= len(self.vehicle_power_drive):
                    #   pass
                    elif (massflow_h2 <= 0.000902679830747531 and massflow_h2 != np.inf
                        and len(self.massflow_h2) <= len(self.vehicle_power_drive)):
                        self.massflow_h2.append(massflow_h2)
                    self.Energy_sum.append(self.FC_system.Energy_sum / 1000)
                    # BMS
                    self.battery_management_power.append(self.battery_management.power)
                    self.battery_management_efficiency.append(self.battery_management.efficiency)
                    # Battery
                    self.battery_power.append(self.battery.power_battery / 1000)
                    self.battery_efficiency.append(self.battery.efficiency)
                    self.battery_power_loss.append(self.battery.power_loss / 1000)
                    self.battery_state_of_charge.append(self.battery.state_of_charge)
                    self.battery_temperature.append(self.battery.temperature)

                #print(sum(self.massflow_h2))
                summe_e_bat_pos = 0 #summe der batterieleistung mit positiven vorzeichen
                summe_e_bat_neg = 0
                e_bat_div_etas = [] #Batterieleistung jeder sekunde geteilt durch die effizienz
                bat_eta = []
                bms_eta = []
                for i in range(self.duration):
                    if self.battery_efficiency[i] == np.inf or self.battery_efficiency[i] == np.nan:
                        self.battery_efficiency[i] = 0
                    if self.battery_management_efficiency[i] == np.inf or self.battery_management_efficiency[i] == np.nan:
                        self.battery_management_efficiency[i] = 0
                    if self.battery_management_efficiency != 0 and self.battery_efficiency != 0:
                        if self.battery_power[i] > 0:
                            summe_e_bat_pos += (self.battery_power[i] /
                                                self.battery_management_efficiency[i] * self.battery_efficiency[i])
                        else:
                            summe_e_bat_neg += (self.battery_power[i] /
                                                self.battery_management_efficiency[i] * self.battery_efficiency[i])
                        e_bat_div_etas.append(self.battery_power[i] /
                                                self.battery_management_efficiency[i] * self.battery_efficiency[i])




                # Sum of recuperated energy [Wh]
                self.energy_recuperation_f.append(summe_e_bat_pos)

                # Sum of NETTO energy consumption of Battery [Wh]
                self.energy_battery_consumption.append(((abs(summe_e_bat_neg / 3.6 - summe_e_bat_pos / 3.6))))

                # Sum of NETTO energy demand of Battery [Wh]
                self.energy_battery.append(((abs(summe_e_bat_neg / 3.6 - summe_e_bat_pos / 3.6))))

                # Sum of energy consumption of fuel cell stack [Wh]
                self.energy_stack_consumption.append(abs(sum(x for x in self.power_stack if x < 0)) / 3.6)

                # Sum of energy consumption of air compressor [Wh]
                self.energy_aircompressor.append(abs(sum(x for x in self.power_aircompressor if x < 0)) / 3.6)

                # Sum of energy consumption of pump [Wh]
                self.energy_pump.append(abs(sum([x for x in self.power_pump if x < 0])) / 3.6)

                # Sum of energy input for fuel cell stack [Wh]
                self.energy_stack.append(abs(sum([x for x in self.Energy_stack if x < 0])) / 3.6)

                # Sum of energy input for fuel cell system [Wh]
                self.energy_sum.append(abs(sum([x for x in self.Energy_sum if x > 0])) / 3.6)

                # Sum of energy of H2WCV[Wh]
                self.energy_f.append((((abs(summe_e_bat_neg / 3.6 -
                    summe_e_bat_pos / 3.6)) + abs(sum([x for x in self.Energy_stack if x < 0])) / 3.6)))

                # Specific energy per distance [Wh/m] or [kWh/km]
                self.energy_per_km_f.append((((abs(summe_e_bat_neg / 3.6 - summe_e_bat_pos / 3.6))
                                              + abs(sum([x for x in self.Energy_stack if x < 0])) / 3.6)
                                             / self.route.profile_day.distance))

                ## Simulation over: set needs_update to false and call end method
                results_parameter = {'energy_motor': self.energy_motor,
                                      'energy_recuperation_f': self.energy_recuperation_f,
                                      'energy_battery': self.energy_battery,
                                      'energy_battery_consumption': self.energy_battery_consumption,
                                      'energy_stack_consumption': self.energy_stack_consumption,
                                      'energy_stack': self.energy_stack,
                                      'energy_aircompressor': self.energy_aircompressor,
                                      'energy_pump': self.energy_pump,
                                      'energy_sum': self.energy_sum,
                                      'energy_f': self.energy_f,
                                      'energy_per_km_f': self.energy_per_km_f,
                                      'mass_h2': sum(self.massflow_h2)
                                      #'massflow_h2': self.massflow_h2
                                      }

                ## Result powerflow data
                ###########################################################################
                # Summarize route data

                results_powerflows = {'route_distance': self.route.profile_day.distance,
                                      'vehicle_power_drive': self.vehicle_power_drive,
                                      'vehicle_power_motor': self.vehicle_power_motor,
                                      'vehicle_eta': self.vehicle_efficiency_drivetrain,
                                      'vehicle_torque': self.vehicle_torque,
                                      'vehicle_W_m': self.vehicle_W_m,
                                      'EC_power_battery': self.EC_power_battery,
                                      'EC_power_fuelcell': self.EC_power_fuelcell,
                                      'power_stack': self.power_stack,
                                      'efficiency_bc': self.efficiency_bc,
                                      'power_aircompressor': self.power_aircompressor,
                                      'power_pump': self.power_pump,
                                      'efficiency_stack': self.efficiency_stack,
                                      'efficiency_system': self.efficiency_system,
                                      'Energy_stack': self.Energy_stack,
                                      'Energy_sum': self.Energy_sum,
                                      'battery_management_power': self.battery_management_power,
                                      'battery_management_eta': self.battery_management_efficiency,
                                      'battery_power': self.battery_power,
                                      'efficiency_b-f': (0.9190 * np.mean(self.battery_management_efficiency) * np.mean(self.battery_efficiency)),
                                      #'battery_c-rate': abs((np.array(self.battery_power) / Battery.capacity_nominal_wh)),
                                      'battery_soc': self.battery_state_of_charge,
                                      'battery_eta': self.battery_efficiency,
                                      'massflow_h2': self.massflow_h2}

                #data_mass = pd.DataFrame(self.massflow_h2)
                #data_mass.to_csv("results/Dataframe_massflow.csv")

                file_name = str('results/power_flows__'+self.routen_profil+'.pkl')
                output = open(file_name, 'wb')
                pickle.dump(results_powerflows, output)
                output.close()

                # Save results parameter dict
                file_name = 'results/parameter__'+self.routen_profil+'.pkl'
                output = open(file_name, 'wb')
                pickle.dump(results_parameter, output)
                output.close()

                self.needs_update = False
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S'), ' End')
                self.end()