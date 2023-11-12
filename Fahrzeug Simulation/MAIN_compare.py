import pandas as pd
import numpy as np
import pickle
from collections import OrderedDict

from simulation import Simulation
from components.charger import Charger
from components.power_component import Power_Component
from components.battery import Battery
from components.fuelcell_charger_battery import Charger_fc


## Define simulation parameters
###############################################################################
# Tour data
data_route = pd.read_pickle('data/load/Tour_suburb_short.pkl')


## Initialization of list containers to store different tour simulation results
# Route
route_distance = list()
waste_mass = list()
energy_motor = list()
energy_loader = list()
# Electro
energy_recuperation = list()
energy_consumption = list()
energy = list()
energy_per_km = list()
energy_per_kg = list()
# Fuelcell
energy_recuperation_f = list()
energy_battery = list()
energy_battery_consumption = list()
energy_stack = list()
energy_stack_consumption = list()
energy_aircompressor = list()
energy_pump = list()
energy_sum = list()
energy_f = list()
energy_per_km_f = list()
energy_per_kg_f = list()
mass_h2 = list()




for key in data_route.keys():
    data_route0 = data_route[key]
    # Create Simulation instance
    sim = Simulation(data_route0)
    # Call Main Simulation method
    sim.simulate()

    # Route distance
    route_distance.append(data_route0['overall_distance'])
    # Waste mass collected
    waste_mass.append((max(sim.vehicle_mass_cum) - sim.vehicle.mass_empty))
    # Sum of energy consumption for vehicle motor
    energy_motor.append(abs(sum([x for x in sim.vehicle_power_motor if x > 0])) / 3.6)
    # Sum of energy consumption for vehicle loader
    energy_loader.append(abs(sum([x for x in sim.vehicle_power_loader if x > 0])) / 3.6)

    if sim.vehicle.specification == 'vehicle_electric':
        ## ELECTRO
        charger = Charger(power_grid=22000,
                          file_path='data/components/charger_ac.json')
        charger.calculate()

        bms = Power_Component(timestep=1,
                              input_link=charger,
                              input_link1=sim.vehicle,
                              file_path='data/components/battery_management.json')
        bms.calculate()

        battery = Battery(timestep=1,
                          input_link=bms,
                          file_path='data/components/battery_lfp_ele.json')
        battery.calculate()

        # Sum of recuperated energy [Wh]
        energy_recuperation.append(sum([x for x in sim.battery_power if x > 0]) / 3.6)
        # Sum of BRUTTO energy consumption (without recuperation) [Wh]
        energy_consumption.append(abs(sum([x for x in sim.battery_power if x < 0]))  / 3.6)
        # Sum of NETTO energy consumption [Wh]
        energy.append((abs(sum([x for x in sim.battery_power if x < 0]) / 3.6)
                       - (sum([x for x in sim.battery_power if x > 0]))  / 3.6) \
                       / (charger.efficiency * bms.efficiency * battery.efficiency))
        # Spesific energy per distance [Wh/m] or [kWh/km]
        energy_per_km.append((abs(sum([x for x in sim.battery_power if x < 0]) / 3.6)
                       - (sum([x for x in sim.battery_power if x > 0]))  / 3.6) \
                       / (charger.efficiency * bms.efficiency * battery.efficiency) / data_route0['overall_distance'])
        # Specific energy per kg waste [Wh/kg] or [kWh/t]
        energy_per_kg.append((abs(sum([x for x in sim.battery_power if x < 0]) / 3.6)
                       - (sum([x for x in sim.battery_power if x > 0]))  / 3.6) \
                       / (charger.efficiency * bms.efficiency * battery.efficiency) / (max(sim.vehicle_mass_cum) - sim.vehicle.mass_empty))

        ## Result powerflow data
        ###########################################################################
        # Summarize route data
        results_powerflows = pd.DataFrame(
            data=OrderedDict({'route_type': sim.route.profile_day.phase_type,
                              'route_speed': sim.route.profile_day.speed,
                              'route_acceleration': sim.route.profile_day.acceleration,
                              'route_distance': sim.route.profile_day.distance,
                              'route_loader_active': sim.route.profile_day.loader_active,
                              'route_container_mass': sim.route.profile_day.container_mass,
                              'vehicle_mass_cum': sim.vehicle_mass_cum,
                              'vehicle_power_drive': sim.vehicle_power_drive,
                              'vehicle_power_loader': sim.vehicle_power_loader,
                              'vehicle_power_motor': sim.vehicle_power_motor,
                              'vehicle_eta': sim.vehicle_efficiency_drivetrain,
                              'vehicle_torque': sim.vehicle_torque,
                              'vehicle_W_m': sim.vehicle_W_m,
                              'battery_management_power': sim.battery_management_power,
                              'battery_management_eta': sim.battery_management_efficiency,
                              'battery_power': sim.battery_power,
                              'battery_c-rate': abs((np.array(sim.battery_power) / sim.battery.capacity_nominal_wh)),
                              'battery_soc': sim.battery_state_of_charge,
                              'battery_eta': sim.battery_efficiency}))

        # Set Datetimeindex
        datetimeindex_day = pd.date_range('01.01.2020 07:00:00', periods=len(sim.route.profile_day.speed), freq='S')
        results_powerflows['date'] = datetimeindex_day
        results_powerflows = results_powerflows.set_index('date')

    elif sim.vehicle.specification =='vehicle_fuelcell':
        ## Fuel Cell
        charger = Charger_fc(power_stack=10000,
                             file_path='data/components/fuelcell_charger_battery.json')
        charger.calculate()

        bms = Power_Component(timestep=1,
                              input_link=charger,
                              input_link1=sim.vehicle,
                              input_link2=sim.aircompressor,
                              input_link3=sim.pump,
                              file_path='data/components/battery_management.json')
        bms.calculate()

        battery = Battery(timestep=1,
                          input_link=bms,
                          file_path='data/components/battery_lfp_fuel.json')
        battery.calculate()

        # Sum of recuperated energy [Wh]
        energy_recuperation_f.append(sum([x for x in sim.battery_power if x > 0]) / 3.6)
        # Sum of NETTO energy consumption of Battery [Wh]
        energy_battery_consumption.append(((abs(sum([x for x in sim.battery_power if x < 0])) / 3.6 - sum([x for x in sim.battery_power if x > 0]) / 3.6)))
        # Sum of NETTO energy demand of Battery [Wh]
        energy_battery.append(((abs(sum([x for x in sim.battery_power if x < 0])) / 3.6 - sum([x for x in sim.battery_power if x > 0]) / 3.6)) \
                                               / (charger.efficiency * bms.efficiency * battery.efficiency))
        # Sum of energy consumption of fuel cell stack [Wh]
        energy_stack_consumption.append(abs(sum(x for x in sim.power_stack if x < 0)) / 3.6)
        # Sum of energy consumption of air compressor[Wh]
        energy_aircompressor.append(abs(sum(x for x in sim.power_aircompressor if x < 0)) / 3.6)
        # Sum of energy consumption of pump [Wh]
        energy_pump.append(abs(sum([x for x in sim.power_pump if x < 0])) / 3.6)
        # Sum of energy input for fuel cell stack [Wh]
        energy_stack.append(abs(sum([x for x in sim.Energy_stack if x < 0])) / 3.6)
        # Sum of energy input for fuel cell system [Wh]
        energy_sum.append(abs(sum([x for x in sim.Energy_sum if x > 0])) / 3.6)
        # Sum of NETTO energy consumption [Wh]
        energy_f.append((((abs(sum([x for x in sim.battery_power if x < 0])) / 3.6 - sum([x for x in sim.battery_power if x > 0]) / 3.6)) \
                        / (charger.efficiency * bms.efficiency * battery.efficiency) + abs(sum([x for x in sim.Energy_stack if x < 0])) / 3.6) / charger.efficiency_com_tran)
        # Specific energy per distance [Wh/m] or [kWh/km]
        energy_per_km_f.append((((abs(sum([x for x in sim.battery_power if x < 0])) / 3.6 - sum([x for x in sim.battery_power if x > 0]) / 3.6))
                                / (charger.efficiency * bms.efficiency * battery.efficiency) + abs(sum([x for x in sim.Energy_stack if x < 0])) / 3.6) / charger.efficiency_com_tran / data_route0['overall_distance'])
        # Specific energy per kg waste [Wh/kg] or [kWh/t]
        energy_per_kg_f.append((((abs(sum([x for x in sim.battery_power if x < 0])) / 3.6 - sum([x for x in sim.battery_power if x > 0]) / 3.6))
                                / (charger.efficiency * bms.efficiency * battery.efficiency) + abs(sum([x for x in sim.Energy_stack if x < 0])) / 3.6) / charger.efficiency_com_tran / (max(sim.vehicle_mass_cum) - sim.vehicle.mass_empty))
        # Sum of H2 consumption [kg]
        mass_h2.append((((abs(sum([x for x in sim.battery_power if x < 0])) / 3.6 - sum([x for x in sim.battery_power if x > 0]) / 3.6))
                        / (charger.efficiency * bms.efficiency * battery.efficiency) + abs(sum([x for x in sim.Energy_stack if x < 0])) / 3.6) / charger.efficiency_com_tran * 3600 / 1.4188e8)

        ## Result powerflow data
        ###########################################################################
        # Summarize route data
        results_powerflows = pd.DataFrame(
            data=OrderedDict({'route_type': sim.route.profile_day.phase_type,
                              'route_speed': sim.route.profile_day.speed,
                              'route_acceleration': sim.route.profile_day.acceleration,
                              'route_distance': sim.route.profile_day.distance,
                              'route_loader_active': sim.route.profile_day.loader_active,
                              'route_container_mass': sim.route.profile_day.container_mass,
                              'vehicle_mass_cum': sim.vehicle_mass_cum,
                              'vehicle_power_drive': sim.vehicle_power_drive,
                              'vehicle_power_loader': sim.vehicle_power_loader,
                              'vehicle_power_motor': sim.vehicle_power_motor,
                              'vehicle_eta': sim.vehicle_efficiency_drivetrain,
                              'vehicle_torque': sim.vehicle_torque,
                              'vehicle_W_m': sim.vehicle_W_m,
                              'EC_power_battery': sim.EC_power_battery,
                              'EC_power_fuelcell': sim.EC_power_fuelcell,
                              'power_stack': sim.power_stack,
                              'efficiency_bc': sim.efficiency_bc,
                              'power_aircompressor': sim.power_aircompressor,
                              'power_pump': sim.power_pump,
                              'efficiency_stack': sim.efficiency_stack,
                              'efficiency_system': sim.efficiency_system,
                              'Energy_stack': sim.Energy_stack,
                              'massflow_h2': sim.massflow_h2,
                              'battery_management_power': sim.battery_management_power,
                              'battery_management_eta': sim.battery_management_efficiency,
                              'battery_power': sim.battery_power,
                              'efficiency_b-f': (charger.efficiency * bms.efficiency * battery.efficiency),
                              'battery_c-rate': abs((np.array(sim.battery_power) / sim.battery.capacity_nominal_wh)),
                              'battery_soc': sim.battery_state_of_charge,
                              'battery_eta': sim.battery_efficiency}))

        # Set Datetimeindex
        datetimeindex_day = pd.date_range('01.01.2020 07:00:00', periods=len(sim.route.profile_day.speed), freq='S')
        results_powerflows['date'] = datetimeindex_day
        results_powerflows = results_powerflows.set_index('date')

    else:
        print('No vehicle type specified in json file')

