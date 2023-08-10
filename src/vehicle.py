#Author:  Gonca Ezgi Cakır
#Date:  25.04.2021
#Class:  Graduation Project II
#Project:  Kampus Ici Otonom Araclarla Ulasim Simulasyonu

#File:  vehicle.py - contains vehicle class


#import carla library
import time
import glob
import os
import sys
import random

#import carla library
try:
    sys.path.append(glob.glob('../carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

#Vehicle class to represent vehicle in simulation
class Vehicle(object):

  #id: vehicle id
  #capacity: current capacity 
  #stopCounter: number of stopped stops
  #distance: vehicle route's total distance
  #psCounter: number of transported passenger
  #psTakenList: list of currently passengers which are in the vehicle
  #carlaTrans: transform object(carla)
  #carlaObj: vehicle object(carla)
  def __init__(self, id, capacity, stopCounter, distance, psCounter, vehicleObj, vehicleTrans):
    
    self.id = id
    self.capacity = capacity
    self.capacityFlag = 0
    self.stopCounter = stopCounter
    self.distance = distance
    self.psCounter = psCounter
    self.psTakenList = []
    self.carlaObj = vehicleObj
    self.carlaTrans = vehicleTrans



  #function to get route's waypoints
  def drive_route(self, waypoints, route_roads):
      route_path = []

      #loop for given list
      for i in range(len(route_roads)):
          path = []
          temp = []

          #loop for each waypoint
          for waypoint in waypoints:

              #if the lane id and road id is mached, store the waypoints
              if(waypoint.road_id == route_roads[i][0]) and (waypoint.lane_id == route_roads[i][1] ):
                #if the lane id is -1, store iatn path directly
                if(route_roads[i][1] == -1):
                  path.append(waypoint) 
                #if the lane id is 1, store at temp list  
                elif(route_roads[i][1] == 1)  :
                  temp.append(waypoint)

          #traverse the  temp list reversely and store
          if(route_roads[i][1] == 1):
            for k in reversed(temp):
              path.append(k)
          
          #add path to general path
          route_path.append(path)

      return route_path



  #function to drive through given waypoints
  def drive(self, world, spectator, vehicle, view3D, way_path):
      
    vehicle.set_simulate_physics(False)

    #get position for spectator 
    location = vehicle.get_location()
    
    for i in range(len(way_path)):
  
        for j in range(len(way_path[i])):
        
            #wait at each move
            time.sleep(0.09)
            
            #arrange spectator (3D-2D)
            transform = vehicle.get_transform()
            if(view3D == True):
                if(way_path[i][j].road_id == 0 or way_path[i][j].road_id == 17):
                    spectator.set_transform(carla.Transform(transform.location + carla.Location(x=-8,y=0, z=3), carla.Rotation(yaw=0)))
                elif(way_path[i][j].road_id == 21):
                    spectator.set_transform(carla.Transform(transform.location + carla.Location(x=8,y=0, z=3), carla.Rotation(yaw=180)))
                elif(way_path[i][j].road_id == 5 or way_path[i][j].road_id == 26):
                    spectator.set_transform(carla.Transform(transform.location + carla.Location(x=8,y=0, z=3), carla.Rotation(yaw=180)))
                else:
                    spectator.set_transform(carla.Transform(transform.location + carla.Location(x=0,y=8, z=3), carla.Rotation(yaw=-90)))
            else:
                spectator.set_transform(carla.Transform(transform.location + carla.Location(x=0,y=0, z=70), carla.Rotation(yaw=90, pitch=-90)))

            #get new waypoint and transform vehicle
            w = way_path[i][j]
            t = w.transform
            vehicle.set_transform(t)




  #function to initialize road id and lane id information according to wanted path
  # paths are defined and given from greedy approach's node choices
  def select_driveway(self, function_name, waypoints, world, spectator):
    
    #area1
    #s101(S1)---------------------------
    if (function_name == "101to28"):
      route_roads = [[0,-1],[156,-1],[29,-1], [129,-1], [10,-1]]

    elif (function_name == "101to35"):
      route_roads = [[0,-1],[149,-1], [35,1]]

    #s28--------------------------------
    elif (function_name == "28to0"):
      route_roads = [[535,-1], [19,-1],[551,-1],[21,-1]]

    elif (function_name == "28to4"):
      route_roads = [[535,-1],[19,-1],[545,-1], [15,-1], [454,-1], [49, -1]]

    #s29--------------------------------
    elif (function_name == "29to102"):
      route_roads = [[536,1], [10,1],[128,1], [29,1], [155, 1], [0,1]]

    elif (function_name == "29to35"):
      route_roads = [[536,1], [10,1],[128,1], [29,1], [162, 1], [35,1]]

    #s0--------------------------------
    elif (function_name == "0to2"):
      route_roads = [[376,-1],[5,-1]]

    #s1--------------------------------
    elif (function_name == "1to29"):
      route_roads = [ [377, 1], [21,1], [547, 1], [19,1]]

    #s2--------------------------------
    elif (function_name == "2to3"):
      route_roads = [[179, -1], [3,1]]

    elif (function_name == "2to5"):
      route_roads = [[184,-1],[30,-1], [480, 1], [16,1]]

    elif (function_name == "2to6"):
      route_roads = [[184,-1],[30,-1], [464,1], [23,-1], [286,-1]]

    elif (function_name == "2to30"):
      route_roads = [[184,-1],[30,-1], [478, 1], [33,-1]]

    #s33--------------------------------
    elif (function_name == "33to1"):
      route_roads = [[5,-1]]

    #s32--------------------------------
    elif (function_name == "32to33"):
      route_roads = [[343,1],[3,-1],[175,1]]

    elif (function_name == "32to6"):
      route_roads = [[343,1],[3,-1],[170,-1], [30,-1], [464,1], [23,-1], [286,-1]]

    elif (function_name == "32to5"):
      route_roads = [[343,1],[3,-1],[170,-1], [30,-1], [480, 1], [16,1]]

    elif (function_name == "32to30"):
      route_roads = [[343,1],[3,-1],[170,-1], [30,-1], [478, 1], [33,-1]]

    #s3--------------------------------
    elif (function_name == "3to34"):
      route_roads = [[342,1],[26,-1],[318,-1], [17,1]]

    #s34--------------------------------
    elif (function_name == "34to102"):
      route_roads = [[294,1],[35,-1],[148,-1],[0,1]]

    #s35--------------------------------
    elif (function_name == "35to32"):
      route_roads = [[293,1],[17,-1],[313,-1],[26,1]]

    elif (function_name == "35to101"):
      route_roads = [[293,1],[17,-1], [312, -1], [2,-1], [324,-1], [31,-1], [98,-1]]
    
    #area2
    #s6--------------------------------
    elif (function_name == "6to8"):
      route_roads = [[6,-1], [231,-1], [1,1] ]
    elif (function_name == "6to9"):
      route_roads = [ [6,-1], [240,-1], [46,-1], [205,-1], [8,-1] ]
    elif (function_name == "6to7"):
      route_roads = [ [6,-1], [240,-1], [46,-1], [196,-1], [44,-1], [488,-1] ]
    #s7--------------------------------
    elif (function_name == "7to5"):
      route_roads = [ [287,-1], [23,1], [466,1], [16,1] ]
    elif (function_name == "7to30"):
      route_roads = [ [287,-1], [23,1], [479,1], [33,-1] ]

    #s4--------------------------------
    elif (function_name == "4to6"):
      route_roads = [ [136, -1], [16, -1], [465,-1], [23,-1], [286,-1] ]
    elif (function_name == "4to30"):
      route_roads = [ [136, -1], [16, -1], [463,-1], [33, -1] ]
    elif (function_name == "4to3"):
      route_roads = [ [136, -1], [16, -1], [470,-1], [30,1], [174,1], [3,1] ]
    elif (function_name == "4to33"):
      route_roads = [ [136, -1], [16, -1], [470,-1], [30,1], [180, 1] ]

    #s5--------------------------------
    elif (function_name == "5to29"):
      route_roads = [ [137, 1], [49, 1], [456, 1], [15, 1], [543, 1], [19, 1] ]

    #s30-------------------------------
    elif (function_name == "30to26"):
      route_roads = [ [572, -1], [13, -1], [417, -1], [27, -1] ]
    elif (function_name == "30to25"):
      route_roads = [ [572, -1], [13, -1], [423, -1], [50, 1] ]

    #s31--------------------------------
    elif (function_name == "31to3"):
      route_roads = [ [571,1], [33,1], [480, 1], [30,1], [174,1], [3,1] ]
    elif (function_name == "31to5"):
      route_roads = [ [571,1], [33,1], [464, 1], [16,1] ]
    elif (function_name == "31to6"):
      route_roads = [ [571,1], [33,1], [478, 1], [23,-1], [286,-1] ]
    elif (function_name == "31to33"):
      route_roads = [ [571,1], [33,1], [480, 1], [30,1], [180, 1] ]

    #area3
    #s26--------------------------------
    elif (function_name == "26to10"):
      route_roads = [ [395, -1], [12, -1] ]

    #s27--------------------------------
    elif (function_name == "27to31"):
      route_roads = [ [388, 1], [27, 1], [413,1], [13,1] ]
    elif (function_name == "27to25"):
      route_roads = [ [388, 1], [27, 1], [422,1], [50,1] ]

    #s10--------------------------------
    elif (function_name == "10to12"):
      route_roads = [ [186, -1], [14, -1] ]

    #s11--------------------------------
    elif (function_name == "11to27"):
      route_roads = [ [193, 1], [12, 1] ]

    #s12--------------------------------
    elif (function_name == "12to14"):
      route_roads = [ [556, -1], [28, -1], [73, -1], [18, -1] ]
    elif (function_name == "12to16"):
      route_roads = [ [556, -1], [28, -1], [53,-1], [20, -1], [251, -1], [45, -1] ]

    elif (function_name == "12to20"):
      route_roads = [ [556, -1], [28, -1], [53,-1], [20, -1], [265, -1], [34, -1] ]

    elif (function_name == "12to18"):
      route_roads = [ [556, -1], [28, -1], [68, -1], [7,1], [348, 1], [4, -1] ]

    #s13--------------------------------
    elif (function_name == "13to11"):
      route_roads = [ [563,1], [14,1] ]

    #s14--------------------------------
    elif (function_name == "14to20"):
      route_roads = [ [386, -1], [22, -1], [255, -1], [34, -1] ]
    elif (function_name == "14to16"):
      route_roads = [ [386, -1], [22, -1], [244, -1], [45, -1] ]

    #s15--------------------------------
    elif (function_name == "15to18"):
      route_roads = [ [385, 1], [18,1], [75,1], [7,1], [348, 1], [4, -1] ]
    elif (function_name == "15to13"):
      route_roads = [ [385, 1], [18,1], [72,1], [28, 1] ]

    #s16--------------------------------
    elif (function_name == "16to18"):
      route_roads = [ [521, -1], [32, -1], [354, -1], [4, -1]]

    #s17--------------------------------
    elif (function_name == "17to20"):
      route_roads = [ [520, 1], [45,1], [245, 1], [34, -1] ]
    elif (function_name == "17to15"):
      route_roads = [ [520, 1], [45,1], [243, 1], [22,1] ]
    elif (function_name == "17to13"):
      route_roads = [ [520, 1], [45,1], [250,1], [20,1], [52,1], [28,1] ]
   

    #s18--------------------------------
    elif (function_name == "18to23"):
      route_roads = [ [368, -1], [24, -1], [430, -1], [25,1] ]
    elif (function_name == "18to24"):
      route_roads = [ [368, -1], [24, -1], [443, -1], [41,-1] ]

    #s19--------------------------------
    elif (function_name == "19to17"):
      route_roads = [ [367, 1], [4,1], [353, 1], [32,1] ]
    elif (function_name == "19to13"):
      route_roads = [ [367, 1], [4,1], [349, 1], [7, -1], [64, -1], [28,1] ]
    elif (function_name == "19to14"):
      route_roads = [ [367, 1], [4,1], [349, 1], [7, -1], [74,-1], [18, -1] ]

    #s25--------------------------------
    elif (function_name == "25to19"):
      route_roads = [ [575, 1], [41, 1], [442,1], [24,1] ]
    elif (function_name == "25to23"):
      route_roads = [ [575, 1], [41, 1], [437,1], [25,1] ]

    #s24--------------------------------
    elif (function_name == "24to31"):
      route_roads = [ [574,-1], [50, -1], [427, -1], [13,1] ]
    elif (function_name == "24to26"):
      route_roads = [ [574,-1], [50, -1], [418,-1], [27,-1] ]

    #s22--------------------------------
    elif (function_name == "22to24"):
      route_roads = [ [84,-1], [25,-1], [438,-1], [41,-1] ]
    elif (function_name == "22to19"):
      route_roads = [ [84,-1], [25,-1], [429, -1], [24, 1] ]

    #s23--------------------------------
    elif (function_name == "23to21"):
      route_roads = [ [77,1], [48,1] ]
        
    #s20--------------------------------
    elif (function_name == "20to22"):
      route_roads = [ [268, -1], [48, -1] ]

    #s21--------------------------------
    elif (function_name == "21to13"):
      route_roads = [ [269, 1], [34,1] , [266,1], [20,1] , [52,1], [28,1] ]
    elif (function_name == "21to15"):
      route_roads = [  [269, 1], [34,1] , [259,1], [22,1] ]
    elif (function_name == "21to16"):
      route_roads = [  [269, 1], [34,1] , [246, 1], [45,-1] ]


    else:
      print("not found")


    route = self.drive_route(waypoints,route_roads)
    self.drive(world, spectator, self.carlaObj, True, route)





