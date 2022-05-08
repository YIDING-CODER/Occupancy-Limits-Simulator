import pandas as pd
import numpy as np
import os
import math
import random
import ast
from datetime import datetime

# Read the configuration file
import configparser
config = configparser.ConfigParser()
config.read('configure.ini')


# New Simulation folder data
folder_name=datetime.now().strftime("%Y%m%d_%H%M%S")


print("Step1: Loading Configuation File")
# Load configuration file
NUMBER_OF_OCCUPANCY=int(config["SETTING"]["NUMBER_OF_OCCUPANCY"])
GRID_SIZE=float(config["SETTING"]["GRID_SIZE"])
ROOM_WIDTH=float(config["SETTING"]["ROOM_WIDTH"])/GRID_SIZE
ROOM_HEIGHT=float(config["SETTING"]["ROOM_HEIGHT"])/GRID_SIZE
DURATION_OF_ACTIVITY=int(config["SETTING"]["DURATION_OF_ACTIVITY"])
COUNT_FREQENCY=int(config["SETTING"]["COUNT_FREQENCY"])
INCIDENT_THRESHOLD=int(config["SETTING"]["INCIDENT_THRESHOLD"])/COUNT_FREQENCY
DISTANCE_NORM=float(config["SETTING"]["DISTANCE_NORM"])
BLOCKED_AREAS=list(ast.literal_eval(config["SETTING"]["BLOCKED_AREAS"]))
NUMBER_OF_SENARIO=int(DURATION_OF_ACTIVITY*60/COUNT_FREQENCY)+1

# Create folder if not existed
if not os.path.exists("data/"+folder_name):
    os.makedirs("data/"+folder_name)
    
if not os.path.exists("data/"+folder_name+"/images"):
    os.makedirs("data/"+folder_name+"/images")

with open("data/"+folder_name+"/"+folder_name+".ini", "w") as configfile:
    config.write(configfile)


# Calculate the distance between point a and b.
def distance(a,b):
    x_1,y_1=a
    x_2,y_2=b
    sq1 = (x_1-x_2)*(x_1-x_2)
    sq2 = (y_1-y_2)*(y_1-y_2)
    return math.sqrt(sq1 + sq2)

# Check whether a point is inside rectangle area
def check_inside(rectangle,point):
    x1,y1,x2,y2=rectangle
    px,py=point
    if px > x1 and px < x2 and py > y1 and py < y2:
        return True
    else:
        return False
    
# Check whether a point is on the edge of rectangle area
def on_edge(rectangle,point):
    x1,y1,x2,y2=rectangle
    px,py=point
    if (x1<=px<=x2 and (py==y1 or py==y2)) or (y1<=py<=y2 and (px==x1 or px==x2)):
        return True
    else:
        return False



