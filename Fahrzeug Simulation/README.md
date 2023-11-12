
# Toyota Mirai I Simulation


## Kontext

In dieser Simulation wird der Toyota Mirai I mit seinen Komponenten abgebildet und sein Fahrverhalten simuliert. 

## Aufbau


Die einzelnen Klassen der Komponenten, befinden sich im Ordner "componentents/", ihre Daten werden aus dem Ordner "data/" geladen.
"Main.py" ist die Hauptsimulation, welche auf die Parent-Klassen "simulatable" und "serializable" zurückgreift, die in "simulation.py"
ausgeführt werden. Die Routenprofile werden im Ordner "Routenauslegung/data" ausgelesen und die Tagesverteilung für die aufbauende Simulation erzeugt.
Die aus der Simulation entstandenen Daten, werden im Ordner "results/" gespeichert.

## Rechte
Die Simulation beruht auf dem Modell "Refuse Collection Vehicle Simulation" (siehe unten und "license.txt").












# Refuse Collection Vehicle Simulation

### About

This tool includes an object oriented programmed energy demand simulation of a waste collection vehicle. The backwards simulation has a resolution of one second. All related power flows of the vehicle are modeled and can be analyzed.  

### Features

1. Models for electric driven vehicle drivetrains, the vehicle body, the vehicle route and in case of an electric vehicle a battery, battery management and charger model included, and in case of a fuel cell vehicle a fuel cell stack, a pump, an air compressor, a boost converter and an energy controller included. 

   *All component models stored in the folder components.*

2. Models are fully serializable, component parameter are stored in json files.

   *All model parameters stored in the folder data/components*

3. Vehicle route is synthesized on route parameter and normalized driven cycles.

   *Route parameters are stored in the folder data/load*

   

### Getting started

Sample component and route data is provided. Test simulation can be started with file *MAIN.py*, results will be stored in folder *results* and include general evaluation parameters as energy consumption and detailed timeseries powerflows of all relevant components.



###  Remark

The simulation tool was developed during a research project. Research results obtained on the basis of the model will be published in the upcoming months and will be referenced here.





