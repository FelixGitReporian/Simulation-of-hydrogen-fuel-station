import pandas as pd
from simulation import Simulation

# Define simulation parameters
# Tour data
# zentrale Stadt
route_stadt = pd.read_csv("Routenauslegung/data/Cycle_Stadt1.csv", sep=";")
route_stadt.columns = ["v", "a", "s"]
t_route_stadt = int(len(route_stadt["v"]))
distance_route_stadt = route_stadt["s"][float(len(route_stadt["v"]))-1]

# mittel Stadt
route_m_stadt = pd.read_csv("Routenauslegung/data/Cycle_MittelStadt1.csv", sep=";")
route_m_stadt.columns = ["v", "a", "s"]
t_route_m_stadt = int(len(route_m_stadt["v"]))
distance_route_m_stadt = route_m_stadt["s"][float(len(route_m_stadt["v"]))-1]

# klein Stadt
route_k_stadt = pd.read_csv("Routenauslegung/data/Cycle_KleinStadt1.csv", sep=";")
route_k_stadt.columns = ["v", "a", "s"]
t_route_k_stadt = int(len(route_k_stadt["v"]))
distance_route_k_stadt = route_k_stadt["s"][float(len(route_k_stadt["v"]))-1]

#routenprofil: name der Route zum Speichern
data_route = {'overall_distance': distance_route_stadt,
              'duration': t_route_stadt,"routenprofil": "route_zstadt"}

# Create Simulation instance
sim = Simulation(data_route)
# Call Main Simulation method
sim.simulate()