class Room():
    def __init__(self,width,height,blocked_area):
        self.width=width
        self.height=height
        self.occupants=[]
        self.distance_incident={}
        self.blocked_area=blocked_area
        
    # get the data about the room
    def get_data(self):
        result={}
        columns=[]
        columns.append("#intersections")
        columns.append("#distance_incidents")
        columns.append("total_area")
        for occupant in self.occupants:
            o_name=occupant.get_name()
            columns.append(o_name)
            result[o_name]=occupant.get_position()
        
        total_area=0
        number_of_intersection=0
        number_of_distance_incident=0
        for key in self.distance_incident:
            o1,o2=key
            intersect_name=o1.get_name()+o2.get_name()
            columns.append(intersect_name)
            di=self.distance_incident[key]
            is_di,continuity, area=di
            if continuity>0:
                number_of_intersection+=1
            if continuity>=INCIDENT_THRESHOLD:
                number_of_distance_incident+=1
                total_area+=area
            result[intersect_name]=di
        


        result["#intersections"]=number_of_intersection
        result["#distance_incidents"]=number_of_distance_incident
        result["total_area"]=total_area
        return columns, result
    
    def is_valid(self,location,mid_location):
        x,y=location
        if x<0 or x>self.width or y<0 or y>self.height:
            return False
        
        # Block here
        
        for block in self.blocked_area:
            if check_inside(block,mid_location):
                return False
            elif on_edge(block,mid_location) and on_edge((0,0,self.width,self.height),mid_location):
                return False
        
        for cur_occupant in self.occupants:
            if cur_occupant.get_position()==location:
                return False
        
        return True
    
    def initialise_occupant(self,number_of_occupant):
        for i in range(number_of_occupant):
            valid=False
            while not valid:
                x=random.randint(0, self.width)
                y=random.randint(0, self.height)
                if self.is_valid((x,y),(x,y)):
                    occupant=Occupant(x,y,DISTANCE_NORM/GRID_SIZE,chr(ord('A')+i))
                    self.occupants.append(occupant)
                    valid=True
        self.calculate_intersection()
            
        
    def add_occupant(self,occupant):
        self.occupants.append(occupant)
        
        
    def update(self):
        for occupant in self.occupants:
            moved=False
            while not moved:
                current_location=occupant.get_position()
                new_location=occupant.get_next_position()
                if new_location==current_location:
                    moved=True    
                else:
                    cx,cy=current_location
                    nx,ny=new_location
                    middle=(cx+nx)/2,(cy+ny)/2
                    if self.is_valid(new_location,middle):
                        occupant.move(new_location)
                        moved=True
        self.calculate_intersection()
        
        
    def get_occupants(self):
        return self.occupants
    
    def get_occupants_position(self):
        result=[]
        for occupant in self.occupants:
            result.append(occupant.get_position())
        return result
    
    def calculate_intersection(self):
        for index,occupant_1 in enumerate(self.occupants):
            for occupant_2 in self.occupants[index+1:]:
                area=self.calculate_area(occupant_1,occupant_2)
                is_distance_incident,continuity,_=self.distance_incident.get((occupant_1,occupant_2),(0,0,0))
                
                # When two circle are intersected
                if area!=0:
                    current_continuity=continuity+1
                    if current_continuity>=INCIDENT_THRESHOLD:
                        is_distance_incident=1

                    self.distance_incident[(occupant_1,occupant_2)]=is_distance_incident,current_continuity,area
                else:
                    self.distance_incident[(occupant_1,occupant_2)]=0,0,area
                    
        return self.distance_incident

    def get_distance_incident(self):
        result={}
        for key in self.distance_incident:
            _,continuity,_=self.distance_incident[key]
            
            if continuity>=INCIDENT_THRESHOLD:
                result[key]=self.distance_incident[key]
                
        return result 
                

    # Calculate the intersection area of two circle. The origin of circles must be different.
    def calculate_area(self,cicle_a,cicle_b):
        a_x,a_y=cicle_a.get_position()
        a_x*=GRID_SIZE
        a_y*=GRID_SIZE
        b_x,b_y=cicle_b.get_position()
        b_x*=GRID_SIZE
        b_y*=GRID_SIZE
        d=distance((a_x,a_y),(b_x,b_y))
        a_radius=cicle_a.get_radius()*GRID_SIZE
        b_radius=cicle_b.get_radius()*GRID_SIZE
        if d<a_radius+b_radius:
            a=a_radius*a_radius
            b=b_radius*b_radius
            x=(a - b + d * d) / (2 * d)
            z=x*x
            y=math.sqrt(a-z)
            if d<=abs(b_radius-a_radius):
                return math.pi*min(a,b)
            return a * math.asin(y / a_radius) + b * math.asin(y /b_radius) - y * (x + math.sqrt(z + b - a))
        else:
            return 0
    
class Occupant():
    def __init__(self,x,y,radius,name):
        self.x=x
        self.y=y
        self.radius=radius
        self.neighbor=[]
        self.name=name
        
    def get_position(self):
        return self.x, self.y
    def move(self,new_location):
        self.x,self.y=new_location
    def get_radius(self):
        return self.radius
        
    def get_next_position(self):
        directions=[(0,0),(1,0),(-1,0),(0,1),(0,-1)]
        x_delta,y_delta=random.choice(directions)
        return self.x+x_delta,self.y+y_delta
    
    def get_name(self):
        return self.name

    def is_intersected():
        pass
    def is_incident():
        pass
    
        
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import shapely.geometry as sg
import descartes

