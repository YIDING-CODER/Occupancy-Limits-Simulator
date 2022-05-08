# Occupancy Limits Simulator

A ‘scatter charts’ (dots and circles in coordinate system, within a rectangular boundary) to show positioning of 16 occupant in a room measuring 6x8m every 20 seconds for 3 hours, and distancing incidents + GIF sequence.

## Features

- Generate simulation data, gif based on the given configuation file
- Export part of the simulation data using helper_tool.py
- Generate Grid image using export_grid_image.py

## Tech

The program is wriiten in Python3 and required the following library installed:
- matplotlib
- pandas
- Shapely
- descartes
- imageio
- Pillow
- natsort


## File Structures

```
├── data
│   ├── Senario_Time_Stamp
│      ├── images
│      |  └── 0..N.png
│      ├── Senario_Time_Stamp.csv
│      ├── Senario_Time_Stamp.gif
│      └── Senario_Time_Stamp.ini
├── configure.ini
├── requirments.txt
├── simulator.py
├── helper_tool.py
├── export_grid_image.py
└── ReadMe.md
```

| File | Description |
| ------ | ------ |
| ```0..N.png``` | All the export images will be stored under data/Senario_Time_Stamp/images. |
| ```Senario_Time_Stamp.csv``` | Simulator output data for Senario 0 to N.|
| ```Senario_Time_Stamp.gif``` | Gif image generated based on all the senario png in data/Senario_Time_Stamp/images folder.|
| ```Senario_Time_Stamp.ini``` | A copy of the configuation file for that particular run|
| ```configure.ini``` | This is where user set up the behavior of the simulator. |
| ```requirments.txt``` | All the dependencies reqired for this python program, see the Installation section to insall the dependencies. |
| ```simulator.py``` |The main Simulator python script. |
| ```export_grid_image.py``` | Generate grid images by providing the senario ranges. |
| ```helper_tool.py``` | A helper tool to export part of the simulation data by providing the senario range.
| ```ReadMe.md``` | Documentation file. |

## Installation

Install the dependencies.

```sh
pip install -r requirements.txt
```

## Run the Simulation

After install the dependecies libraries, you can run the simulator using following command.

```sh
python simulator.py
```
## Run the Helper_Tool
A helper tool to export part of the simulation data by providing the senario range. Follow the instructions in the terminal screen to export the data. Use ```control```+```z``` to exit program.

```sh
python helper_tool.py
```
## Run the export_grid_image.py
A helper tool to export part of the simulation data by providing the senario range.Follow the instructions in the terminal screen to export the grid image. 

```sh
python export_grid_image.py
```

## Simulator Configuration
Below is the content of the ```conigure.ini```, the settings in this file will affect the behaviors of the simulator.
```sh
[SETTING]
NUMBER_OF_OCCUPANCY=16
ROOM_WIDTH= 9.6
ROOM_HEIGHT= 6
GRID_SIZE=0.6
DURATION_OF_ACTIVITY=180
COUNT_FREQENCY=20
INCIDENT_THRESHOLD=60
DISTANCE_NORM=0.75
BLOCKED_AREAS=[(4,2,5,10),(7,2,8,10),(10,2,11,10),(13,2,14,10)]
```
**[SETTING]**
- The value of ```NUMBER_OF_OCCUPANCY```is integer.
- The unit of ```ROOM_WIDTH```, ```ROOM_HEIGHT```, ```GRID_SIZE```, ```DISTANCE_NORM``` is meter
    - ```GRID_SIZE``` defines the unit size of grid system 
    - ```DISTANCE_NORM``` defines the radius of Occupancy
- The unit of ```DURATION_OF_ACTIVITY``` is ```minutes``` and it defines the length of the simulation. 
- The unit of ```COUNT_FREQENCY``` and ```INCIDENT_THRESHOLD``` is ```seconds```
    -  ```COUNT_FREQENCY``` defines the frequency of generating the senario
    -  ```INCIDENT_THRESHOLD``` defines what is the distance incident.
- The ```BLOCKED_AREA``` defines the restricted area on the map. Each block is defined by it's ```gird  position``` (```left_bottom_x```,```left_bottom_y```,```right_top_x```,```right_top_y```) .


## Developer Notes

When runing the ```simulation.py```, you will get the following warning. It needs to be fixed if you are using Shaprely 2.0.

```
ShapelyDeprecationWarning: The array interface is deprecated and will no longer work in Shapely 2.0. Convert the '.coords' to a numpy array instead.
```