if sim.vehicle.specification == 'vehicle_electric':
    results_parameter = pd.DataFrame(
        data=OrderedDict({'route_distance': route_distance,
                          'waste_mass': waste_mass,
                          'energy_motor': energy_motor,
                          'energy_loader': energy_loader,
                          'energy_recuperation': energy_recuperation,
                          'energy_consumption': energy_consumption,
                          'energy': energy,
                          'energy_per_km': energy_per_km,
                          'energy_per_kg': energy_per_kg}))

elif sim.vehicle.specification == 'vehicle_fuelcell':
    results_parameter = pd.DataFrame(
        data=OrderedDict({'route_distance': route_distance,
                          'waste_mass': waste_mass,
                          'energy_motor': energy_motor,
                          'energy_loader': energy_loader,
                          'energy_recuperation_f': energy_recuperation_f,
                          'energy_battery_consumption': energy_battery_consumption,
                          'energy_battery': energy_battery,
                          'energy_stack_consumption': energy_stack_consumption,
                          'energy_stack': energy_stack,
                          'energy_aircompressor': energy_aircompressor,
                          'energy_pump': energy_pump,
                          'energy_sum': energy_sum,
                          'energy_f': energy_f,
                          'energy_per_km_f': energy_per_km_f,
                          'energy_per_kg_f': energy_per_kg_f,
                          'mass_h2': mass_h2}))

# Save all daytour dicts to pkl
##############################################################################
# Save results powerflow dict
file_name = 'results/EDS_power_flows_tour4_'+sim.vehicle.specification+'.pkl'
output = open(file_name, 'wb')
pickle.dump(results_powerflows, output)
output.close()

# Save results parameter dict
file_name = 'results/EDS_parameter_tour4_'+sim.vehicle.specification+'.pkl'
output = open(file_name, 'wb')
pickle.dump(results_parameter, output)
output.close()