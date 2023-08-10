#Author:  Gonca Ezgi Cakır
#Date:  20.04.2021
#Class:  Graduation Project II
#Project:  Kampus Ici Otonom Araclarla Ulasim Simulasyonu

#File:  greedy_cvrp.py - contains envoirment and greedy solution


#import carla library
import glob
import os
import sys
import math
import random
from time import*
import threading

try:
    sys.path.append(glob.glob('../../carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

#import source files
from passenger import Passenger
from vehicle import Vehicle
import diGraph as diGraph


#GLOBALS----------------------------------------------------------------------------------

#there are 36 stops 
#holds number of passenger at each stop (start anf final)
passengers_at_stops_start = [0] * 36
passengers_at_stops_final = [0] * 36
passengers_at_main_stops_start = [0] * 3 #(index 0 is empty, only to store S1 ans S2)
passengers_at_main_stops_final = [0] * 3 #(index 0 is empty, only to store S1 ans S2)

vehicleList = []
passengerList = []
stopList = [] 
mainStopList = [] 
global campusGraph

#thread's global variable
global time_counter
#thread sync locks
lock1 = threading.Lock()
lock2 = threading.Lock()


#THREADS ---------------------------------------------------------------------------------

#thread to simulate time during simulation
def timeCounter():

    global time_counter 
    time_counter = 0
   
    for i in range(30):
        lock1.acquire()
        time_counter = time_counter + 1
        #print("counter:", time_counter)
        sleep(15) 
        lock2.release()

    print("out of time")


#thread to simulate time during simulation
def spawning(world):

    global passengerList 
    
    for i in range(len(passengerList)):
        
        lock2.acquire()
        #print(time_counter)
        
        dist=0.0
        for i in range(len(passengerList)):
           
            if(passengerList[i].spawnTime == time_counter):
                #print("create passenger id", passengerList[i].id)
                
                locX, locY, rot = getStopLoc_byID(i, "startS")

                if(rot == 90 or rot == -90):
                    passengerList[i].spawn_passenger(world, locX+dist, locY, rot)
                
                else:
                    passengerList[i].spawn_passenger(world, locX, locY+dist, rot)

                dist=dist+0.8

        lock1.release()



#MAIN -------------------------------------------------------------------------------------

#driver code 
def main():
    
    #SET ENVOIRMENT----------------------------------------------

    #connecting to server
    client = carla.Client('localhost', 2000)

    #initializing the kampus map (gtuMap)
    world = client.get_world()

    #set the weather of the world
    weather = carla.WeatherParameters(
        cloudiness=60.0,
        sun_altitude_angle=50.0)

    world.set_weather(weather)

    #get map waypoints (distance between 2 points: 0.5)
    waypoints = world.get_map().generate_waypoints(1)



    #INITIALIZE DATAS and CREATE OBJECTS-----------------------------------
    
    #list holds passenger objects
    global passengerList
    #list holds passenger objects
    global vehicleList
    #list of stops to hold coordinates
    global stopList
    global mainStopList
    global campusGraph

    #get campusData from text file and store
    passengerTextData = readObjectDatas()

    #get stopCoordinate data from text file and store it stopList/mainStopList
    readStopDatas()

    #create objects according to data
    passengerList, vehicleList = createObjects(passengerTextData, world)

    #get each stop's number of passenger
    #seperate for start stops and final stops
    getStopData(passengerTextData)

    #implement campus map as a graph 
    #and print all edges
    campusGraph = diGraph.implementCampusGraph()



    #START COUNTER THREAD-----------------------------------------------

    countdown_thread = threading.Thread(target = timeCounter)
    countdown_thread.start()


    #SET ENVOIRMENT SPECTATOR -----------------------------------------

    #create spectator
    spectator = world.get_spectator()

    #show the path on simulator
    spectator.set_transform(carla.Transform(vehicleList[1].carlaTrans.location + carla.Location( x=0,y=-15, z=2), carla.Rotation(yaw=90)))
    sleep(3)


    #START PASSENGER SPAWN THREAD--------------------------------------

    spawn_thread = threading.Thread(target = spawning, args=(world,))
    spawn_thread.start()


    #GREEDY ALGORTIHM-----------------------------------------------
    
    control1 = carla.VehicleControl()
    control2 = carla.VehicleControl()
    control3 = carla.VehicleControl()
    control4 = carla.VehicleControl()
    sleep(1)

    print("AUTONOMUS VEHICLE 1")
    greedy_v1(world, spectator, waypoints, control1, control2, control3, control4)




#GREEDY FUNCTIONS-------------------------------------------------------------------------------------------


#function for greedy approach (first)
#takes passenger - drops passsenger
#capacity control
#vehicle variable updates
#passenger amount according to stops updated
#graph data used to choose the closest next node
#if there is no passenger at the stop, vehicle continues route without stopping
def greedy_v1(world, spectator, waypoints, control1, control2, control3, control4):
    
    start_stopName = 's101'
    next_stopID = -1

    while(start_stopName != 's102'):
        
        #get the compact name for the path
        next_stopName = getClosest(start_stopName)
        next_stopID = int (next_stopName[1:] )
        funcName = start_stopName[1:] + "to" + next_stopName[1:]
        print(funcName)

        #OTHER STOPS (0 to 35)
        if(next_stopID < 101):

            #if there is a passenger at that stop and vehicle has capacity/ or has passenger to drop
            #then go there and stop
            #take the passenger and move
            if( (passengers_at_stops_start[next_stopID] > 0)  and (vehicleList[0].capacity <= 10 or stoppingForDrop(next_stopID, vehicleList[0])) ):
                
                #call the releated function according to sleected path
                vehicleList[0].select_driveway(funcName, waypoints, world, spectator)

                #stop at the end of a junction
                control1.brake=1
                vehicleList[0].carlaObj.apply_control(control1)

                #update vehicle variables
                vehicleList[0].stopCounter = vehicleList[0].stopCounter + 1
                vehicleList[0].distance = vehicleList[0].distance + campusGraph.get_edge_data(start_stopName, next_stopName).get('weight')
                
                #drop the passenger if needed
                if( stoppingForDrop(next_stopID, vehicleList[0]) ):
                    vehicleList[0].psTakenList = dropPassenger(world, next_stopID, vehicleList[0])
                
                #take the passenger
                vehicleList[0].psTakenList, count = takePassenger(next_stopID, vehicleList[0])
                passengers_at_stops_start[next_stopID] = passengers_at_stops_start[next_stopID] - count

                #continue to route
                control1.brake=0
                vehicleList[0].carlaObj.apply_control(control1)
            
            #if vehicle has no capacity pass the stop without stopping
            else:
                vehicleList[0].select_driveway(funcName, waypoints, world, spectator)

        
        #MAIN STOP (101 or 102)
        else:
            #there is a passenger at the next selected stop
            #if you have the capacity then take passenger(s)
            #if there is drop passenger 
            if( (passengers_at_main_stops_start[next_stopID - 100] > 0)  and (vehicleList[0].capacity <= 10 or stoppingForDrop(next_stopID, vehicleList[0])) ):
                
                #call the releated function according to sleected path
                vehicleList[0].select_driveway(funcName, waypoints, world, spectator)

                #stop at the end of a junction
                control1.brake=1
                vehicleList[0].carlaObj.apply_control(control1)

                #update vehicle variables
                vehicleList[0].stopCounter = vehicleList[0].stopCounter + 1
                vehicleList[0].distance = vehicleList[0].distance + campusGraph.get_edge_data(start_stopName, next_stopName).get('weight')
                
                #drop the passenger if needed
                if( stoppingForDrop(next_stopID, vehicleList[0]) ):
                    vehicleList[0].psTakenList = dropPassenger(world, next_stopID, vehicleList[0])
                
                #take the passenger
                vehicleList[0].psTakenList , count = takePassenger(next_stopID, vehicleList[0])
                passengers_at_stops_start[next_stopID] = passengers_at_stops_start[next_stopID] - count

                #continue to route
                control1.brake=0
                vehicleList[0].carlaObj.apply_control(control1)
            
            #if vehicle has no capacity pass the stop without stopping
            else:
                vehicleList[0].select_driveway(funcName, waypoints, world, spectator)
        

        #for loop ends
        #start stop updated to find the next one
        start_stopName = next_stopName

    #while loop ends
    #stop the vehicle
    control1.brake=0
    vehicleList[0].carlaObj.apply_control(control1)
    
    #last stop's passengers are dropped
    if( stoppingForDrop(next_stopID, vehicleList[0]) ):
        vehicleList[0].psTakenList = dropPassenger(world, next_stopID, vehicleList[0])
    
    #calls the second greedy approach
    print("AUTONOMUS VEHICLE 2")
    greedy_v2(world, spectator, waypoints, control2, control3, control4)

    return



#function to find closest next node from graph
#compares according to neighbor nodes weights
def getClosest(node):
    
    cur_weight = 99999999

    #look for node's all neighbors
    for n in campusGraph.neighbors(node):

        #if the weight is  less the previous one, store it
        if(cur_weight > campusGraph.get_edge_data(node, n).get('weight')):
            cur_weight = campusGraph.get_edge_data(node, n).get('weight')
            closest = n

    return closest



#function to simulate taking passengers from stop
#checks passenger list according to start stop ids of each passenger
#if the vehicle has the capacity, accepts the passenger
def takePassenger(stopID, vehicle):

    sleep(1)
    #taken passenger counter
    count = 0
    #temp list 
    takenPassenger = vehicle.psTakenList

    #loop for checking each passenger
    for psgr in passengerList:

        #if the passenger is in the wanted(current) stop and if there is a capacity
        if(psgr.startS == stopID and vehicle.capacity < 10):

            #dd passenger to temp list
            takenPassenger.append(psgr)
            #destroy carla object from simulation
            psgr.carlaObj.destroy()
            #increment taken passenger counter
            count = count + 1
            #increment vehile capacity
            vehicle.capacity = vehicle.capacity + 1
            #print information
            print("VEHICLE (take) -> stopID:", stopID, " capacity:", vehicle.capacity, "  distance:", vehicle.distance )
            sleep(0.7)

    return takenPassenger, count



#function to simulate dropping a passenger to its final stop
#stores the dropped passengers and removes them from vehicle passenger list at the end
def dropPassenger(world, stopID, vehicle):

    #variable for position of the passenger in simulation
    dist = 4
    #empty list for removed passengers
    removes = []
    #templ list
    tempList = vehicle.psTakenList

    #loop for each passenger which are in the vehicle
    for psgr in tempList:

        #if the taken passenger has to be dropped at the current stop
        if(psgr.finalS == stopID):

            #get the location for stop coordinates
            locX, locY, rot = getStopLoc_byID(psgr.id, "finalS")
            #spawn according to degree of the stop
            if(rot == 90 or rot == -90):
                psgr.spawn_passenger(world, locX+dist, locY, rot)

            #spawn according to degree of the stop
            else:
                psgr.spawn_passenger(world, locX, locY+dist, rot)

            #incremen tdist value in order to prevent collision
            dist=dist+0.8

            #decrement vehicle capacity
            vehicle.capacity = vehicle.capacity - 1
            #add choosen passenger to removes list
            removes.append(psgr)
            #print info
            print("VEHICLE (drop) -> stopID: ", stopID, "capacity: ", vehicle.capacity, "  distance: ", vehicle.distance )
            sleep(0.7)

    #remove dropped passenger from vehicle take passanger list
    for p in removes:
        vehicle.psTakenList.remove(p)
        
    return vehicle.psTakenList


#function to check the taken passenger want to be dropped at this stop or not
#if there is return True, otherwise False
def stoppingForDrop(stopID, vehicle):
    
    #if the vehicle taken passenger list empty, rteurn False
    if (len(vehicle.psTakenList) == 0 ) :
        return False

    #if the stop is the final stop for some vehicles taken passenger    
    else:
        for psgr in vehicle.psTakenList:
            if(psgr.finalS == stopID):
                return True

    return False


#function for greedy approach (second)
#takes passenger - drops passsenger
#capacity control
#vehicle variable updates
#passenger amount according to stops updated
#graph data used to choose the closest next node
#if there is no passenger at the stop, vehicle continues route without stopping
def greedy_v2(world, spectator, waypoints, control2, control3, control4):
    
    start_stopName = 's101'
    next_stopID = -1

    while(start_stopName != 's102'):
                
        #get the compact name for the path
        next_stopName = getClosest(start_stopName)
        next_stopID = int (next_stopName[1:] )
        funcName = start_stopName[1:] + "to" + next_stopName[1:]
        print(funcName)

        #OTHER STOPS (0 to 35)
        if(next_stopID < 101):

            #if there is a passenger at that stop and vehicle has capacity/ or has passenger to drop
            #then go there and stop
            #take the passenger and move
            if( (passengers_at_stops_start[next_stopID] > 0)  and (vehicleList[1].capacity <= 10 or stoppingForDrop(next_stopID, vehicleList[1])) ):
                
                #call the releated function according to sleected path
                vehicleList[1].select_driveway(funcName, waypoints, world, spectator)

                #stop at the end of a junction
                control2.brake=1
                vehicleList[1].carlaObj.apply_control(control2)

                #update vehicle variables
                vehicleList[1].stopCounter = vehicleList[1].stopCounter + 1
                vehicleList[1].distance = vehicleList[1].distance + campusGraph.get_edge_data(start_stopName, next_stopName).get('weight')
                
                #drop the passenger if needed
                if( stoppingForDrop(next_stopID, vehicleList[1]) ):
                    vehicleList[1].psTakenList = dropPassenger(world, next_stopID, vehicleList[1])
                
                #take the passenger
                vehicleList[1].psTakenList  , count = takePassenger(next_stopID, vehicleList[1])
                passengers_at_stops_start[next_stopID] = passengers_at_stops_start[next_stopID] - count

                #continue to route
                control2.brake=0
                vehicleList[1].carlaObj.apply_control(control2)
            
            #if vehicle has no capacity pass the stop without stopping
            else:
                vehicleList[1].select_driveway(funcName, waypoints, world, spectator)

        
        #MAIN STOP
        else:
            if( (passengers_at_main_stops_start[next_stopID - 100] > 0)  and (vehicleList[1].capacity <= 10 or stoppingForDrop(next_stopID, vehicleList[1])) ):
                
                #call the releated function according to sleected path
                vehicleList[1].select_driveway(funcName, waypoints, world, spectator)

                #stop at the end of a junction
                control2.brake=1
                vehicleList[1].carlaObj.apply_control(control2)

                #update vehicle variables
                vehicleList[1].stopCounter = vehicleList[1].stopCounter + 1
                vehicleList[1].distance = vehicleList[1].distance + campusGraph.get_edge_data(start_stopName, next_stopName).get('weight')
                
                #drop the passenger if needed
                if( stoppingForDrop(next_stopID, vehicleList[1]) ):
                    vehicleList[1].psTakenList = dropPassenger(world, next_stopID, vehicleList[1])
                
                #take the passenger
                vehicleList[1].psTakenList, count = takePassenger(next_stopID, vehicleList[1])
                passengers_at_stops_start[next_stopID] = passengers_at_stops_start[next_stopID] - count

                #continue to route
                control2.brake=0
                vehicleList[1].carlaObj.apply_control(control2)
            
            #if vehicle has no capacity pass the stop without stopping
            else:
                vehicleList[1].select_driveway(funcName, waypoints, world, spectator)
        


        #for loop ends
        #start stop updated to find the next one
        start_stopName = next_stopName

    #while loop ends
    control2.brake=1
    vehicleList[1].carlaObj.apply_control(control2)
    
    #last stop's passengers are dropped
    if( stoppingForDrop(next_stopID, vehicleList[1]) ):
        vehicleList[1].psTakenList = dropPassenger(world, next_stopID, vehicleList[1])
    
    return



#OTHER FUNCTIONS-------------------------------------------------------------------------------------------------------

#reads passenger data from file
#file contains:
#number of vehicles(at the first line)
#passenger id - start stop - time to spawn - final stop - time to wait (other lines)
#returns a list of each passsenger's data 
#    and a list vehicles
def readObjectDatas():
    
    passData = []

    with open(sys.argv[1], "r") as dataFile: #opens file only to read

        for line in dataFile:
            if( len (line.split()) == 1):
                numV = int(line)
            else:
                passData.append(line.split( )) #get each line and split according to space character
    
    dataFile.close() #close the file
    
    return passData


#reads stop coordinates from file
#file contains:
#stopID - x coor - y coor
#returns a list of each stop's data 
def readStopDatas():
    
    data = []

    with open("stopCoordinates.txt", "r") as dataFile: #opens file only to read

        for line in dataFile:
            data.append(line.split( )) #get each line and split according to space character
    
    dataFile.close() #close the file
    

    for i in range(len(data)):

        stopNo = data[i][0]
        stopNo = int (stopNo[5:])     #get the no of the stop and use it as an index
        line=[]

        if(stopNo <= 35):
            line.append(float(data[i][1])) #x vlaue
            line.append(float(data[i][2]) )#y vlaue
            line.append(float(data[i][3]) )#y vlaue
            stopList.append(line)
            line=[]

        elif(stopNo == 101):
            line.append(float(data[36][1])) #x vlaue
            line.append(float(data[36][2]) )#y vlaue
            line.append(float(data[36][3]) )#y vlaue
            mainStopList.append(line)
            line=[]

        elif(stopNo == 102):
            line.append(float(data[37][1])) #x vlaue
            line.append(float(data[37][2]) )#y vlaue
            line.append(float(data[37][3]) )#y vlaue
            mainStopList.append(line)
            line=[]


#creates passenger object accoridng to data from input file
#store objects in a list
#returns the list of passenger and vehicle objects
def createObjects(passengerData, world):

    passList = []
    vehList = []
    
    #passenger objects
    for i in range(len(passengerData)):

        stopNo1 = passengerData[i][1]
        stopNo1 = int (stopNo1[5:])     #get the no of the stop and use it as an index

        stopNo2 = passengerData[i][3]
        stopNo2 = int (stopNo2[5:])     #get the no of the stop and use it as an index

        ps = Passenger( int(passengerData[i][0]), int(stopNo1), int(passengerData[i][2]), int(stopNo2), int(passengerData[i][4]) , 0)
        passList.append(ps)

    #vehicle objects
    vehicle1, vehicle2, vehicle3, vehicle4, transform1, transform2, transform3, transform4 =  create_vehicles(world)

    vehList.append ( Vehicle(1, 0, 0, 0, 0 ,vehicle1, transform1) )
    vehList.append ( Vehicle(2, 0, 0, 0, 0 ,vehicle2, transform2) )
    vehList.append ( Vehicle(3, 0, 0, 0, 0 ,vehicle3, transform3) )
    vehList.append ( Vehicle(4, 0, 0, 0, 0 ,vehicle4, transform4) )

    return passList, vehList


#function to initialize each stop's number of passenger
#it initializes seperatly for start stops and final stops
#also seperated for main stops and normal stops
def getStopData(passengerData):

    #for start stop no
    for i in range(len(passengerData)):

        stopNo = passengerData[i][1]
        stopNo = int (stopNo[5:])     #get the no of the stop and use it as an index

        if(stopNo <= 36):
            passengers_at_stops_start[stopNo] = passengers_at_stops_start[stopNo] + 1
        else:
            stopNo = stopNo - 100
            passengers_at_main_stops_start[stopNo] = passengers_at_main_stops_start[stopNo] + 1

    #for final stop no
    for j in range(len(passengerData)):

        stopNo = passengerData[j][3]
        stopNo = int (stopNo[5:])   #get the no of the stop and use it as an index

        if(stopNo <= 36):
            passengers_at_stops_final[stopNo] = passengers_at_stops_final[stopNo] + 1
        else:
            stopNo = stopNo - 100
            passengers_at_main_stops_final[stopNo] = passengers_at_main_stops_final[stopNo] + 1


#get the given stop's x and y coordinates
def getStopLoc_byID(id, key):

    if (key == "startS"):
        stopID = passengerList[id].startS
    elif (key == "finalS"):
        stopID = passengerList[id].finalS
    else:
        print("key is not valid.")

    if(stopID <= 35):
        locX = stopList[stopID][0]
        locY = stopList[stopID][1]
        rot = stopList[stopID][2]
    
    else:
        stopID = stopID - 101
        locX = mainStopList[stopID][0]
        locY = mainStopList[stopID][1]
        rot = mainStopList[stopID][2]

    return locX, locY, rot


#function to print passenger and vehicle datas
def printData(passengerList, vehicleList):

    print("passenger: ", len(passengerList))

    for i in range(len(passengerList)):
        print(passengerList[i].id, passengerList[i].startS, passengerList[i].spawnTime, passengerList[i].finalS, passengerList[i].waitTime, passengerList[i].waitLimit)

    print("\nvehicle: ", len(vehicleList))

    for i in range(len(vehicleList)):
        print(vehicleList[i].id, vehicleList[i].capacity, vehicleList[i].stopCounter, vehicleList[i].distance, vehicleList[i].psCounter)


#function to print passenger value at each stop
def printStopData():

    for i in range(36):
        print("s-stop", i, passengers_at_stops_start[i])
    
    for i in range(36):
        print("f-stop", i, passengers_at_stops_final[i])

    print("s-stop1", passengers_at_main_stops_start[1])
    print("s-stop2",  passengers_at_main_stops_start[2])
    print("f-stop1", passengers_at_main_stops_final[1])
    print("f-stop2",  passengers_at_main_stops_final[2])

#function to print each stop's coordinates
def printStopCoor():

    print("Stop Data")
    for i in range(len(stopList)):
            print(stopList[i][0], " ", stopList[i][1])
    
    print("Main Stop Dta")
    for i in range(len(mainStopList)):
        print(mainStopList[i][0], " ", mainStopList[i][1])


#function for marking given waypoints on simulation
def draw_waypoints(world, waypoints, life_time, junctionList):
    
    #for junctions
    junction_path = []
    
    junction_path = drive_route(waypoints, junctionList)

    
    for i in range(len(junction_path)):
        for j in range(len(junction_path[i])):
        
            world.debug.draw_string(junction_path[i][j].transform.location, "*", draw_shadow=False,
                                        color=carla.Color(r=0, g=255, b=0), life_time=life_time,
                                        persistent_lines=True)

    return junction_path




#creating vehicles
def create_vehicles(world): 
    
    #1
    bp_lib = world.get_blueprint_library()
    vehicle1_bp = bp_lib.filter("vehicle.volkswagen.t2")[0]
    vehicle1_bp.set_attribute('color', '253,95,0') #orange
    t1 = carla.Transform(carla.Location(x=20, y=2.5, z=1.85), carla.Rotation(yaw=0))

    #2
    vehicle2_bp = bp_lib.filter("vehicle.volkswagen.t2")[0]
    vehicle2_bp.set_attribute('color', '48,112,223') #blue
    t2 = carla.Transform(carla.Location(x=15, y=2.5, z=1.85), carla.Rotation(yaw=0))

    #3
    vehicle3_bp = bp_lib.filter("vehicle.volkswagen.t2")[0]
    vehicle3_bp.set_attribute('color', '227,234,209') #floral white
    t3 = carla.Transform(carla.Location(x=10, y=2.5, z=1.85), carla.Rotation(yaw=0))

    #4
    vehicle4_bp = bp_lib.filter("vehicle.volkswagen.t2")[0]
    vehicle4_bp.set_attribute('color', '0,0,0') #black
    t4 = carla.Transform(carla.Location(x=5, y=2.5, z=1.85), carla.Rotation(yaw=0))

    #all vehicles are spawned 
    
    v1 = world.spawn_actor(vehicle1_bp, t1)
    v2 = world.spawn_actor(vehicle2_bp, t2)
    v3 = world.spawn_actor(vehicle3_bp, t3)
    v4 = world.spawn_actor(vehicle4_bp, t4)
    
    return v1, v2, v3, v4, t1, t2, t3,t4




#DRIVER CODE-------------------------------------------------------------------------------------

#execute program
if __name__ == '__main__':

    main()