def generate_image(file_name,room,labels):
    fig, ax = plt.subplots()
    ax = plt.subplot(111)
    ax.grid(linestyle = '-', linewidth = 1,zorder=-1)
    ax.set_xticks(np.arange(0, ROOM_WIDTH+1, 1))
    ax.set_xticklabels([str(round(item*GRID_SIZE,1)) for item in np.arange(0, ROOM_WIDTH+1, 1)])
    ax.set_yticks(np.arange(0, ROOM_HEIGHT+1, 1))
    ax.set_yticklabels([str(round(item*GRID_SIZE,1)) for item in np.arange(0, ROOM_HEIGHT+1, 1)])
    plt.xlim([0,ROOM_WIDTH])
    plt.ylim([0,ROOM_HEIGHT])
    ax.set_aspect('equal', 'box')


    # Draw Block Area
    
    for block in BLOCKED_AREAS:
        x1,y1,x2,y2=block
        rect = mpatches.Rectangle((x1, y1), x2-x1, y2-y1, color="grey",zorder=5)
        # Add the patch to the Axes
        ax.add_patch(rect)
    
    # Add dot to cicle
    scat=ax.scatter([], [], color='b',zorder=11,clip_on=False)
    scat.set_offsets(room.get_occupants_position())


    # Plot Cicle
    occupants=room.get_occupants()
    for occupant in occupants:
        circle = mpatches.Circle(occupant.get_position(),occupant.get_radius(), facecolor="r",edgecolor='b',fill=False,zorder=10,clip_on=True)
        ax.annotate(occupant.get_name(),np.add(occupant.get_position(),(0,0.3)),size=10,zorder=12,annotation_clip=False)
        ax.add_patch(circle)

    # add place holder on the top of the image, so there is always some space on the top of the image.
    ax.annotate("`",np.add((0,ROOM_HEIGHT),(-0.1,0.3)),size=10,zorder=12,annotation_clip=False,color="white")
    
    # Draw distance incident
    distance_incidents=room.get_distance_incident()
    for key in distance_incidents:
        occ1,occ2=key
        a = sg.Point(occ1.get_position()).buffer(occ1.get_radius())
        b = sg.Point(occ2.get_position()).buffer(occ2.get_radius())
        middle = a.intersection(b)
        ax.add_patch(descartes.PolygonPatch(middle, fc='r', ec='k'))
    
    # Add label to diagram    
    l_x=0.1
    l_y=0
    padding=[0.15,0.25,0.2]
    for index,label in enumerate(labels):
        fig.text(l_x, l_y, label)
        l_x+=padding[index]

    fig.savefig(file_name,bbox_inches ="tight")   
    plt.close(fig)


print("Step2: Starting Simulation")
room=Room(ROOM_WIDTH, ROOM_HEIGHT,BLOCKED_AREAS)
room.initialise_occupant(NUMBER_OF_OCCUPANCY)
data=[]
for i in range(NUMBER_OF_SENARIO):
    file_name="data/"+folder_name+"/"+"images/"+str(i)+".png"
    columns,row_data=room.get_data()
    row_data["senario"]=i
    data.append(row_data)
    
    labels=[]
    labels.append("senario: "+str(i))
    labels.append("total_area: "+str(round(row_data["total_area"],2))+"$m^2$")
    labels.append("#incidents/#intersections: "+str(row_data["#distance_incidents"])+"/"+str(row_data["#intersections"]))
    generate_image(file_name,room,labels)
    room.update()

    if i%20==0:
        print("Number of Senario Generated: {}/{}".format(str(i+1),NUMBER_OF_SENARIO))

    

print("Step3: Exporting simulation data")
import pandas as pd
columns.insert(0,"senario")
df=pd.DataFrame(data,columns=columns)

columns.insert(4,"acc_area")
df["acc_area"]=df['total_area'].cumsum()
df=df[columns]
df.to_csv("data/"+folder_name+"/"+folder_name+".csv",index=None)


print("Step4: Generating Gif")
import imageio
from natsort import natsorted
import glob
image_list=glob.glob("data/"+folder_name+"/images/*.png")
image_list=natsorted(image_list)

images = []
for file_name in image_list:
    images.append(imageio.imread(file_name))
imageio.mimsave("data/"+folder_name+"/"+folder_name+".gif", images)

print("Simulation Completed")